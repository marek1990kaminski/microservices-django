import random

from django.db.models import QuerySet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, User
from products.producer import publish
from products.serializers import ProductSerializer


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):  # /api/products/
        products: QuerySet[Product] = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):  # /api/products/
        serializer: ProductSerializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):  # /api/products/<str:id>/
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(product)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Product.DoesNotExist as e:
            return Response(
                data={'message': f'not found, error: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )

    def update(self, request, pk=None):  # /api/products/<str:id>/
        try:
            product = Product.objects.get(id=pk)
            serializer = ProductSerializer(instance=product, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            publish('product_updated', serializer.data)

            return Response(
                data=serializer.data,
                status=status.HTTP_202_ACCEPTED
            )
        except Product.DoesNotExist as e:
            return Response(
                data={'message': f'not found, error: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, pk=None):  # /api/products/<str:id>/
        try:
            product = Product.objects.get(id=pk)
            product.delete()
            publish('product_deleted', pk)

            return Response(
                data={'message': 'removed successfully'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Product.DoesNotExist as e:
            return Response(
                data={'message': f'not found, error: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )


class UserAPIView(APIView):
    def get(self, _):
        users: QuerySet[User] = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })

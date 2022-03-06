from django.contrib import admin

# Register your models here.
from products.models import Product
from products.producer import publish
from django.forms.models import model_to_dict


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)

    def save_model(self, request, obj, form, change):
        # super().save_model(request, obj, form, change)
        new_product = Product.objects.create(
            title=request.POST.get('title'),
            image=request.POST.get('image'),
        )

        publish(
            'product_created',
            model_to_dict(
                new_product,
                fields=[field.name for field in new_product._meta.fields if not field.name.startswith('_')]
            )
        )

        # super().save_model(request, obj, form, change)

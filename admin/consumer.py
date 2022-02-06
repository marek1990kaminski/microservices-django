# amqps://auxgvlie:XDN7xkGQH2kFu6QmiHYDZg5GZ-E-h3SN@rat.rmq2.cloudamqp.com/auxgvlie
import django
import json
import os

import pika
from pika import URLParameters, BlockingConnection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin.settings')
django.setup()
from products.models import Product

queue_name = 'admin'

params: URLParameters = pika.URLParameters(
    'amqps://auxgvlie:XDN7xkGQH2kFu6QmiHYDZg5GZ-E-h3SN@rat.rmq2.cloudamqp.com/auxgvlie')

connection: BlockingConnection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    print(f'received in {queue_name}')
    product_id = json.loads(body)
    print(product_id)
    product = Product.objects.get(id=product_id)
    product.likes = product.likes + 1
    product.save()
    print('Product likes increased')


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print('Started consuming')

channel.start_consuming()

channel.close()

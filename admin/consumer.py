# amqps://auxgvlie:XDN7xkGQH2kFu6QmiHYDZg5GZ-E-h3SN@rat.rmq2.cloudamqp.com/auxgvlie
import pika
from pika import URLParameters, BlockingConnection

queue_name = 'admin'

params: URLParameters = pika.URLParameters(
    'amqps://auxgvlie:XDN7xkGQH2kFu6QmiHYDZg5GZ-E-h3SN@rat.rmq2.cloudamqp.com/auxgvlie')

connection: BlockingConnection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=queue_name)


def callback(ch, method, properties, body):
    print(f'received in {queue_name}')
    print(body)


channel.basic_consume(queue=queue_name, on_message_callback=callback)

print('Started consuming')

channel.start_consuming()

channel.close()

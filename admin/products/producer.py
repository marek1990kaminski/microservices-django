import pika
from pika import URLParameters, BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

params: URLParameters = pika.URLParameters(
    'amqps://auxgvlie:XDN7xkGQH2kFu6QmiHYDZg5GZ-E-h3SN@rat.rmq2.cloudamqp.com/auxgvlie')

connection: BlockingConnection = pika.BlockingConnection(params)

channel: BlockingChannel = connection.channel()


def publish():
    channel.basic_publish(exchange='', routing_key='main', body='hello main')

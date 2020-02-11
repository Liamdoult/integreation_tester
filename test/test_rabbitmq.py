import pika
import pytest

from integration_tester import rabbitmq_driver


def test_rabbitmqdriver():
    drive = rabbitmq_driver.RabbitMQDriver(tag="3.8-management")
    drive.wait_until_ready()
    
    credentials = pika.PlainCredentials("guest", "guest")
    parameters= pika.ConnectionParameters("127.0.0.1", "5672", '/', credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare("test")

    channel.basic_publish(exchange="", routing_key="test", body=b'Test message 1.')
    channel.basic_publish(exchange="", routing_key="test", body=b'Test message 2.')

    def consume_test(method_frame, properties, body):
        assert body == b'Test message 1.'
    channel.basic_consume(queue="test", auto_ack=True, on_message_callback=consume_test)

    drive.reset(['test'])
    
    with pytest.raises(pika.exceptions.ChannelClosedByBroker):
        channel.basic_consume(queue="test", auto_ack=True, on_message_callback=consume_test)
    
    del(drive)

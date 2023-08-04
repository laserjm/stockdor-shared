"""
AIORMQ AMQP Client.

# Usage sample:

async def process_received_message(msg):
    print("Received:", str(msg))

async def main():
    AMQP_URL = os.environ['AMQP_URL']
    QUEUE_NAME = os.environ['QUEUE_NAME']
    MESSAGE = "Hello, World!"

    amqp_processor = AMQPMessageProcessor(AMQP_URL, QUEUE_NAME)
    await amqp_processor.send_message(MESSAGE)
    await amqp_processor.receive_messages(process_received_message)

if __name__ == "__main__":
    asyncio.run(main())
"""
import aiormq

from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient


class AiormqAmqpClient(AbstractBrokerClient):
    def __init__(self, amqp_url, queue_name):
        self.amqp_url = amqp_url
        self.queue_name = queue_name

    async def _message_callback(self, channel, body, envelope, properties):
        await self.receive_callback(body)
        await channel.basic_ack(envelope.delivery_tag)

    async def receive_messages(self, receive_callback):
        self.receive_callback = receive_callback
        connection = await aiormq.connect(self.amqp_url)
        channel = await connection.channel()
        await channel.queue_declare(queue=self.queue_name, durable=True)
        await channel.basic_consume(self._message_callback, queue_name=self.queue_name)

    async def send_message(self, message):
        connection = await aiormq.connect(self.amqp_url)
        channel = await connection.channel()
        await channel.queue_declare(queue=self.queue_name, durable=True)
        await channel.basic_publish("", routing_key=self.queue_name, body=message)
        await connection.close()

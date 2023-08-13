"""
AIORMQ AMQP Client.

# Usage sample. Also look https://github.com/mosquito/aiormq/blob/master/README.rst#tutorial.

import asyncio


async def process_received_message(msg):
    print("YEWWWWW, Received:", msg.body.decode())


async def main():
    AMQP_URL = os.environ["AMQP_URL"]
    QUEUE_NAME = os.environ["QUEUE_NAME"]
    MESSAGE = b"Hello, World 1000!"

    amqp_processor = AiormqAmqpClient(AMQP_URL, QUEUE_NAME)
    await amqp_processor.send_message(MESSAGE)
    await amqp_processor.receive_messages(process_received_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
"""
"""
AIORMQ AMQP Client.

# Usage sample. Also look https://github.com/mosquito/aiormq/blob/master/README.rst#tutorial.

import asyncio


async def process_received_message(msg):
    print("YEWWWWW, Received:", msg.body.decode())


async def main():
    AMQP_URL = os.environ["AMQP_URL"]
    QUEUE_NAME = os.environ["QUEUE_NAME"]
    MESSAGE = b"Hello, World 1000!"

    amqp_processor = AiormqAmqpClient(AMQP_URL, QUEUE_NAME)
    await amqp_processor.send_message(MESSAGE)
    await amqp_processor.receive_messages(process_received_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
"""
import aiormq
from aiormq.abc import DeliveredMessage

from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient


class AiormqAmqpClient(AbstractBrokerClient):
    def __init__(self, amqp_url, queue_name):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    async def _get_connection(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aiormq.connect(self.amqp_url)
        return self.connection

    async def _get_channel(self):
        if self.channel is None or self.channel.is_closed:
            connection = await self._get_connection()
            self.channel = await connection.channel()
        return self.channel

    async def receive_messages(self, receive_callback):
        channel = await self._get_channel()
        await channel.basic_qos(prefetch_count=1)
        # Declaring queue
        declare_ok = await channel.queue_declare(self.queue_name)
        try:
            # await channel.basic_consume(declare_ok.queue, receive_callback, no_ack=True)
            message: DeliveredMessage = await channel.basic_get(self.queue_name)
            print(message.body.decode())
        # will be recovered
        except aiormq.exceptions.ChannelClosed as e:
            print(e.msg)
        # consume_ok = await channel.basic_consume(
        #     declare_ok.queue, receive_callback, no_ack=True
        # )
        if self.connection:
            await self.connection.close()

    async def send_message(self, message):
        channel = await self._get_channel()
        declare_ok = await channel.queue_declare(self.queue_name)
        # Sending the message
        await channel.basic_publish(message, routing_key=self.queue_name)
        # Debug
        print(f" [x] Sent {message}")

    async def send_batch_messages(self, messages):
        return await super().send_batch_messages(messages)

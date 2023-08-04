"""
# Usage sample

async def process_received_message(msg):
    print("Received:", msg.content)

async def main():
    STORAGE_CONNECTION_STR = os.environ['STORAGE_CONNECTION_STR']
    QUEUE_NAME = os.environ['QUEUE_NAME']
    MESSAGE = "Hello, World!"

    storage_queue_processor = AzureStorageQueueProcessor(STORAGE_CONNECTION_STR, QUEUE_NAME)
    await storage_queue_processor.send_message(MESSAGE)
    await storage_queue_processor.receive_messages(process_received_message)

if __name__ == "__main__":
    asyncio.run(main())
"""
from azure.storage.queue.aio import QueueServiceClient

from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient


class AzureStorageQueueClient(AbstractBrokerClient):
    def __init__(self, connection_str, queue_name):
        self.connection_str = connection_str
        self.queue_name = queue_name

    async def receive_messages(self, receive_callback):
        queue_service_client = QueueServiceClient.from_connection_string(
            conn_str=self.connection_str
        )
        async with queue_service_client:
            queue_client = queue_service_client.get_queue_client(queue=self.queue_name)
            async with queue_client:
                messages = await queue_client.receive_messages(
                    num_messages=10, visibility_timeout=5 * 60
                )
                for msg in messages:
                    await receive_callback(msg)
                    await queue_client.delete_message(msg)

    async def send_message(self, message):
        queue_service_client = QueueServiceClient.from_connection_string(
            conn_str=self.connection_str
        )
        async with queue_service_client:
            queue_client = queue_service_client.get_queue_client(queue=self.queue_name)
            await queue_client.send_message(message)

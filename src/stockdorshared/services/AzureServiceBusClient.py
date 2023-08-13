"""
Azure Service Bus Client.

# Usage sample:

async def process_received_message(msg):
    print("Received:", str(msg))

async def main():
    SERVICEBUS_CONNECTION_STR = os.environ['SERVICEBUS_CONNECTION_STR']
    QUEUE_NAME = os.environ['QUEUE_NAME']
    MESSAGE = "Hello, World!"

    service_bus_processor = ServiceBusMessageProcessor(SERVICEBUS_CONNECTION_STR, QUEUE_NAME)
    await service_bus_processor.send_message(MESSAGE)
    await service_bus_processor.receive_messages(process_received_message)

if __name__ == "__main__":
    asyncio.run(main())
"""
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage

from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient


class AzureServiceBusClient(AbstractBrokerClient):
    def __init__(self, connection_str, queue_name):
        self.connection_str = connection_str
        self.queue_name = queue_name

    async def receive_messages(self, receive_callback):
        servicebus_client = ServiceBusClient.from_connection_string(
            conn_str=self.connection_str
        )
        async with servicebus_client:
            receiver = servicebus_client.get_queue_receiver(queue_name=self.queue_name)
            async with receiver:
                received_msgs = await receiver.receive_messages(
                    max_message_count=10, max_wait_time=5
                )
                for msg in received_msgs:
                    await receive_callback(msg)
                    await receiver.complete_message(msg)

    async def send_message(self, message):
        async with ServiceBusClient.from_connection_string(
            conn_str=self.connection_str
        ) as client:
            sender = client.get_queue_sender(queue_name=self.queue_name)
            async with sender:
                msg = ServiceBusMessage(message)
                await sender.send_messages(msg)

    def slice_list_into_batches(self, lst, batch_size=700):
        for i in range(0, len(lst), batch_size):
            yield lst[i : i + batch_size]
    
    async def send_batch_messages(self, messages: []):
        batches = list(self.slice_list_into_batches(messages))
        async with ServiceBusClient.from_connection_string(
            conn_str=self.connection_str
        ) as client:
            sender = client.get_queue_sender(queue_name=self.queue_name)
            async with sender:
                for batch in batches:
                    await self.send_batch_message(sender, batch)
    
    async def send_batch_message(self, sender, message_bodies):
        batch_message = await sender.create_message_batch()
        for msg in message_bodies:
            try:
                batch_message.add_message(ServiceBusMessage(msg))
            except ValueError:
                # ServiceBusMessageBatch object reaches max_size.
                # New ServiceBusMessageBatch object can be created here to send more data.
                break
        await sender.send_messages(batch_message)

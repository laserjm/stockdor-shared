"""Azure Service Bus Client."""
from azure.servicebus.aio import ServiceBusClient

from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient


class AzureServiceBusClient(AbstractBrokerClient):
    def __init__(self, connection_str, queue_name, callback):
        self.connection_str = connection_str
        self.queue_name = queue_name
        self.callback = callback

    async def send_message(self, message):
        return super().send_message(message)

    async def receive_messages(self):
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
                    await self.callback(msg)
                    await receiver.complete_message(msg)

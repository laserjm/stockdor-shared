"""
# Example usage
if __name__ == "__main__":
    factory = BrokerClientFactory()

    azure_service_bus_client = factory.create_broker_client(BrokerType.AZURE_SERVICE_BUS.value)
    azure_storage_queue_client = factory.create_broker_client(BrokerType.AZURE_STORAGE_QUEUE.value)
    amqp_pika_client = factory.create_broker_client(BrokerType.AMQP_PIKA.value)
    
    # Now you can use the created clients to connect, send, and receive messages.
"""
from stockdorshared.services.AbstractBrokerClient import AbstractBrokerClient
from stockdorshared.services.AiormqAmqpClient import AiormqAmqpClient
from stockdorshared.services.AzureServiceBusClient import AzureServiceBusClient
from stockdorshared.services.AzureStorageQueueClient import AzureStorageQueueClient
from stockdorshared.services.BrokerType import BrokerType


class BrokerClientFactory:
    @staticmethod
    def create_broker_client(broker_type) -> AbstractBrokerClient:
        if broker_type == BrokerType.AZURE_SERVICE_BUS.value:
            return AzureServiceBusClient()
        elif broker_type == BrokerType.AZURE_STORAGE_QUEUE.value:
            return AzureStorageQueueClient()
        elif broker_type == BrokerType.AIORMQ_AMQP.value:
            return AiormqAmqpClient()
        else:
            raise ValueError("Invalid broker type")

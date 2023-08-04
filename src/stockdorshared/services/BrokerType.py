from enum import Enum


class BrokerType(Enum):
    AZURE_SERVICE_BUS = "azure_service_bus"
    AZURE_STORAGE_QUEUE = "azure_storage_queue"
    AIORMQ_AMQP = "aiormq_amqp"

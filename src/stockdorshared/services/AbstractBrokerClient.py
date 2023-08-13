from abc import ABC, abstractmethod


class AbstractBrokerClient(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    async def send_batch_messages(self, messages):
        pass

    @abstractmethod
    async def receive_messages(self):
        pass

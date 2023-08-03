from abc import ABC, abstractmethod


class AbstractBrokerClient(ABC):
    @abstractmethod
    async def send_message(self, message):
        pass

    @abstractmethod
    async def receive_messages(self):
        pass

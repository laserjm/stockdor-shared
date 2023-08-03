from abc import ABC, abstractmethod

class AbstractBrokerClient(ABC):
    @abstractmethod
    async def receive_messages(self):
        pass
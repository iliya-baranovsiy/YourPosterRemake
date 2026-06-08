from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    async def create_record(self):
        pass

    @abstractmethod
    async def get_record(self):
        pass

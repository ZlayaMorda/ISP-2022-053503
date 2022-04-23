from abc import ABC, abstractmethod

class Serializer(ABC):

    @classmethod
    @abstractmethod
    def factory_serialize(cls, obj):
        pass

    @classmethod
    @abstractmethod
    def factory_deserialize(cls, obj):
        pass

    @classmethod
    def dumps(cls, obj) -> str:
        return factory_serialize(obj)

    @classmethod
    def loads(cls, obj) -> any:
        return factory_deserialize(obj)

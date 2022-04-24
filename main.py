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


def dumps(serializer: Serializer, obj) -> str:
    return serializer.factory_serialize(obj)


def loads(serializer: Serializer, obj) -> any:
    return serializer.factory_deserialize(obj)

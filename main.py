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


def dump(serializer: Serializer, obj, path):
    with open(path, "w") as file:
        file.write(serializer.factory_serialize(obj))


def load(serializer: Serializer, path):
    with open(path, "r") as file:
        return serializer.factory_deserialize(file.readline())


def check(one, two):
    return (one + two) ** 2


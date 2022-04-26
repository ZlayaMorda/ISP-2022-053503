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


def check(one, two):
    return (one + two) ** 2


class Person:

    def __init__(self, one, two):
        self.one = one
        self.two = two

    def sum(self):
        return self.one + self.two


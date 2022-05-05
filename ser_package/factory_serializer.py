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
    """
    serialize to string
    :param serializer: class(Serializer)
    :param obj: any
    :return: str
    """
    return serializer.factory_serialize(obj)


def loads(serializer: Serializer, obj) -> any:
    """
    deserialize to any
    :param serializer: class(Serializer)
    :param obj: str
    :return: any
    """
    return serializer.factory_deserialize(obj)


def dump(serializer: Serializer, obj, path):
    """
    serialize to file, open to write
    :param serializer: class(Serializer)
    :param obj: any
    :param path: path to file
    :return: str
    """
    with open(path, "w") as file:
        file.write(serializer.factory_serialize(obj))


def load(serializer: Serializer, path):
    """
    deserialize from file, open to read
    :param serializer: class(Serializer)
    :param path: path to file
    :return: any
    """
    with open(path, "r") as file:
        string = ""
        for i in file.readlines():
            string += i
        return serializer.factory_deserialize(string)

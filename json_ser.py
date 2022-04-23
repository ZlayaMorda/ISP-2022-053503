from main import Serializer

import re


class JsonSerializer(Serializer):

    @classmethod
    def factory_serialize(cls, obj):
        return cls.serialize(obj)

    @classmethod
    def factory_deserialize(cls, obj):
        return cls.deserialize(obj)

    @classmethod
    def serialize(cls, obj):
        """
        :param obj: object to serialize
        :return: tuple, which will be converted to json string
        """
        ser = cls.choose_type_method(obj)
        ser = ser(obj)
        return tuple((temp, ser[temp]) for temp in ser)

    @classmethod
    def choose_type_method(cls, obj):
        """
        :param obj: object to serialize
        :return: method to convert different types
        """
        if isinstance(obj, int, float, complex, bool, str, type(None)):
            return cls.serialize_standart(obj)

    @classmethod
    def serialize_standart(cls, obj):
        """
        serialize int, float, complex, bool, str, None
        to dict with ["type"] and ["value"]
        :param obj: int, float, complex, bool, str, None
        :return: dict
        """
        ser_dick = dict()
        ser_dick["type"] = re.search(r"\w+", str(type(obj)))
        ser_dick["value"] = obj
        return ser_dick


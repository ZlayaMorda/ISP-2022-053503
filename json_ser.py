from main import Serializer
from pydoc import locate
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
        ser = cls.choose_serialize_type_method(obj)
        return tuple((temp, ser[temp]) for temp in ser)

    @classmethod
    def choose_serialize_type_method(cls, obj):
        """
        :param obj: object to serialize
        :return: method to convert different types
        """
        if isinstance(obj, (int, float, complex, bool, str, type(None))):
            return cls.serialize_standart(obj)
        elif isinstance(obj, (list, tuple, bytes, bytearray, set, frozenset)):
            return cls.serialize_structures(obj)
        elif isinstance(obj, dict):
            return cls.serialize_dict(obj)

    @classmethod
    def serialize_standart(cls, obj):
        """
        serialize to dict
        :param obj: int, float, complex, bool, str, None
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        ser_dick = dict()
        ser_dick["type"] = re.search(r"\'(\w+)\'", str(type(obj))).group(1)
        ser_dick["value"] = obj
        return ser_dick

    @classmethod
    def serialize_structures(cls, obj):
        """
        serialize to dict
        :param obj: list, tuple, bytes, bytearray, set, frozenset
        :return: tuple ict with keys: ["type"] and ["value"]
        """
        ser_dick = dict()
        ser_dick["type"] = re.search(r"\'(\w+)\'", str(type(obj))).group(1)
        ser_dick["value"] = tuple([cls.serialize(temp_obj) for temp_obj in obj])
        return ser_dick

    @classmethod
    def serialize_dict(cls, obj):
        """
        serialize do dict
        :param obj: dict
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        ser_dic = dict()
        ser_dic["type"] = "dict"
        ser_dic["value"] = {}
        for i in obj:
            key = cls.serialize(i)
            value = cls.serialize(obj[i])
            ser_dic["value"][key] = value

        ser_dic["value"] = tuple((key, ser_dic["value"][key]) for key in ser_dic["value"])
        return ser_dic

    @classmethod
    def deserialize(cls, obj):
        """
        :param obj: tuple
        :return: deserialized object
        """
        obj = dict((obj_type, obj_value) for obj_type, obj_value in obj)
        return cls.choose_deserialize_type_method(obj["type"], obj["value"])

    @classmethod
    def choose_deserialize_type_method(cls, obj_type, obj_value):
        """
        :param obj_type: type str
        :param obj_value: tuple value
        :return: deserialized object
        """
        if obj_type in ["int", "float", "complex", "bool", "str", "NoneType"]:
            return cls.deserialize_standart(obj_type, obj_value)
        elif obj_type in ["list", "tuple", "bytes", "bytearray", "set", "frozenset"]:
            return cls.deserialize_structures(obj_type, obj_value)
        elif obj_type == "dict":
            return cls.deserialize_dict(obj_value)

    @classmethod
    def deserialize_standart(cls, obj_type, obj_value):
        """
        deserialize returned types
        :param obj_type: type str
        :param obj_value: tuple value
        :return: int, float, complex, bool, str, None
        """
        if obj_type == "NoneType":
            return None
        elif obj_type == "bool":
            return obj_value is True
        else:
            return locate(obj_type)(obj_value)

    @classmethod
    def deserialize_structures(cls, obj_type, obj_value):
        """
               deserialize returned types
               :param obj_type: type str
               :param obj_value: tuple value
               :return: list, tuple, bytes, bytearray, set, frozenset
        """
        if obj_type == "list":
            return [cls.deserialize(temp) for temp in obj_value]
        elif obj_type == "tuple":
            return tuple([cls.deserialize(temp) for temp in obj_value])
        elif obj_type == "bytes":
            return bytes([cls.deserialize(temp) for temp in obj_value])
        elif obj_type == "bytearray":
            return bytearray([cls.deserialize(temp) for temp in obj_value])
        elif obj_type == "set":
            return set([cls.deserialize(temp) for temp in obj_value])
        elif obj_type == "frozenset":
            return frozenset([cls.deserialize(temp) for temp in obj_value])

    @classmethod
    def deserialize_dict(cls, obj_value):
        dic = {}
        for key in obj_value:
            dic[cls.deserialize(key[0])] = cls.deserialize(key[1])
        return dic

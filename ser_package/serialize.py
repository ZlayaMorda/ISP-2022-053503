import re
import inspect
from ser_package.json_constants import *


class JsonSerialize:

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
        elif inspect.isfunction(obj):
            return cls.serialize_function(obj)
        elif inspect.isclass(obj):
            return cls.serialize_class(obj)
        elif inspect.ismodule(obj):
            return cls.serialize_module(obj)
        elif isinstance(obj, type(type.__dict__)):
            return cls.serialize_instance(obj)
        else:
            return cls.serialize_instance(obj)

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
    def serialize_function(cls, obj):
        """
        serialize func
        :param obj: function
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        ser_dic = dict()
        ser_dic["type"] = "function"
        ser_dic["value"] = {}
        members = inspect.getmembers(obj)
        members = [i for i in members if i[0] in FUNCTION_ATTRIBUTES]
        for i in members:
            key = cls.serialize(i[0])
            if i[0] != "__closure__":
                value = cls.serialize(i[1])
            else:
                value = cls.serialize(None)

            ser_dic["value"][key] = value
            if i[0] == "__code__":
                key = cls.serialize("__globals__")
                ser_dic["value"][key] = {}
                names = i[1].__getattribute__("co_names")
                glob = obj.__getattribute__("__globals__")
                glob_dict = {}
                for name in names:
                    if name == obj.__name__:
                        glob_dict[name] = obj.__name__
                    elif name in glob and not inspect.ismodule(name) and name not in __builtins__:
                        glob_dict[name] = glob[name]
                ser_dic["value"][key] = cls.serialize(glob_dict)
        ser_dic["value"] = tuple((k, ser_dic["value"][k]) for k in ser_dic["value"])
        return ser_dic

    @classmethod
    def serialize_class(cls, obj):
        """
        serialize class
        :param obj: class
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        ser = dict()
        ser["type"] = "class"
        ser["value"] = {}
        ser["value"][cls.serialize("__name__")] = \
            cls.serialize(obj.__name__)
        members = []
        for i in inspect.getmembers(obj):
            if not (i[0] in NOT_CLASS_ATTRIBUTES):
                members.append(i)

        cls.iter_member(members, ser)
        ser["value"] = tuple((k, ser["value"][k]) for k in ser["value"])

        return ser

    @classmethod
    def serialize_instance(cls, obj):
        """
        serialize descriptors, mapping proxy, builtins
        :param obj: descriptors, mapping proxy, builtins
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        if re.search(r"\'(\w+)\'", str(type(obj))) is None:
            return None
        ser = dict()
        ser["type"] = re.search(r"\'(\w+)\'", str(type(obj))).group(1)

        ser["value"] = {}
        members = inspect.getmembers(obj)
        members = [i for i in members if not callable(i[1])]
        cls.iter_member(members, ser)
        ser["value"] = tuple((k, ser["value"][k]) for k in ser["value"])

        return ser

    @classmethod
    def serialize_module(cls, obj):
        """
        serialize module
        :param obj: module
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        ser = dict()
        ser["type"] = "__module__name__"
        ser["value"] = re.search(r"\'(\w+)\'", str(obj)).group(1)

        return ser

    @classmethod
    def iter_member(cls, members, ser):
        for i in members:
            key = cls.serialize(i[0])
            val = cls.serialize(i[1])
            ser["value"][key] = val

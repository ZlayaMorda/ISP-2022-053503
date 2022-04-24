from main import Serializer
from pydoc import locate
from types import CodeType, FunctionType
import re
import inspect


class JsonSerializer(Serializer):

    FUNCTION_ATTRIBUTES = [
        "__code__",
        "__name__",
        "__defaults__",
        "__closure__"
    ]

    CODE_OBJECT_ARGS = [
        'co_argcount',
        'co_posonlyargcount',
        'co_kwonlyargcount',
        'co_nlocals',
        'co_stacksize',
        'co_flags',
        'co_code',
        'co_consts',
        'co_names',
        'co_varnames',
        'co_filename',
        'co_name',
        'co_firstlineno',
        'co_lnotab',
        'co_freevars',
        'co_cellvars'
    ]

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
        elif inspect.isfunction(obj):
            return cls.serialize_function(obj)

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
        ser_dic = dict()
        ser_dic["type"] = "function"
        ser_dic["value"] = {}
        members = inspect.getmembers(obj)
        members = [i for i in members if i[0] in cls.FUNCTION_ATTRIBUTES]
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
        print(ser_dic["value"])
        ser_dic["value"] = tuple((k, ser_dic["value"][k]) for k in ser_dic["value"])
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
        elif obj_type == "function":
            return cls.deserialize_function(obj_value)

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
    
    @classmethod
    def deserialize_function(cls, obj_value):
        func = [0] * 4
        code = [0] * 16
        glob = {"__builtins__": __builtins__}
        for i in obj_value:
            key = cls.deserialize(i[0])

            if key == "__globals__":
                glob_dict = cls.deserialize(i[1])
                for glob_key in glob_dict:
                    glob[glob_key] = glob_dict[glob_key]
            elif key == "__code__":
                val = i[1][1][1]
                for arg in val:
                    code_arg_key = cls.deserialize(arg[0])
                    if code_arg_key != "__doc__":
                        code_arg_val = cls.deserialize(arg[1])
                        index = cls.CODE_OBJECT_ARGS.index(code_arg_key)
                        code[index] = code_arg_val

                code = CodeType(*code)
            else:
                index = cls.FUNCTION_ATTRIBUTES.index(key)
                func[index] = (cls.deserialize(i[1]))

        func[0] = code
        func.insert(1, glob)

        des = FunctionType(*func)
        if des.__name__ in des.__getattribute__("__globals__"):
            des.__getattribute__("__globals__")[des.__name__] = des

        return des
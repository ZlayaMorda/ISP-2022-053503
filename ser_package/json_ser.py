from ser_package.factory_serializer import Serializer
from pydoc import locate
from types import CodeType, FunctionType
import re
import inspect
import ast


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
    NOT_CLASS_ATTRIBUTES = [
        "__class__",
        "__getattribute__",
        "__new__",
        "__setattr__",
    ]

    @classmethod
    def factory_serialize(cls, obj):
        return cls.convert_str(cls.serialize(obj), True)

    @classmethod
    def factory_deserialize(cls, obj):
        return cls.deserialize(cls.convert_str(obj, False))

    @classmethod
    def convert_str(cls, serialized, convert):
        """
        Convert string to json format
        """
        if convert:
            ser = str(serialized)
            ser = ser.replace("(", "{").replace(")", "}") \
                .replace("'type',", "'type':").replace("'value',", "'value':")
            return ser
        else:
            ser = serialized.replace("{", "(").replace("}", ")") \
                .replace("'type':", "'type',").replace("'value':", "'value',")

            return ast.literal_eval(ser)

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
        elif inspect.iscode(obj):
            return cls.serialize_instance(obj)
        elif inspect.ismethoddescriptor(obj) or inspect.isbuiltin(obj):
            return cls.serialize_instance(obj)
        elif inspect.isgetsetdescriptor(obj):
            return cls.serialize_instance(obj)
        elif inspect.ismodule(obj):
            return cls.serialize_module(obj)
        elif isinstance(obj, type(type.__dict__)):
            return cls.serialize_instance(obj)
        else:
            return cls.serialize_object(obj)

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
            if not (i[0] in cls.NOT_CLASS_ATTRIBUTES):
                members.append(i)

        cls.iter_member(members, ser)
        ser["value"] = tuple((k, ser["value"][k]) for k in ser["value"])

        return ser

    @classmethod
    def serialize_object(cls, obj):
        """
        serialize object
        :param obj: object
        :return: tuple dict with keys: ["type"] and ["value"]
        """
        class_obj = type(obj)
        ser = dict()
        ser["type"] = "object"
        ser["value"] = {}
        ser["value"][cls.serialize("__object_type__")] = \
            cls.serialize(class_obj)
        ser["value"][cls.serialize("__fields__")] = \
            cls.serialize(obj.__dict__)
        ser["value"] = tuple((k, ser["value"][k]) for k in ser["value"])

        return ser

    @classmethod
    def serialize_instance(cls, obj):
        """
        serialize descriptors, mapping proxy, builtins
        :param obj: descriptors, mapping proxy, builtins
        :return: tuple dict with keys: ["type"] and ["value"]
        """
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
        elif obj_type == "class":
            return cls.deserialize_class(obj_value)
        elif obj_type == "object":
            return cls.deserialize_object(obj_value)
        elif obj_type == "__module__name__":
            return cls.deserialize_module(obj_value)

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
        """
        deserialize dict
        :param obj_value: tuple value
        :return: dict
        """
        dic = {}
        for key in obj_value:
            dic[cls.deserialize(key[0])] = cls.deserialize(key[1])
        return dic

    @classmethod
    def deserialize_function(cls, obj_value):
        """
        deserialize function
        :param obj_value: tuple value
        :return: function
        """
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

    @classmethod
    def deserialize_object(cls, obj):
        """
        deserialize object
        :param obj: tuple value
        :return: object
        """
        obj_dict = cls.deserialize_dict(obj)
        fields = []
        for key in obj_dict["__fields__"]:
            fields.append(obj_dict["__fields__"][key])
        result = obj_dict["__object_type__"](*fields)
        for key, value in obj_dict["__fields__"].items():
            result.key = value
        return result

    @classmethod
    def deserialize_class(cls, class_dict):
        """
        deserialize class
        :param class_dict: tuple value
        :return: class
        """
        some_dict = cls.deserialize_dict(class_dict)
        name = some_dict["__name__"]
        del some_dict["__name__"]
        return type(name, (object,), some_dict)

    @classmethod
    def deserialize_module(cls, obj):
        """
        deserialize module
        :param obj: tuple value
        :return: module
        """
        return __import__(obj)

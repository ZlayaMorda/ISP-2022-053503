from ser_package.json_constants import *
from pydoc import locate
from types import CodeType, FunctionType


class JsonDeserialize:
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
                        index = CODE_OBJECT_ARGS.index(code_arg_key)
                        code[index] = code_arg_val

                code = CodeType(*code)
            else:
                index = FUNCTION_ATTRIBUTES.index(key)
                func[index] = (cls.deserialize(i[1]))

        func[0] = code
        func.insert(1, glob)

        des = FunctionType(*func)
        if des.__name__ in des.__getattribute__("__globals__"):
            des.__getattribute__("__globals__")[des.__name__] = des

        return des

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

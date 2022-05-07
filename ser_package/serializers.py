from ser_package.factory_serializer import Serializer
from ser_package.serialize import Serialize
from ser_package.deserialize import Deserialize
import ast
import yaml
import toml


class JsonSerializer(Serializer):

    @classmethod
    def factory_serialize(cls, obj, from_type, to_type):
        if from_type is None or to_type is None:
            return cls.convert_str(Serialize.serialize(obj), True)
        else:
            return convert(from_type, to_type, obj)

    @classmethod
    def factory_deserialize(cls, obj):
        return Deserialize.deserialize(cls.convert_str(obj, False))

    @classmethod
    def convert_str(cls, serialized, is_not_back):
        """
        Convert string to json format
        """
        if is_not_back:
            ser = str(serialized)
            ser = ser.replace("(", "{").replace(")", "}") \
                .replace("'type',", "'type':").replace("'value',", "'value':")
            return ser
        else:
            ser = serialized.replace("{", "(").replace("}", ")") \
                .replace("'type':", "'type',").replace("'value':", "'value',")

            return ast.literal_eval(ser)


class YamlSerializer(Serializer):
    @classmethod
    def factory_serialize(cls, obj, from_type, to_type):
        if from_type is None or to_type is None:
            return yaml.dump(Serialize.serialize(obj))
        else:
            return convert(from_type, to_type, obj)

    @classmethod
    def factory_deserialize(cls, obj):
        return Deserialize.deserialize(yaml.load(obj))


class TomlSerializer(Serializer):
    @classmethod
    def factory_serialize(cls, obj, from_type, to_type):
        if from_type is None or to_type is None:
            return toml.dumps({"data": str(Serialize.serialize(obj))})
        else:
            return convert(from_type, to_type, obj)

    @classmethod
    def factory_deserialize(cls, obj):
        return Deserialize.deserialize(ast.literal_eval(toml.loads(obj)['data']))


def convert(from_type, to_type, obj):
    if from_type == "json" and (to_type == "toml" or to_type == "yaml"):
        new_obj = obj.replace("{", "(").replace("}", ")") \
            .replace("'type':", "'type',").replace("'value':", "'value',")
        if to_type == "yaml":
            return yaml.dump(ast.literal_eval(new_obj))
        else:
            return toml.dumps({"data": new_obj})
    elif from_type == "toml" and (to_type == "json" or to_type == "yaml"):
        new_obj = toml.loads(obj)['data']
        if to_type == "json":
            return JsonSerializer.convert_str(new_obj, True)
        else:
            return yaml.dump(ast.literal_eval(new_obj))
    elif from_type == "yaml" and (to_type == "json" or to_type == "toml"):
        new_obj = yaml.load(obj)
        if to_type == "json":
            return JsonSerializer.convert_str(new_obj, True)
        else:
            return toml.dumps({"data": str(new_obj)})
    else:
        print("input correct type: json, toml or yaml")
        return None

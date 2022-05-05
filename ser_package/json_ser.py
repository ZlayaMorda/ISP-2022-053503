from ser_package.factory_serializer import Serializer
from ser_package.serialize import Serialize
from ser_package.deserialize import Deserialize
import ast
import yaml


class JsonSerializer(Serializer):

    @classmethod
    def factory_serialize(cls, obj):
        return cls.convert_str(Serialize.serialize(obj), True)

    @classmethod
    def factory_deserialize(cls, obj):
        return Deserialize.deserialize(cls.convert_str(obj, False))

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


class YamlSerializer(Serializer):
    @classmethod
    def factory_serialize(cls, obj):
        return yaml.dump(Serialize.serialize(obj))

    @classmethod
    def factory_deserialize(cls, obj):
        return Deserialize.deserialize(yaml.load(obj))

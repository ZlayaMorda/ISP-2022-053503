from ser_package.factory_serializer import Serializer
from ser_package.serialize import JsonSerialize
from ser_package.deserialize import JsonDeserialize
import ast


class JsonSerializer(Serializer):

    @classmethod
    def factory_serialize(cls, obj):
        return cls.convert_str(JsonSerialize.serialize(obj), True)

    @classmethod
    def factory_deserialize(cls, obj):
        return JsonDeserialize.deserialize(cls.convert_str(obj, False))

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

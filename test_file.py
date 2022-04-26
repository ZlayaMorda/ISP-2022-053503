from main import *
from json_ser import JsonSerializer

print(JsonSerializer.deserialize(JsonSerializer.serialize(Person(1, 2))))
# print(JsonSerializer.deserialize(JsonSerializer.serialize(Person())))

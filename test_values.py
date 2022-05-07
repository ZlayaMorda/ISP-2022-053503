import ast
import math
from ser_package.serializers import *

test_int = 5
test_float = 4.723948
test_complex = 4 + 5j
test_bool_true = True
test_bool_false = False
test_str = "ooh haayooo"
test_none = None

test_list = list(x for x in range(10))
test_tuple = tuple(x for x in range(10))
test_bytes = bytes('puk puk puk', encoding='utf-8')
test_bytearray = bytearray('puk puk puk', encoding='utf-8')
test_set = set(x for x in range(10))
test_frozen_set = frozenset(x for x in range(10))

test_dict_1 = {"puk": 1, "puk puk": 1.213}
test_dict_2 = {(1, 2, 3): "biba", 1234: "boba"}
test_dict_3 = {"kek": test_dict_2.copy(), "lol": test_dict_2.copy()}


def test_fun_1():
    return 1234


def test_fun_2(one, two):
    print(one + two)
    return one + two


def test_fun_3(one, *args):
    for i in args:
        one += i
    return one


def test_fun_wrap(one, two):
    return test_fun_3(one, two)


c = 42


def big_boss_fun(x):
    a = 123
    return math.sin(x * a * c)


class Puk:
    def __init__(self, one, two):
        self.one = one
        self.two = two

    def sum(self):
        return self.one + self.two


test_convert = "{{'type': 'dict'}, {'value': {{{{'type': 'int'}, {'value': 123}}, {{'type': 'int'}, {'value': 23}}}, {{{'type': 'int'}, {'value': 234}}, {{'type': 'int'}, {'value': 23789}}}}}}"

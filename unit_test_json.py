import unittest
import ser_package.factory_serializer as fs
import ser_package.json_ser as js
from test_values import *


class TestJsonSerialize(unittest.TestCase):
    def setUp(self):
        self.file_name = "ser.json"

    def check_equals(self, test):
        self.assertEqual(test, fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), test)))
        self.assertIsNone(fs.dump(js.JsonSerializer(), test, self.file_name))
        self.assertEqual(test, fs.load(js.JsonSerializer(), self.file_name))

    def check_fun_other(self, test, *args):
        self.assertEqual(test(*args), fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), test))(*args))
        self.assertIsNone(fs.dump(js.JsonSerializer(), test, self.file_name))
        self.assertEqual(test(*args), fs.load(js.JsonSerializer(), self.file_name)(*args))

    def test_standart(self):
        self.check_equals(test_int)
        self.check_equals(test_float)
        self.check_equals(test_complex)
        self.check_equals(test_str)
        self.check_equals(test_none)
        self.assertTrue(fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), True)))
        fs.dump(js.JsonSerializer(), True, self.file_name)
        self.assertTrue(fs.load(js.JsonSerializer(), self.file_name))
        self.assertFalse(fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), False)))
        fs.dump(js.JsonSerializer(), False, self.file_name)
        self.assertFalse(fs.load(js.JsonSerializer(), self.file_name))
        self.assertEqual(test_int, js.JsonSerializer.
                         factory_deserialize(js.JsonSerializer.factory_serialize(test_int)))
        self.assertEqual(test_int, js.JsonDeserialize.
                         deserialize_standart(js.JsonSerialize.serialize_standart(test_int)["type"],
                                              js.JsonSerialize.serialize_standart(test_int)["value"]))

    def test_structures(self):
        self.check_equals(test_list)
        self.check_equals(test_tuple)
        self.check_equals(test_bytes)
        self.check_equals(test_bytearray)
        self.check_equals(test_set)
        self.check_equals(test_frozen_set)

    def test_dict(self):
        self.check_equals(test_dict_1)
        self.check_equals(test_dict_2)
        self.check_equals(test_dict_3)

    def test_function(self):
        self.check_fun_other(test_fun_1)
        self.check_fun_other(test_fun_2, "ha", "dushnila")
        self.check_fun_other(test_fun_3, 3, 4, 5, 6)
        self.check_fun_other(big_boss_fun, 12)

    def test_class(self):
        self.assertEqual(Puk(1, 2).one, fs.loads(js.JsonSerializer(),
                                                 fs.dumps(js.JsonSerializer(), Puk))(1, 2).one)
        self.assertEqual(Puk(1, 2).two, fs.loads(js.JsonSerializer(),
                                                 fs.dumps(js.JsonSerializer(), Puk))(1, 2).two)

        self.assertEqual(Puk(1, 2).sum(), fs.loads(js.JsonSerializer(),
                                                   fs.dumps(js.JsonSerializer(), Puk))(1, 2).sum())

    def test_convert(self):
        self.assertEqual(test_convert,
                         js.JsonSerializer.convert_str(js.JsonSerialize.serialize({123: 23, 234: 23789}), True))
        self.assertEqual(js.JsonSerialize.serialize({123: 23, 234: 23789}),
                         js.JsonSerializer.convert_str(test_convert, False))


if __name__ == "__main__":
    unittest.main()

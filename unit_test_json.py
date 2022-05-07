import unittest
import ser_package.factory_serializer as fs
import ser_package.serializers as js
from test_values import *


class TestJsonSerialize(unittest.TestCase):
    def setUp(self):
        self.file_name_json = "ser.json"
        self.file_name_yaml = "ser.yaml"
        self.file_name_toml = "ser.toml"

    def check_equals(self, test):
        self.assertEqual(test, fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), test)))
        self.assertIsNone(fs.dump(js.JsonSerializer(), test, self.file_name_json))
        self.assertEqual(test, fs.load(js.JsonSerializer(), self.file_name_json))

        self.assertEqual(test, fs.loads(js.YamlSerializer(), fs.dumps(js.YamlSerializer(), test)))
        self.assertIsNone(fs.dump(js.YamlSerializer(), test, self.file_name_yaml))
        self.assertEqual(test, fs.load(js.YamlSerializer(), self.file_name_yaml))

        self.assertEqual(test, fs.loads(js.TomlSerializer(), fs.dumps(js.TomlSerializer(), test)))
        self.assertIsNone(fs.dump(js.TomlSerializer(), test, self.file_name_toml))
        self.assertEqual(test, fs.load(js.TomlSerializer(), self.file_name_toml))

    def check_fun_other(self, test, *args):
        self.assertEqual(test(*args), fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), test))(*args))
        self.assertIsNone(fs.dump(js.JsonSerializer(), test, self.file_name_json))
        self.assertEqual(test(*args), fs.load(js.JsonSerializer(), self.file_name_json)(*args))

        self.assertEqual(test(*args), fs.loads(js.YamlSerializer(), fs.dumps(js.YamlSerializer(), test))(*args))
        self.assertIsNone(fs.dump(js.YamlSerializer(), test, self.file_name_yaml))
        self.assertEqual(test(*args), fs.load(js.YamlSerializer(), self.file_name_yaml)(*args))

        self.assertEqual(test(*args), fs.loads(js.TomlSerializer(), fs.dumps(js.TomlSerializer(), test))(*args))
        self.assertIsNone(fs.dump(js.TomlSerializer(), test, self.file_name_toml))
        self.assertEqual(test(*args), fs.load(js.TomlSerializer(), self.file_name_toml)(*args))

    def test_convert_between_formats(self):
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.TomlSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), big_boss_fun),
                                           "json", "toml"))(12))
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.YamlSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), big_boss_fun),
                                           "json", "yaml"))(12))
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.JsonSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.TomlSerializer(), big_boss_fun),
                                           "toml", "json"))(12))
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.YamlSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.TomlSerializer(), big_boss_fun),
                                           "toml", "yaml"))(12))
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.TomlSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.YamlSerializer(), big_boss_fun),
                                           "yaml", "toml"))(12))
        self.assertEqual(big_boss_fun(12),
                         fs.loads(js.JsonSerializer(),
                                  fs.dumps(js.JsonSerializer(), fs.dumps(js.YamlSerializer(), big_boss_fun),
                                           "yaml", "json"))(12))

    def test_standart(self):
        self.check_equals(test_int)
        self.check_equals(test_float)
        self.check_equals(test_complex)
        self.check_equals(test_str)
        self.check_equals(test_none)
        self.assertTrue(fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), True)))
        fs.dump(js.JsonSerializer(), True, self.file_name_json)
        self.assertTrue(fs.load(js.JsonSerializer(), self.file_name_json))
        self.assertFalse(fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), False)))
        fs.dump(js.JsonSerializer(), False, self.file_name_json)
        self.assertFalse(fs.load(js.JsonSerializer(), self.file_name_json))
        self.assertEqual(test_int, js.JsonSerializer.
                         factory_deserialize(js.JsonSerializer.factory_serialize(test_int, None, None)))
        self.assertEqual(test_int, js.Deserialize.
                         deserialize_standart(js.Serialize.serialize_standart(test_int)["type"],
                                              js.Serialize.serialize_standart(test_int)["value"]))

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

        self.assertEqual(Puk(1, 2).one, fs.loads(js.YamlSerializer(),
                                                 fs.dumps(js.YamlSerializer(), Puk))(1, 2).one)
        self.assertEqual(Puk(1, 2).two, fs.loads(js.YamlSerializer(),
                                                 fs.dumps(js.YamlSerializer(), Puk))(1, 2).two)
        self.assertEqual(Puk(1, 2).sum(), fs.loads(js.YamlSerializer(),
                                                   fs.dumps(js.YamlSerializer(), Puk))(1, 2).sum())

    def test_convert(self):
        self.assertEqual(test_convert,
                         js.JsonSerializer.convert_str(js.Serialize.serialize({123: 23, 234: 23789}), True))
        self.assertEqual(js.Serialize.serialize({123: 23, 234: 23789}),
                         js.JsonSerializer.convert_str(test_convert, False))


if __name__ == "__main__":
    unittest.main()

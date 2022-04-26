import unittest
import ser_package.factory_serializer as fs
import ser_package.json_ser as js
from test_values import *


class TestJsonSerialize(unittest.TestCase):
    def setUp(self):
        self.file_name = "ser.json"

    def check_equals(self, test):
        self.assertEqual(test, fs.loads(js.JsonSerializer(), fs.dumps(js.JsonSerializer(), test)))
        fs.dump(js.JsonSerializer(), test, self.file_name)
        self.assertEqual(test, fs.load(js.JsonSerializer(), self.file_name))

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
        
    def test_structures(self):
        self.check_equals(test_list)
        self.check_equals(test_tuple)
        self.check_equals(test_bytes)
        self.check_equals(test_bytearray)
        self.check_equals(test_set)
        self.check_equals(test_frozen_set)


if __name__ == "__main__":
    unittest.main()

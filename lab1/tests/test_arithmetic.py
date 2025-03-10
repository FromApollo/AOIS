import unittest
from src.arithmetic import *


class TestAdditionalCodeOperations(unittest.TestCase):
    def test_add_in_additional_code(self):
        self.assertEqual(add_in_additional_code(5, 3), "00001000")
        self.assertEqual(add_in_additional_code(-5, -3), "11111000")
        self.assertEqual(add_in_additional_code(-5, 3), "11111110")
        self.assertEqual(add_in_additional_code(0, 0), "00000000")

    def test_subtract_in_additional_code(self):
        self.assertEqual(subtract_in_additional_code(5, 3), "00000010")
        self.assertEqual(subtract_in_additional_code(-5, -3), "11111110")
        self.assertEqual(subtract_in_additional_code(-5, 3), "11111000")
        self.assertEqual(subtract_in_additional_code(0, 0), "00000000")

    def test_multiply_in_direct_code(self):
        self.assertEqual(multiply_in_direct_code(5, 3), "00001111")
        self.assertEqual(multiply_in_direct_code(-5, 3), "10001111")
        self.assertEqual(multiply_in_direct_code(-5, -3), "00001111")

    def test_add_float(self):
        self.assertEqual(add_float(9.75, 18.5625), "01000001111000101000000000000000")

    def test_divide_direct_code(self):
        self.assertEqual(divide_direct_code(15, 4), "00000011.11000")
        self.assertEqual(divide_direct_code(-101, 7), "10001110.01101")


if __name__ == '__main__':
    unittest.main()

import unittest
from src.conversion import *


class TestConversions(unittest.TestCase):

    def test_decimal_to_binary(self):
        self.assertEqual(decimal_to_binary(5, 7), '0000101')
        self.assertEqual(decimal_to_binary(7, 7), '0000111')
        self.assertEqual(decimal_to_binary(0, 7), '0000000')
        self.assertEqual(decimal_to_binary(127, 7), '1111111')

    def test_to_direct(self):
        self.assertEqual(to_direct(5), '00000101')
        self.assertEqual(to_direct(-5), '10000101')
        self.assertRaises(ValueError, to_direct, 128)
        self.assertRaises(ValueError, to_direct, -129)

    def test_to_inverse(self):
        self.assertEqual(to_inverse(5), '00000101')
        self.assertEqual(to_inverse(-5), '11111010')
        self.assertRaises(ValueError, to_inverse, 128)
        self.assertRaises(ValueError, to_inverse, -129)

    def test_to_additional(self):
        self.assertEqual(to_additional(5), '00000101')
        self.assertEqual(to_additional(-5), '11111011')

    def test_float_to_ieee754(self):
        self.assertEqual(float_to_ieee754(0), '00000000000000000000000000000000')
        self.assertEqual(float_to_ieee754(1), '00111111100000000000000000000000')
        self.assertEqual(float_to_ieee754(3.75), '01000000011100000000000000000000')

    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal('00000101'), 5)
        self.assertEqual(binary_to_decimal('11111111'), 255)
        self.assertEqual(binary_to_decimal('00000000'), 0)

    def test_direct_to_decimal(self):
        self.assertEqual(direct_to_decimal('00000101'), 5)
        self.assertEqual(direct_to_decimal('10000101'), -5)

    def test_fixed_point_to_decimal(self):
        self.assertEqual(fixed_point_to_decimal('00000011.11000', 5), 3.75)
        self.assertEqual(fixed_point_to_decimal('10000011.11000', 5), -3.75)
        self.assertEqual(fixed_point_to_decimal('00000000.00000', 5), 0)

    def test_floating_point_to_decimal(self):
        self.assertEqual(floating_point_to_decimal('01000000011100000000000000000000'), 3.75)

    def test_additional_to_decimal(self):
        self.assertEqual(additional_to_decimal('00000101'), 5)
        self.assertEqual(additional_to_decimal('11111011'), -5)
        self.assertEqual(additional_to_decimal('00000000'), 0)
        self.assertEqual(additional_to_decimal('11111111'), -1)


if __name__ == '__main__':
    unittest.main()

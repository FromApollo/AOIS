import unittest
from src.matrix import *


class TestMatrixOperations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = [
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    def test_read_word(self):
        expected_word = [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
        self.assertEqual(read_word(self.matrix, 0), expected_word)

    def test_logical_functions(self):

        self.assertEqual(f6(0, 0), 0)
        self.assertEqual(f6(0, 1), 1)
        self.assertEqual(f6(1, 0), 1)
        self.assertEqual(f6(1, 1), 0)

        self.assertEqual(f9(0, 0), 1)
        self.assertEqual(f9(0, 1), 0)
        self.assertEqual(f9(1, 0), 0)
        self.assertEqual(f9(1, 1), 1)

        self.assertEqual(f4(0, 0), 0)
        self.assertEqual(f4(0, 1), 1)
        self.assertEqual(f4(1, 0), 0)
        self.assertEqual(f4(1, 1), 0)

        self.assertEqual(f11(0, 0), 1)
        self.assertEqual(f11(0, 1), 0)
        self.assertEqual(f11(1, 0), 1)
        self.assertEqual(f11(1, 1), 1)

    def test_apply_logical_function(self):

        test_matrix = [row.copy() for row in self.matrix]

        apply_logical_function(test_matrix, f6, 0, 1, 2)

        word0 = read_word(self.matrix, 0)
        word1 = read_word(self.matrix, 1)
        expected_word = [f6(word0[i], word1[i]) for i in range(16)]
        self.assertEqual(read_word(test_matrix, 2), expected_word)

    def test_get_set_field(self):
        word = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        self.assertEqual(get_field(word, 0, 3), [1, 0, 1])
        self.assertEqual(get_field(word, 4, 4), [1, 0, 1, 0])

        set_field(word, 4, [0, 1, 0, 1])
        self.assertEqual(word, [1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0])

    def test_process_matrix(self):

        test_matrix = [row.copy() for row in self.matrix]

        process_matrix(test_matrix, "100")

        word14_before = read_word(self.matrix, 14)
        v_bits = get_field(word14_before, 0, 3)
        self.assertEqual(''.join(map(str, v_bits)), "100")

        a_bits = get_field(word14_before, 3, 4)
        b_bits = get_field(word14_before, 7, 4)

        calculated_sum = binary_addition(a_bits, b_bits)

        word14_after = read_word(test_matrix, 14)
        actual_sum = get_field(word14_after, 11, 5)

        self.assertEqual(actual_sum, calculated_sum)

    def test_compare_words(self):
        word1 = [0, 0, 1, 1]
        word2 = [0, 1, 0, 1]

        g, l = compare_words(word1, word2)
        self.assertEqual((g, l), (0, 1))

        g, l = compare_words(word2, word1)
        self.assertEqual((g, l), (1, 0))

        g, l = compare_words(word1, word1)
        self.assertEqual((g, l), (0, 0))

    def test_sort_matrix(self):

        test_matrix = [row.copy() for row in self.matrix]

        sorted_asc = sort_matrix([row.copy() for row in test_matrix], ascending=True)

        words = [read_word(sorted_asc, col) for col in range(16)]
        for i in range(len(words) - 1):
            g, l = compare_words(words[i], words[i + 1])
            self.assertTrue(not g)

        sorted_desc = sort_matrix([row.copy() for row in test_matrix], ascending=False)

        words = [read_word(sorted_desc, col) for col in range(16)]
        for i in range(len(words) - 1):
            g, l = compare_words(words[i], words[i + 1])
            self.assertTrue(not l)


if __name__ == '__main__':
    unittest.main()

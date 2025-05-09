import random
from src.arithmetic import *


def create_matrix():
    return [[random.randint(0, 1) for _ in range(16)] for _ in range(16)]


def read_word(matrix, col_index):
    size = len(matrix)
    shift = col_index
    return [matrix[(i + shift) % size][col_index] for i in range(size)]


def f6(x1, x2):
    return 1 if ((not x1 and x2) or (x1 and not x2)) else 0


def f9(x1, x2):
    return 1 if ((x1 and x2) or (not x1 and not x2)) else 0


def f4(x1, x2):
    return 1 if (not x1 and x2) else 0


def f11(x1, x2):
    return 1 if (x1 or not x2) else 0


def apply_logical_function(matrix, func, word1_col, word2_col, result_col):
    word1 = read_word(matrix, word1_col)
    word2 = read_word(matrix, word2_col)
    result = [func(word1[i], word2[i]) for i in range(len(word1))]

    size = len(matrix)
    shift = result_col
    for i in range(size):
        matrix[(i + shift) % size][result_col] = result[i]


def get_field(word, start, length):
    return word[start:start + length]


def set_field(word, start, new_bits):
    for i in range(len(new_bits)):
        word[start + i] = new_bits[i]


def binary_addition(a_bits, b_bits):
    full_result = add_in_additional_code(a_bits, b_bits, input_in_decimal=False, trim_result=False)
    return [int(bit) for bit in full_result[-5:]]


def process_matrix(matrix, v_key):
    for col in range(len(matrix[0])):
        word = read_word(matrix, col)

        v_bits = get_field(word, 0, 3)
        v_str = ''.join(map(str, v_bits))

        if v_str == v_key:
            a_bits = get_field(word, 3, 4)
            b_bits = get_field(word, 7, 4)
            sum_bits = binary_addition(a_bits, b_bits)
            set_field(word, 11, sum_bits)

            for i in range(16):
                matrix[(i + col) % 16][col] = word[i]


def compare_words(word1, word2):
    g = 0
    l = 0
    for i in range(len(word1)):
        a_i = word1[i]
        s_ji = word2[i]
        g_new = g or (a_i and not s_ji and not l)
        l_new = l or (not a_i and s_ji and not g)
        g, l = g_new, l_new
    return g, l


def sort_matrix(matrix, ascending=True):
    words = [read_word(matrix, col) for col in range(len(matrix[0]))]
    n = len(words)

    for i in range(n):
        for j in range(i + 1, n):
            g, l = compare_words(words[i], words[j])
            if (ascending and g) or (not ascending and l):
                words[i], words[j] = words[j], words[i]

    for col in range(len(matrix[0])):
        word = words[col]
        shift = col
        for row in range(len(matrix)):
            pos = (row + shift) % len(matrix)
            matrix[pos][col] = word[row]

    return matrix


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))


def print_word(word):
    print(" ".join(map(str, word)))

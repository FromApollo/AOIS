import unittest
from src.karnaugh_map import *


class TestLogicSolver(unittest.TestCase):

    def test_is_power_of_two(self):
        self.assertTrue(is_power_of_two(1))
        self.assertTrue(is_power_of_two(2))
        self.assertTrue(is_power_of_two(4))
        self.assertTrue(is_power_of_two(8))
        self.assertTrue(is_power_of_two(16))

        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(3))
        self.assertFalse(is_power_of_two(5))
        self.assertFalse(is_power_of_two(6))
        self.assertFalse(is_power_of_two(7))
        self.assertFalse(is_power_of_two(9))

    def test_get_rectangle_cells(self):

        matrix = [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0]
        ]

        result = get_rectangle_cells(matrix, 0, 1, 2, 3)
        expected = {(0, 1), (0, 2), (0, 3),
                    (1, 1), (1, 2), (1, 3),
                    (2, 1), (2, 2), (2, 3)}
        self.assertEqual(result, expected)

        result = get_rectangle_cells(matrix, 3, 0, 1, 2)
        expected = {(3, 0), (3, 1), (3, 2),
                    (0, 0), (0, 1), (0, 2),
                    (1, 0), (1, 1), (1, 2)}
        self.assertEqual(result, expected)

        result = get_rectangle_cells(matrix, 1, 3, 3, 1)
        expected = {(1, 3), (1, 0), (1, 1),
                    (2, 3), (2, 0), (2, 1),
                    (3, 3), (3, 0), (3, 1)}
        self.assertEqual(result, expected)

        result = get_rectangle_cells(matrix, 3, 3, 1, 1)
        expected = {(3, 3), (3, 0), (3, 1),
                    (0, 3), (0, 0), (0, 1),
                    (1, 3), (1, 0), (1, 1)}
        self.assertEqual(result, expected)

        result = get_rectangle_cells(matrix, 0, 0, 0, 0)
        self.assertEqual(result, {(0, 0)})

    def test_filter_unique_rectangles(self):
        rectangles = [
            ({(0, 0), (0, 1), (1, 0), (1, 1)}, 4),
            ({(0, 0)}, 1),
            ({(1, 1), (1, 2), (2, 1), (2, 2)}, 4),
            ({(0, 0), (0, 1)}, 2)
        ]

        filtered = filter_unique_rectangles(rectangles)
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0][1], 4)
        self.assertEqual(filtered[1][1], 4)

    def test_select_non_overlapping_rectangles(self):
        matrix = [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1]
        ]

        rectangles = [
            ({(0, 0), (0, 1), (1, 0), (1, 1)}, 4),
            ({(0, 0)}, 1),
            ({(2, 2), (2, 3), (3, 2), (3, 3)}, 4),
            ({(0, 0), (0, 1)}, 2)
        ]

        selected = select_non_overlapping_rectangles(matrix, rectangles, "sdnf")
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[0][1], 4)
        self.assertEqual(selected[1][1], 4)

    def test_remove_redundant_rectangles(self):
        matrix = [
            [1, 1, 0],
            [1, 1, 0],
            [0, 0, 1]
        ]

        rectangles = [
            ({(0, 0), (0, 1), (1, 0), (1, 1)}, 4),
            ({(0, 0), (1, 0)}, 2),
            ({(2, 2)}, 1)
        ]

        filtered = remove_redundant_rectangles(matrix, rectangles, "sdnf")
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0][1], 4)
        self.assertEqual(filtered[1][1], 1)

    def test_find_islands_torus(self):
        matrix = [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1]
        ]

        sdnf_islands = find_islands_torus(matrix, "sdnf")
        self.assertGreater(len(sdnf_islands), 0)
        for cells, area in sdnf_islands:
            self.assertTrue(is_power_of_two(area))
            for i, j in cells:
                self.assertEqual(matrix[i][j], 1)

        scnf_islands = find_islands_torus(matrix, "scnf")
        self.assertGreater(len(scnf_islands), 0)
        for cells, area in scnf_islands:
            self.assertTrue(is_power_of_two(area))
            for i, j in cells:
                self.assertEqual(matrix[i][j], 0)

    def test_split_matrix_two_parts(self):
        matrix = [
            [0, 1, 2, 3, 4, 5, 6, 7],
            [8, 9, 10, 11, 12, 13, 14, 15]
        ]

        left, right = split_matrix_two_parts(matrix)
        self.assertEqual(left, [[0, 1, 2, 3], [8, 9, 10, 11]])
        self.assertEqual(right, [[4, 5, 6, 7], [12, 13, 14, 15]])

    def test_mirror_matrix_vertically(self):
        matrix = [
            [0, 1, 2, 3],
            [4, 5, 6, 7]
        ]

        mirrored = mirror_matrix_vertically(matrix)
        self.assertEqual(mirrored, [[3, 2, 1, 0], [7, 6, 5, 4]])

    def test_transform_coords(self):
        groups = [({(0, 0), (1, 1)}, 2), ({(2, 3), (3, 2)}, 2)]
        transformed = transform_coords(groups, 4)
        expected = [({(0, 4), (1, 5)}, 2), ({(2, 7), (3, 6)}, 2)]
        self.assertEqual(transformed, expected)

    def test_add_mirrored_coordinates_to_groups(self):
        groups = [({(0, 0), (0, 1)}, 2), ({(1, 2), (1, 3)}, 2)]
        extended = add_mirrored_coordinates_to_groups(groups)
        expected = [
            ({(0, 0), (0, 1), (0, 6), (0, 7)}, 4),
            ({(1, 2), (1, 3), (1, 4), (1, 5)}, 4)
        ]
        self.assertEqual(extended, expected)

    def test_find_islands_torus_5vars(self):
        matrix = [
            [1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 0],
            [1, 0, 1, 0, 0, 1, 0, 1],
            [0, 1, 0, 1, 1, 0, 1, 0]
        ]

        sdnf_islands = find_islands_torus_5vars(matrix, "sdnf")
        self.assertGreater(len(sdnf_islands), 0)
        for cells, area in sdnf_islands:
            self.assertTrue(is_power_of_two(area))
            for i, j in cells:
                self.assertEqual(matrix[i][j], 1)

        scnf_islands = find_islands_torus_5vars(matrix, "scnf")
        self.assertGreater(len(scnf_islands), 0)
        for cells, area in scnf_islands:
            self.assertTrue(is_power_of_two(area))
            for i, j in cells:
                self.assertEqual(matrix[i][j], 0)

    def test_generate_gray_code(self):
        self.assertEqual(generate_gray_code(0), [0])
        self.assertEqual(generate_gray_code(1), [0, 1])
        self.assertEqual(generate_gray_code(2), [0, 1, 3, 2])
        self.assertEqual(generate_gray_code(3), [0, 1, 3, 2, 6, 7, 5, 4])
        self.assertEqual(len(generate_gray_code(4)), 16)
        self.assertEqual(len(generate_gray_code(5)), 32)


class TestLogicSolverExtended(unittest.TestCase):

    def test_gray_code(self):
        self.assertEqual(gray_code(0), [''])
        self.assertEqual(gray_code(1), ['0', '1'])
        self.assertEqual(gray_code(2), ['00', '01', '11', '10'])
        self.assertEqual(gray_code(3), ['000', '001', '011', '010', '110', '111', '101', '100'])
        self.assertEqual(len(gray_code(4)), 16)

    def test_build_karnaugh_map(self):
        index_form = ['1', '0', '1', '0', '0', '1', '1', '0']
        variables = ['a', 'b', 'c']
        truth_table = [
            [0, 0, 0],
            [0, 0, 1],
            [0, 1, 0],
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 1],
            [1, 1, 0],
            [1, 1, 1]
        ]

        kmap = build_karnaugh_map(index_form, variables, truth_table)
        self.assertEqual(len(kmap), 2)
        self.assertEqual(len(kmap[0]), 4)

        self.assertEqual(kmap[0][0], 1)
        self.assertEqual(kmap[0][1], 0)

    def test_process_formula(self):
        formula = "a|b"
        process_formula(formula)

        formula = "(a&b)|(!c)"
        process_formula(formula)

    def test_add_mirrored_coordinates(self):
        input_groups = [
            ({(1, 2), (3, 4)}, 10)
        ]

        expected_output = [
            ({(1, 2), (3, 4), (1, 5), (3, 3)}, 20)
        ]

        result = add_mirrored_coordinates_to_groups(input_groups)

        self.assertEqual(len(result), len(expected_output))

        for (result_cells, result_area), (expected_cells, expected_area) in zip(result, expected_output):
            self.assertEqual(result_area, expected_area)
            self.assertEqual(result_cells, expected_cells)


if __name__ == '__main__':
    unittest.main()

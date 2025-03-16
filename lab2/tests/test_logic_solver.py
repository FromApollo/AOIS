import unittest
from unittest.mock import patch
from io import StringIO
from src.logic_solver import *


class TestLogicalFunctions(unittest.TestCase):
    def test_binary_to_decimal(self):
        self.assertEqual(binary_to_decimal("0"), 0)
        self.assertEqual(binary_to_decimal("1"), 1)
        self.assertEqual(binary_to_decimal("10"), 2)
        self.assertEqual(binary_to_decimal("101"), 5)

    def test_to_postfix(self):
        self.assertEqual(to_postfix("A+B"), "AB+")
        self.assertEqual(to_postfix("A*B"), "AB*")
        self.assertEqual(to_postfix("(A+B)*C"), "AB+C*")
        self.assertEqual(to_postfix("A>B"), "AB>")
        self.assertEqual(to_postfix("!(A+B)"), "AB+!")

    def test_negation(self):
        self.assertEqual(negation(0), 1)
        self.assertEqual(negation(1), 0)

    def test_conjunction(self):
        self.assertEqual(conjunction(0, 0), 0)
        self.assertEqual(conjunction(0, 1), 0)
        self.assertEqual(conjunction(1, 0), 0)
        self.assertEqual(conjunction(1, 1), 1)

    def test_disjunction(self):
        self.assertEqual(disjunction(0, 0), 0)
        self.assertEqual(disjunction(0, 1), 1)
        self.assertEqual(disjunction(1, 0), 1)
        self.assertEqual(disjunction(1, 1), 1)

    def test_implication(self):
        self.assertEqual(implication(0, 0), 1)
        self.assertEqual(implication(0, 1), 1)
        self.assertEqual(implication(1, 0), 0)
        self.assertEqual(implication(1, 1), 1)

    def test_equivalence(self):
        self.assertEqual(equivalence(0, 0), 1)
        self.assertEqual(equivalence(0, 1), 0)
        self.assertEqual(equivalence(1, 0), 0)
        self.assertEqual(equivalence(1, 1), 1)

    def test_evaluate_postfix(self):
        var_values = {'A': 1, 'B': 0}

        self.assertEqual(evaluate_postfix("AB+", var_values)[-1][1], 1)
        self.assertEqual(evaluate_postfix("AB*", var_values)[-1][1], 0)
        self.assertEqual(evaluate_postfix("A!", {'A': 0})[-1][1], 1)

        self.assertEqual(evaluate_postfix("AB>", var_values)[-1][1], 0)

        self.assertEqual(evaluate_postfix("AB~", var_values)[-1][1], 0)

    def test_generate_truth_table(self):
        self.assertEqual(generate_truth_table(['A']), [(0,), (1,)])
        self.assertEqual(generate_truth_table(['A', 'B']), [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_get_sdnf_sknf(self):
        variables = ['A', 'B']
        truth_table = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1),
        ]
        postfix = "AB+"

        sdnf, sknf = get_sdnf_sknf(variables, truth_table, postfix)

        expected_sdnf = "(!A*B)+(A*!B)+(A*B)"
        expected_sknf = "(A+B)"

        self.assertEqual(sdnf, expected_sdnf)
        self.assertEqual(sknf, expected_sknf)

    def test_get_numeric_forms(self):
        variables = ['A', 'B']
        truth_table = generate_truth_table(variables)
        postfix = "AB+"
        sdnf, sknf = get_numeric_forms(truth_table, postfix, variables)
        self.assertEqual(sdnf, [1, 2, 3])
        self.assertEqual(sknf, [0])

    def test_get_index_form(self):
        variables = ['A', 'B']
        truth_table = generate_truth_table(variables)
        postfix = "AB+"
        self.assertEqual(get_index_form(truth_table, postfix, variables), 7)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_table(self, mock_stdout):
        variables = ['A', 'B']
        truth_table = [(0, 0), (0, 1), (1, 0), (1, 1)]
        postfix_formula = "AB+"

        print_table(variables, truth_table, postfix_formula)

        output = mock_stdout.getvalue()

        expected_output = "0\t0\t0\n0\t1\t1\n1\t0\t1\n1\t1\t1\n"

        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()

from src.calculation_table_method import *

import unittest
from io import StringIO
from contextlib import redirect_stdout


class TestMinimizerFunctions(unittest.TestCase):

    def test_term_to_literal_sdnf(self):
        variables = ['A', 'B', 'C']
        self.assertEqual(term_to_literal('1-0', variables, 'sdnf'), 'A*!C')
        self.assertEqual(term_to_literal('111', variables, 'sdnf'), 'A*B*C')
        self.assertEqual(term_to_literal('---', variables, 'sdnf'), '1')

    def test_term_to_literal_sknf(self):
        variables = ['A', 'B', 'C']
        self.assertEqual(term_to_literal('1-0', variables, 'sknf'), '!A+C')
        self.assertEqual(term_to_literal('111', variables, 'sknf'), '!A+!B+!C')
        self.assertEqual(term_to_literal('---', variables, 'sknf'), '1')

    def test_print_minimization_table_sdnf(self):
        variables = ['A', 'B']
        implicants = ['1-', '0-']
        terms = [('10', 1), ('11', 1), ('00', 1)]

        buffer = StringIO()
        with redirect_stdout(buffer):
            print_minimization_table(implicants, terms, variables, mode='sdnf')
        output = buffer.getvalue()
        self.assertIn("Минимальная ДНФ:", output)
        self.assertIn("(A)", output)
        self.assertIn("(!A)", output)

    def test_print_minimization_table_sknf(self):
        variables = ['A', 'B']
        implicants = ['1-', '0-']
        terms = [('10', 0), ('11', 0), ('00', 0)]

        buffer = StringIO()
        with redirect_stdout(buffer):
            print_minimization_table(implicants, terms, variables, mode='sknf')
        output = buffer.getvalue()

        self.assertIn("Минимальная КНФ:", output)
        self.assertIn("(!A)", output)
        self.assertIn("(A)", output)


if __name__ == '__main__':
    unittest.main()

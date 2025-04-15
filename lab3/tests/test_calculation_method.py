import unittest
from unittest.mock import patch
from src.calculation_method import *


class TestLogicMinimizer(unittest.TestCase):

    def test_combine_terms(self):
        self.assertEqual(combine_terms("1100", "1000"), "1-00")
        self.assertEqual(combine_terms("1100", "1101"), "110-")
        self.assertEqual(combine_terms("1100", "1110"), "11-0")
        self.assertEqual(combine_terms("1100", "1100"), None)

    def test_format_terms(self):
        variables = ['a', 'b', 'c']
        self.assertEqual(format_sdnf_term("101", variables), "(a * !b * c)")
        self.assertEqual(format_scnf_term("101", variables), "(!a + b + !c)")

    def test_get_minterms_and_maxterms(self):
        implicant = "1-0"
        variables = ['a', 'b', 'c']
        self.assertEqual(sorted(get_minterms(implicant, variables)), ['100', '110'])
        self.assertEqual(sorted(get_maxterms(implicant, variables)), ['100', '110'])

    def test_covers_minterm_and_maxterm(self):
        self.assertTrue(covers_minterm("1-0", "100"))
        self.assertTrue(covers_minterm("1-0", "110"))
        self.assertFalse(covers_minterm("1-0", "111"))

        self.assertTrue(covers_maxterm("1-0", "100"))
        self.assertTrue(covers_maxterm("1-0", "110"))
        self.assertFalse(covers_maxterm("1-0", "111"))

    def test_remove_redundant_implicants_sdnf(self):
        implicants = ["1-0", "110"]
        variables = ['a', 'b', 'c']
        reduced = remove_redundant_implicants_sdnf(implicants, variables)
        self.assertEqual(reduced, ["1-0"])

    def test_remove_redundant_implicants_scnf(self):
        implicants = ["1-0", "110"]
        variables = ['a', 'b', 'c']
        reduced = remove_redundant_implicants_scnf(implicants, variables)
        self.assertEqual(reduced, ["1-0"])

    def test_remove_redundant_implicants_dispatch(self):
        implicants = ["1-0", "110"]
        variables = ['a', 'b', 'c']
        self.assertEqual(remove_redundant_implicants(implicants, variables, 'sdnf'), ["1-0"])
        self.assertEqual(remove_redundant_implicants(implicants, variables, 'scnf'), ["1-0"])

    def test_minimize_logic_function(self):
        terms = [("1100", 0), ("1000", 1)]
        variables = ['a', 'b', 'c', 'd']
        result = minimize_logic_function(terms, variables, 'sdnf')
        self.assertIn("1-00", result)

    @patch('src.calculation_method.evaluate_postfix')
    def test_generate_sdnf_scnf_terms(self, mock_eval):
        variables = ['a', 'b']
        truth_table = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
        ]
        postfix_formula = 'ab+'

        mock_eval.side_effect = [
            [('', 0)],
            [('', 1)],
            [('', 1)],
            [('', 0)],
        ]

        sdnf, scnf = generate_sdnf_scnf_terms(truth_table, postfix_formula, variables)

        self.assertEqual(sdnf, [('01', 1), ('10', 2)])
        self.assertEqual(scnf, [('00', 0), ('11', 3)])


if __name__ == '__main__':
    unittest.main()

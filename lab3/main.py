from src.calculation_table_method import *
from src.karnaugh_map import *
from src.calculation_method import *


def calculation_method():
    formula = "(a>b)*!c+(d~e>a)"
    variables = sorted(set(c for c in formula if c.isalnum()))

    postfix = to_postfix(formula)
    truth_table = generate_truth_table(variables)

    sdnf_terms, scnf_terms = generate_sdnf_scnf_terms(truth_table, postfix, variables)

    prime_implicants = minimize_logic_function(sdnf_terms, variables, mode='sdnf')

    minimized_sdnf = remove_redundant_implicants(prime_implicants, variables, mode='sdnf')

    print("\nМинимизированная ДНФ после удаления лишних импликант:")
    print(" + ".join(format_sdnf_term(t, variables) for t in minimized_sdnf))

    print("=======================================================================================================")

    prime_scnf = minimize_logic_function(scnf_terms, variables, mode='scnf')
    minimized_scnf = remove_redundant_implicants(prime_scnf, variables, mode='scnf')

    print("\nМинимизированная КНФ после удаления лишних импликант:")
    print(" * ".join(format_scnf_term(t, variables) for t in minimized_scnf))


def calculation_table_method():
    formula = "(a>b)*!c+(d~e>a)"

    variables = sorted(set(c for c in formula if c.isalnum()))

    postfix = to_postfix(formula)
    truth_table = generate_truth_table(variables)

    sdnf_terms, scnf_terms = generate_sdnf_scnf_terms(truth_table, postfix, variables)

    print("\n============================================")
    prime_sdnf = minimize_logic_function(sdnf_terms, variables, mode='sdnf')
    print('\n')
    print("Таблица для СДНФ: ")
    print_minimization_table(prime_sdnf, sdnf_terms, variables, mode='sdnf')

    print("\n============================================")
    prime_scnf = minimize_logic_function(scnf_terms, variables, mode='scnf')
    print('\n')
    print("Таблица для СКНФ: ")
    print_minimization_table(prime_scnf, scnf_terms, variables, mode='scnf')


def karnaugh_map_method():
    formula = "(a>b)*!c+(d~e>a)"
    process_formula(formula)


if __name__ == '__main__':
    calculation_method()
    calculation_table_method()
    karnaugh_map_method()

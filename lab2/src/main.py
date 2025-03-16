from src.logic_solver import *


def main():
    print("! - отрицание ¬")
    print("* - конъюнкция ∧")
    print("+ - дизъюнкция ∨")
    print("> - импликация →")
    print("~ - эквиваленция ↔")
    print("\n")

    formula = "a+(!b>c)*d~e"
    print(f"Формула: {formula}")
    print("\n")

    postfix_formula = to_postfix(formula)
    variables = sorted(set(c for c in formula if c.isalnum()))
    truth_table = generate_truth_table(variables)

    print("Таблица истинности: ")
    print_table(variables, truth_table, postfix_formula)
    print("\n")

    numeric_form_sdnf, numeric_form_sknf = get_numeric_forms(truth_table, postfix_formula, variables)
    print(f"Числовая форма СДНФ: {numeric_form_sdnf}")
    print(f"Числовая форма СKНФ: {numeric_form_sknf}")
    print("\n")

    index_form = get_index_form(truth_table, postfix_formula, variables)
    print(f"Индексная форма в десятичном представлении: {index_form}")
    print("\n")

    sdnf, sknf = get_sdnf_sknf(variables, truth_table, postfix_formula)
    print(f"СДНФ: {sdnf}")
    print(f"СКНФ: {sknf}")


if __name__ == "__main__":
    main()

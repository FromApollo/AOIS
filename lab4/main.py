from src.karnaugh_map import *

ODS_3_truth_table = [
    # A, B, C, S, P
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

D8421_plus_9_truth_table = [
    # A, B, C, D, A', B', C', D'
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 1],
    [0, 0, 1, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 1],
    [0, 1, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 0],
    [1, 0, 1, 0, 1, 0, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0, 0]
]


def print_truth_table(table):
    print("Таблица истинности ODS-3:")
    print("A B C | S P")
    print("------|---")
    for row in table:
        print(f"{row[0]} {row[1]} {row[2]} | {row[3]} {row[4]}")


print_truth_table(ODS_3_truth_table)

matrix_S = [row[:3] + [row[3]] for row in ODS_3_truth_table]
matrix_P = [row[:3] + [row[4]] for row in ODS_3_truth_table]


def build_kmap_3vars(truth_table):
    kmap = [[0, 0, 0, 0],
            [0, 0, 0, 0]]

    for row in truth_table:
        a, b, c, val = row
        if a == 0:
            if b == 0 and c == 0:
                kmap[0][0] = val
            elif b == 0 and c == 1:
                kmap[0][1] = val
            elif b == 1 and c == 1:
                kmap[0][2] = val
            elif b == 1 and c == 0:
                kmap[0][3] = val
        else:
            if b == 0 and c == 0:
                kmap[1][0] = val
            elif b == 0 and c == 1:
                kmap[1][1] = val
            elif b == 1 and c == 1:
                kmap[1][2] = val
            elif b == 1 and c == 0:
                kmap[1][3] = val
    return kmap


kmap_S = build_kmap_3vars(matrix_S)
kmap_P = build_kmap_3vars(matrix_P)

variables = ['A', 'B', 'C']

print("\nМинимизация СДНФ для выхода S (сумма):")
minimized_S = get_boolean_expression(kmap_S, variables, mode="sdnf")
print(minimized_S)

print("\nМинимизация СДНФ для выхода P (перенос):")
minimized_P = get_boolean_expression(kmap_P, variables, mode="sdnf")
print(minimized_P)

print("====================================================================")


def print_d8421_truth_table(table):
    print("Таблица истинности D8421+1:")
    print("A B C D | A' B' C' D'")
    print("--------|------------")
    for row in table:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]} | {row[4]} {row[5]} {row[6]} {row[7]}")


print_d8421_truth_table(D8421_plus_9_truth_table)


def build_kmap_4vars(truth_table, output_index):
    kmap = [[0 for _ in range(4)] for _ in range(4)]

    for row in truth_table:
        a, b, c, d = row[:4]
        val = row[4 + output_index]

        row_index = (a << 1) | b
        if row_index == 3:
            row_index = 2
        elif row_index == 2:
            row_index = 3

        col_index = (c << 1) | d
        if col_index == 3:
            col_index = 2
        elif col_index == 2:
            col_index = 3

        kmap[row_index][col_index] = val
    return kmap


kmap_Ap = build_kmap_4vars(D8421_plus_9_truth_table, 0)
kmap_Bp = build_kmap_4vars(D8421_plus_9_truth_table, 1)
kmap_Cp = build_kmap_4vars(D8421_plus_9_truth_table, 2)
kmap_Dp = build_kmap_4vars(D8421_plus_9_truth_table, 3)

variables4 = ['A', 'B', 'C', 'D']

print("\nМинимизация A':")
print(f'ДНФ: {get_boolean_expression(kmap_Ap, variables4, mode="sdnf")}')

print("\nМинимизация B':")
print(f'ДНФ: {get_boolean_expression(kmap_Bp, variables4, mode="sdnf")}')

print("\nМинимизация C':")
print(f'ДНФ: {get_boolean_expression(kmap_Cp, variables4, mode="sdnf")}')

print("\nМинимизация D':")
print(f'ДНФ: {get_boolean_expression(kmap_Dp, variables4, mode="sdnf")}')

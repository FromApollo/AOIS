def term_to_literal(term, variables, mode='sdnf'):
    parts = []
    for i, val in enumerate(term):
        if val == '-':
            continue
        if mode == 'sdnf':
            if val == '1':
                parts.append(variables[i])
            elif val == '0':
                parts.append(f"!{variables[i]}")
        else:
            if val == '1':
                parts.append(f"!{variables[i]}")
            elif val == '0':
                parts.append(variables[i])
    if mode == 'sdnf':
        return '*'.join(parts) if parts else '1'
    else:
        return '+'.join(parts) if parts else '1'


def print_minimization_table(implicants, terms, variables, mode='sdnf'):
    headers = [''] + [term_to_literal(t, variables, mode) for t, _ in terms]

    col_widths = [max(len(h) for h in headers)]
    for i in range(1, len(headers)):
        width = max(len(headers[i]), max(len(term_to_literal(imp, variables, mode)) for imp in implicants))
        col_widths.append(width)

    for i, h in enumerate(headers):
        print(h.ljust(col_widths[i]), end=' | ')
    print()

    for w in col_widths:
        print('-' * w, end=' | ')
    print()

    matrix = []
    for imp in implicants:
        row = [term_to_literal(imp, variables, mode)]
        covered = []
        for term, _ in terms:
            match = True
            for i in range(len(term)):
                if imp[i] != '-' and imp[i] != term[i]:
                    match = False
                    break
            if match:
                row.append('X')
                covered.append(True)
            else:
                row.append(' ')
                covered.append(False)
        matrix.append((row, covered))

    for row, _ in matrix:
        for i, val in enumerate(row):
            print(val.ljust(col_widths[i]), end=' | ')
        print()

    essentials = set()
    for col in range(len(terms)):
        count = 0
        last_idx = -1
        for i, (_, coverage) in enumerate(matrix):
            if coverage[col]:
                count += 1
                last_idx = i
        if count == 1:
            essentials.add(matrix[last_idx][0][0])

    result_terms = []
    for imp in implicants:
        if term_to_literal(imp, variables, mode) in essentials:
            result_terms.append(term_to_literal(imp, variables, mode))

    if mode == 'sdnf':
        result = " + ".join([f"({t})" for t in result_terms])
        print("\nМинимальная ДНФ:", result)
    else:
        result = " * ".join([f"({t})" for t in result_terms])
        print("\nМинимальная КНФ:", result)

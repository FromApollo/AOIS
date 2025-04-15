from src.logic_solver import *


def combine_terms(term1, term2):
    diff = 0
    result = []
    for a, b in zip(term1, term2):
        if a != b:
            if a != '-' and b != '-':
                diff += 1
                result.append('-')
            else:
                return None
        else:
            result.append(a)
    if diff == 1:
        return ''.join(result)
    return None


def generate_sdnf_scnf_terms(truth_table, postfix_formula, variables):
    sdnf_terms = []
    scnf_terms = []
    for idx, values in enumerate(truth_table):
        var_values = dict(zip(variables, values))
        result = evaluate_postfix(postfix_formula, var_values)[-1][1]
        binary = ''.join(str(x) for x in values)
        if result == 1:
            sdnf_terms.append((binary, idx))
        else:
            scnf_terms.append((binary, idx))
    return sdnf_terms, scnf_terms


def combine_all_terms(terms, variables, mode):
    stage = 1
    all_prime_implicants = []

    term_to_str = format_sdnf_term if mode == 'sdnf' else format_scnf_term
    op_symbol = '+' if mode == 'sdnf' else '*'

    while True:
        grouped = {}
        for term, idx in terms:
            ones = term.count('1')
            grouped.setdefault(ones, []).append((term, idx))

        new_terms = []
        used_pairs = set()
        grouped_keys = sorted(grouped.keys())
        combined_in_this_stage = set()

        for i in range(len(grouped_keys) - 1):
            group1 = grouped[grouped_keys[i]]
            group2 = grouped[grouped_keys[i + 1]]
            for (term1, idx1) in group1:
                for (term2, idx2) in group2:
                    combined = combine_terms(term1, term2)
                    if combined:
                        new_terms.append((combined, (idx1, idx2)))
                        used_pairs.add(term1)
                        used_pairs.add(term2)
                        combined_in_this_stage.add(combined)

        if combined_in_this_stage:
            not_used = {term for term, _ in terms if term not in used_pairs}
            all_terms_this_stage = combined_in_this_stage.union(not_used)

            result_str = f"{stage}-ый этап: " + f" {op_symbol} ".join(
                [term_to_str(term, variables) for term in sorted(all_terms_this_stage)]
            )
            print(result_str)
            stage += 1

        for term, idx in terms:
            if term not in used_pairs:
                all_prime_implicants.append((term, idx))

        if not new_terms:
            break

        terms = list({t: idx for t, idx in new_terms}.items())

    return all_prime_implicants


def remove_redundant_implicants_sdnf(implicants, variables):
    redundant_indices = set()

    for i in range(len(implicants)):

        other_implicants = [imp for j, imp in enumerate(implicants) if j != i]

        is_redundant = True
        for minterm in get_minterms(implicants[i], variables):
            covered = False
            for imp in other_implicants:
                if covers_minterm(imp, minterm):
                    covered = True
                    break
            if not covered:
                is_redundant = False
                break

        if is_redundant:
            redundant_indices.add(i)

    return [imp for j, imp in enumerate(implicants) if j not in redundant_indices]


def remove_redundant_implicants_scnf(implicants, variables):
    redundant_indices = set()

    for i in range(len(implicants)):

        other_implicants = [imp for j, imp in enumerate(implicants) if j != i]

        is_redundant = True
        for maxterm in get_maxterms(implicants[i], variables):
            covered = False
            for imp in other_implicants:
                if covers_maxterm(imp, maxterm):
                    covered = True
                    break
            if not covered:
                is_redundant = False
                break

        if is_redundant:
            redundant_indices.add(i)

    return [imp for j, imp in enumerate(implicants) if j not in redundant_indices]


def get_minterms(implicant, variables):
    minterms = []
    dashes = [i for i, c in enumerate(implicant) if c == '-']

    from itertools import product
    for combo in product(['0', '1'], repeat=len(dashes)):
        minterm = list(implicant)
        for pos, val in zip(dashes, combo):
            minterm[pos] = val
        minterms.append(''.join(minterm))

    return minterms


def get_maxterms(implicant, variables):
    maxterms = []
    dashes = [i for i, c in enumerate(implicant) if c == '-']

    from itertools import product
    for combo in product(['0', '1'], repeat=len(dashes)):
        maxterm = list(implicant)
        for pos, val in zip(dashes, combo):
            maxterm[pos] = val
        maxterms.append(''.join(maxterm))

    return maxterms


def covers_minterm(implicant, minterm):
    for imp_bit, min_bit in zip(implicant, minterm):
        if imp_bit != '-' and imp_bit != min_bit:
            return False
    return True


def covers_maxterm(implicant, maxterm):
    for imp_bit, max_bit in zip(implicant, maxterm):
        if imp_bit != '-' and imp_bit != max_bit:
            return False
    return True


def format_sdnf_term(term, variables):
    result = []
    for bit, var in zip(term, variables):
        if bit == '1':
            result.append(var)
        elif bit == '0':
            result.append(f"!{var}")
    return '(' + ' * '.join(result) + ')'


def format_scnf_term(term, variables):
    result = []
    for bit, var in zip(term, variables):
        if bit == '0':
            result.append(var)
        elif bit == '1':
            result.append(f"!{var}")
    return '(' + ' + '.join(result) + ')'


def remove_redundant_implicants(prime_implicants, variables, mode):
    if mode == 'sdnf':
        return remove_redundant_implicants_sdnf(prime_implicants, variables)
    else:
        return remove_redundant_implicants_scnf(prime_implicants, variables)


def minimize_logic_function(terms, variables, mode):
    all_prime_implicants = combine_all_terms(terms, variables, mode)
    return [term for term, _ in all_prime_implicants]

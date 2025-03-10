from src.conversion import *


def add_in_additional_code(num1, num2, bit_width=BIT_WIDTH, input_in_decimal=True, trim_result=True):
    if input_in_decimal:
        code1 = [int(bit) for bit in to_additional(num1)]
        code2 = [int(bit) for bit in to_additional(num2)]
    else:
        code1 = [int(bit) for bit in num1]
        code2 = [int(bit) for bit in num2]

    max_length = max(len(code1), len(code2), bit_width)
    result_bits = []
    carry = 0

    for i in range(1, max_length + 1):
        bit1 = code1[-i] if i <= len(code1) else 0
        bit2 = code2[-i] if i <= len(code2) else 0

        total = bit1 + bit2 + carry
        result_bits.append(total % 2)
        carry = total // 2

    while carry:
        result_bits.append(carry % 2)
        carry //= 2

        if trim_result:
            result_bits = result_bits[:bit_width]

    result_bits.reverse()

    return ''.join(map(str, result_bits))


def subtract_in_additional_code(num1, num2):
    return add_in_additional_code(num1, -num2)


def multiply_in_direct_code(num1, num2):
    if not (MIN_INT <= num1 <= MAX_INT and MIN_INT <= num2 <= MAX_INT):
        raise ValueError("Число выходит за 8-битный диапазон")

    direct1 = to_direct(abs(num1))
    direct2 = to_direct(abs(num2))

    bits1 = [int(bit) for bit in direct1]
    bits2 = [int(bit) for bit in direct2]

    partial_results = []

    for bit2 in reversed(bits2):
        partial = [bit2 * bit for bit in bits1]
        partial_str = "".join(map(str, partial))
        partial_results.append(partial_str)

    sum_bits = [int(bit) for bit in partial_results[0]]

    for i in range(1, len(partial_results)):
        shifted = partial_results[i] + "0" * i
        shifted = shifted[i:]
        for j in range(len(sum_bits) - 1, -1, -1):
            total = sum_bits[j] + int(shifted[j])
            sum_bits[j] = total % 2
            if total > 1 and j > 0:
                sum_bits[j - 1] += total // 2

    result_bits = ''.join(map(str, sum_bits))

    if (num1 >= 0 > num2) or (num1 < 0 <= num2):
        result_bits = '1' + result_bits[1:]

    return result_bits


def add_float(num1, num2):
    float_num1 = float_to_ieee754(num1)
    float_num2 = float_to_ieee754(num2)

    exp1 = binary_to_decimal(float_num1[1:EXP_BITS + 1]) - EXP_BIAS
    exp2 = binary_to_decimal(float_num2[1:EXP_BITS + 1]) - EXP_BIAS

    mantissa1 = "1" + float_num1[EXP_BITS + 1:]
    mantissa2 = "1" + float_num2[EXP_BITS + 1:]

    if exp1 > exp2:
        exp_res = exp1
        exp_shift = exp1 - exp2
        mantissa2 = "0" * exp_shift + mantissa2
    else:
        exp_res = exp2
        exp_shift = exp2 - exp1
        mantissa1 = "0" * exp_shift + mantissa1

    mantissa1 = mantissa1[:MANTISSA_BITS + 1]
    mantissa2 = mantissa2[:MANTISSA_BITS + 1]

    mantissa_sum = add_in_additional_code(mantissa1, mantissa2, MANTISSA_BITS + 1, False, False)

    if len(mantissa_sum) > MANTISSA_BITS:
        exp_shifted_part = mantissa_sum[:-MANTISSA_BITS]
        exp_shift = 0

        while len(exp_shifted_part) > 1:
            exp_shifted_part = exp_shifted_part[:-1]
            exp_shift += 1

    exp_res += exp_shift

    if mantissa_sum[0] == "1":
        mantissa_sum = mantissa_sum[1:MANTISSA_BITS + 2]

    exp_final = decimal_to_binary(exp_res + EXP_BIAS, EXP_BITS)

    return "0" + exp_final + mantissa_sum[:MANTISSA_BITS]


def divide_direct_code(dividend, divisor, precision=5):
    result = []
    is_negative_res = False
    if (dividend >= 0 > divisor) or (dividend < 0 <= divisor):
        is_negative_res = True

    dividend = abs(dividend)
    divisor = abs(divisor)

    if divisor == 0:
        raise ZeroDivisionError("Деление на ноль невозможно")

    dividend_bin = decimal_to_binary(dividend, BIT_WIDTH)
    divisor_bin = decimal_to_binary(divisor, BIT_WIDTH)

    quotient = ''
    remainder = ''
    for bit in dividend_bin:
        remainder += bit

        if binary_to_decimal(remainder) >= binary_to_decimal(divisor_bin):
            quotient += '1'
            remainder = subtract_in_additional_code(
                direct_to_decimal(remainder.zfill(BIT_WIDTH)),
                direct_to_decimal(divisor_bin.zfill(BIT_WIDTH))
            ).lstrip('0')
        else:
            quotient += '0'

    quotient = quotient[1:]
    quotient = quotient.zfill(BIT_WIDTH - 1)
    result.append(quotient)
    result.append('.')

    fractional_part = ''
    for _ in range(precision):
        remainder += '0'
        if binary_to_decimal(remainder) >= binary_to_decimal(divisor_bin):
            fractional_part += '1'
            remainder = subtract_in_additional_code(
                direct_to_decimal(remainder.zfill(BIT_WIDTH)),
                direct_to_decimal(divisor_bin.zfill(BIT_WIDTH))
            ).lstrip('0')
        else:
            fractional_part += '0'

    result.append(fractional_part)

    result.insert(0, '1' if is_negative_res else '0')

    return ''.join(result)

from src.globals import *


def decimal_to_binary(num, bits=7):
    binary = []
    for _ in range(bits):
        binary.append(str(num % 2))
        num //= 2
    return ''.join(reversed(binary))


def to_direct(num):
    if not (MIN_INT <= num <= MAX_INT):
        raise ValueError("Число выходит за 8-битный диапазон")

    sign_bit = '1' if num < 0 else '0'

    abs_value = abs(num)
    bin_value = decimal_to_binary(abs_value)

    return sign_bit + bin_value


def to_inverse(num):
    if not (MIN_INT <= num <= MAX_INT):
        raise ValueError("Число выходит за 8-битный диапазон")

    sign_bit = '1' if num < 0 else '0'

    abs_value = abs(num)
    bin_value = decimal_to_binary(abs_value)

    if num >= 0:
        return sign_bit + bin_value

    inverse_bin = ''.join('1' if bit == '0' else '0' for bit in bin_value)

    return sign_bit + inverse_bin


def to_additional(num):
    sign_bit = '1' if num < 0 else '0'

    abs_value = abs(num)
    bin_value = decimal_to_binary(abs_value, BIT_WIDTH - 1)

    if num >= 0:
        return sign_bit + bin_value

    inverse_bin = ''.join('1' if bit == '0' else '0' for bit in bin_value)
    add_code = list(inverse_bin)

    carry = 1
    for i in range(BIT_WIDTH - 2, -1, -1):
        if add_code[i] == '1' and carry == 1:
            add_code[i] = '0'
        elif add_code[i] == '0' and carry == 1:
            add_code[i] = '1'
            break

    return sign_bit + ''.join(add_code)


def float_to_ieee754(num):
    if num == 0:
        return '0' * IEEE_TOTAL_BITS

    exp = 0
    mantissa = num
    while mantissa >= 2:
        mantissa /= 2
        exp += 1
    while mantissa < 1:
        mantissa *= 2
        exp -= 1

    exp = exp + EXP_BIAS
    exp_bits = decimal_to_binary(exp, EXP_BITS)

    frac = mantissa - 1
    frac_bits = ""
    for _ in range(MANTISSA_BITS):
        frac *= 2
        if frac >= 1:
            frac_bits += '1'
            frac -= 1
        else:
            frac_bits += '0'

    return '0' + exp_bits + frac_bits


def binary_to_decimal(binary_str):
    decimal = 0
    for i, bit in enumerate(reversed(binary_str)):
        decimal += int(bit) * (2 ** i)
    return decimal


def direct_to_decimal(binary_str):
    sign = -1 if binary_str[0] == '1' else 1
    magnitude = binary_to_decimal(binary_str[1:])
    return sign * magnitude


def fixed_point_to_decimal(binary_str, frac_bits=5):
    sign = -1 if binary_str[0] == '1' else 1
    binary_str = binary_str[1:]
    int_part_str, frac_part_str = binary_str.split('.')
    int_part = binary_to_decimal(int_part_str)
    frac_part = sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(frac_part_str[:frac_bits]))
    return sign * (int_part + frac_part)


def floating_point_to_decimal(binary_str):
    sign = -1 if binary_str[0] == '1' else 1
    exponent_raw = binary_to_decimal(binary_str[1:1 + EXP_BITS])
    exponent = exponent_raw - (2 ** (EXP_BITS - 1) - 1)
    mantissa = 1 + sum(int(bit) * (2 ** -(i + 1)) for i, bit in enumerate(binary_str[1 + EXP_BITS:]))
    return sign * mantissa * (2 ** exponent)


def additional_to_decimal(binary_str):
    if binary_str[0] == '1':
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary_str)
        magnitude = binary_to_decimal(inverted) + 1
        return -magnitude
    return binary_to_decimal(binary_str)

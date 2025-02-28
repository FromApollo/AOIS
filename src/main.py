from arithmetic import *

print("1-ое задание -------------------------------")
print("\n")
num = -4
print(f"Число: {num}")
direct = to_direct(num)
inverse = to_inverse(num)
additional = to_additional(num)
print(f"Прямой код: {direct}")
print(f"Обратный код: {inverse}")
print(f"Дополнительный код: {additional}")

print('\n')
print("2 ое задание -------------------------------")
print("\n")
n1 = 12
n2 = 5
result_binary = add_in_additional_code(n1, n2)
print(f"Сложение чисел {n1} и {n2} в дополнительном коде:")
print(f"Результат в дополнительном коде: {result_binary}")
decimal = additional_to_decimal(result_binary)
print(f"Результат в десятичном виде: {decimal}")

print("\n")
print("3 ее задание -------------------------------")
print("\n")
n1 = 6
n2 = 12
result_binary = subtract_in_additional_code(n1, n2)
print(f"Вычитание чисел {n1} и {n2}:")
print(f"Результат в дополнительном коде: {result_binary}")
decimal = additional_to_decimal(result_binary)
print(f"Результат в десятичном виде: {decimal}")

print("\n")
print("4 ое задание -------------------------------")
print("\n")
n1 = 15
n2 = -2
result_direct = multiply_in_direct_code(n1, n2)
print(f"Произведение чисел {n1} и {n2} в прямом коде: {result_direct}")
decimal = direct_to_decimal(result_direct)
print(f"В десятичном виде: {decimal}")
print("\n")

print("5 ое задание -------------------------------")
print("\n")
n1 = 15
n2 = 4
result = divide_direct_code(n1, n2, precision=5)
print(f"Деление чисел {n1} и {n2}: {result}")
decimal = fixed_point_to_decimal(result)
print(f"В десятичном: {decimal}")

print("\n")
print("6 ое задание -------------------------------")
print("\n")
n1 = 9.75
n2 = 18.5625
result = add_float(n1, n2)
print(f"Сложение ПОЛОЖИТЕЛЬНЫХ чисел {n1} и {n2}: \n{result}")
decimal = floating_point_to_decimal(result)
print(f"В десятичном виде: {decimal}")

print("\n")
print("7 ое задание -------------------------------")
print("\n")
print(additional_to_decimal("11111000"))  # -8
print(direct_to_decimal("00001001"))  # 9
print(fixed_point_to_decimal("10000011.11000", 5))  # -3.75
print(floating_point_to_decimal("00111111010011001100110011001100"))  # примерно 0.8
print(floating_point_to_decimal("01000001111000101000000000000000"))  # 28.3125

from src.matrix import *


def main():
    matrix = None
    while True:
        print("\nМеню:")
        print("1. Создать новую матрицу")
        print("2. Вывести матрицу")
        print("3. Прочитать слово по номеру столбца")
        print("4. Применить логическую функцию к словам")
        print("5. Выполнить арифметическую операцию (сложение Aj и Bj)")
        print("6. Отсортировать матрицу")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            matrix = create_matrix()
            print("Матрица создана:")
            print_matrix(matrix)

        elif choice == "2":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                print("Текущая матрица:")
                print_matrix(matrix)

        elif choice == "3":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                col = int(input("Введите номер столбца (0-15): "))
                if 0 <= col < 16:
                    word = read_word(matrix, col)
                    print(f"Слово в столбце {col}:")
                    print_word(word)
                else:
                    print("Некорректный номер столбца.")

        elif choice == "4":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                print("Доступные логические функции:")
                print("6: !x1 * x2 + x1 * !x2 (f6)")
                print("9: x1 * x2 + !x1 * !x2 (f9)")
                print("4: !x1 * x2 (f4)")
                print("11: x1 + !x2 (f11)")
                func_choice = input("Выберите функцию (6, 9, 4, 11): ")
                func_map = {"6": f6, "9": f9, "4": f4, "11": f11}
                if func_choice in func_map:
                    word1_col = int(input("Введите номер первого столбца (0-15): "))
                    word2_col = int(input("Введите номер второго столбца (0-15): "))
                    result_col = int(input("Введите номер столбца для записи результата (0-15): "))
                    if all(0 <= col < 16 for col in (word1_col, word2_col, result_col)):
                        apply_logical_function(matrix, func_map[func_choice], word1_col, word2_col, result_col)
                        print("Результат записан в матрицу.")
                        print_matrix(matrix)
                    else:
                        print("Некорректные номера столбцов.")
                else:
                    print("Некорректный выбор функции.")

        elif choice == "5":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                v_key = input("Введите ключ V (3 бита, например '111'): ")
                if len(v_key) == 3 and all(c in "01" for c in v_key):
                    process_matrix(matrix, v_key)
                    print("Арифметическая операция выполнена.")
                    print_matrix(matrix)
                else:
                    print("Некорректный ключ. Введите 3 бита (0 или 1).")

        elif choice == "6":
            if matrix is None:
                print("Матрица не создана. Сначала создайте матрицу.")
            else:
                order = input("Сортировать по возрастанию? (да/нет): ").lower()
                ascending = order.startswith("д") or order.startswith("н")
                sort_matrix(matrix, ascending)
                print("Матрица отсортирована.")
                print_matrix(matrix)

        elif choice == "7":
            print("Выход из программы.")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()

from src.hash_table import *


def main():
    ht = HashTable()

    math_terms = {
        "МАТРИЦА": "Таблица чисел",
        "ВЕКТОР": "Направленный отрезок",
        "СКАЛЯР": "Обычное число",
        "ГРАФ": "Набор вершин и рёбер",
        "ИНТЕГРАЛ": "Площадь под кривой",
        "ЛОГАРИФМ": "Степень, в которую нужно возвести основание",
        "ПРОИЗВОДНАЯ": "Скорость изменения функции",
        "УРАВНЕНИЕ": "Равенство с переменными",
        "ФУНКЦИЯ": "Зависимость одной величины от другой",
        "ДИСПЕРСИЯ": "Среднеквадратичное отклонение"
    }

    for key, val in math_terms.items():
        ht.insert(key, val)

    while True:
        print("\nМеню:")
        print("1. Добавить элемент")
        print("2. Найти элемент")
        print("3. Удалить элемент")
        print("4. Обновить элемент")
        print("5. Показать всю таблицу")
        print("6. Показать коэффициент заполнения")
        print("7. Выход")

        choice = input("Выберите пункт: ")

        if choice == '1':
            key = input("Введите ключ (термин): ")
            value = input("Введите значение (определение): ")
            ht.insert(key, value)
        elif choice == '2':
            key = input("Введите ключ для поиска: ")
            result = ht.search(key)
            print(f"Результат: {result}" if result else "Элемент не найден")
        elif choice == '3':
            key = input("Введите ключ для удаления: ")
            print("Удалено" if ht.delete(key) else "Элемент не найден")
        elif choice == '4':
            key = input("Введите ключ: ")
            new_value = input("Введите новое значение: ")
            print("Обновлено" if ht.update(key, new_value) else "Элемент не найден")
        elif choice == '5':
            ht.display()
        elif choice == '6':
            print(f"Коэффициент заполнения: {ht.load_factor():.2f}")
        elif choice == '7':
            print("Выход.")
            break
        else:
            print("Неверный выбор. Повторите.")


if __name__ == '__main__':
    main()

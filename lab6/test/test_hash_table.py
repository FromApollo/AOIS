import unittest

from src.hash_table import *

from unittest.mock import patch
import io


class TestHashTable(unittest.TestCase):
    def setUp(self):
        self.ht = HashTable()

    def test_insert_and_search(self):
        self.ht.insert("ВЕКТОР", "Направленный отрезок")
        self.assertEqual(self.ht.search("ВЕКТОР"), "Направленный отрезок")

    def test_insert_overwrite(self):
        self.ht.insert("ВЕКТОР", "Отрезок")
        self.ht.insert("ВЕКТОР", "Направленный отрезок")
        self.assertEqual(self.ht.search("ВЕКТОР"), "Направленный отрезок")

    def test_delete(self):
        self.ht.insert("ГРАФ", "Вершины и рёбра")
        self.assertTrue(self.ht.delete("ГРАФ"))
        self.assertIsNone(self.ht.search("ГРАФ"))

    def test_delete_nonexistent(self):
        self.assertFalse(self.ht.delete("НЕСУЩЕСТВУЕТ"))

    def test_update_existing(self):
        self.ht.insert("МАТРИЦА", "Сетка чисел")
        self.assertTrue(self.ht.update("МАТРИЦА", "Таблица чисел"))
        self.assertEqual(self.ht.search("МАТРИЦА"), "Таблица чисел")

    def test_update_deleted(self):
        self.ht.insert("ИНТЕГРАЛ", "Область под графиком")
        self.ht.delete("ИНТЕГРАЛ")
        self.assertFalse(self.ht.update("ИНТЕГРАЛ", "Новая инфа"))

    def test_update_nonexistent(self):
        self.assertFalse(self.ht.update("ФУНКЦИЯ", "Зависимость"))

    def test_collision_handling(self):
        # Специально подбираем ключи, дающие одну и ту же хеш-функцию
        key1, key2 = "АА", "АБ"  # Похожий хеш
        self.ht.insert(key1, "Первый")
        self.ht.insert(key2, "Второй")
        self.assertEqual(self.ht.search(key1), "Первый")
        self.assertEqual(self.ht.search(key2), "Второй")

    def test_load_factor(self):
        self.ht.insert("АА", "Первый")
        self.ht.insert("АБ", "Второй")
        self.assertAlmostEqual(self.ht.load_factor(), 2 / TABLE_SIZE)

    def test_flags_correctness(self):
        self.ht.insert("ФУНКЦИЯ", "Зависимость")
        index = self.ht.hash_function("ФУНКЦИЯ")
        node = self.ht.table[index]
        while node and node.key != "ФУНКЦИЯ":
            node = node.next
        self.assertEqual(node.flags['D'], 0)
        self.ht.delete("ФУНКЦИЯ")
        self.assertEqual(node.flags['D'], 1)
        self.assertEqual(node.flags['U'], 0)

    def test_display_empty_table(self):
        expected_output = "\nПолная таблица:\n" + "\n".join([f"{i:2d}: None" for i in range(TABLE_SIZE)]) + "\n"

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.ht.display()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_display_with_data(self):
        self.ht.insert("АА", "Первый")
        self.ht.insert("АБ", "Второй")
        self.ht.insert("ВЕКТОР", "Направленный отрезок")

        index_aa = self.ht.hash_function("АА")
        index_ab = self.ht.hash_function("АБ")
        index_vec = self.ht.hash_function("ВЕКТОР")

        expected_lines = ["\nПолная таблица:"]
        for i in range(TABLE_SIZE):
            line = f"{i:2d}: "
            if i == index_aa:
                line += "[АА → Первый, F:{'C': 0, 'U': 1, 'T': 0, 'L': 1, 'D': 0}] -> None"
            elif i == index_ab:
                line += "[АБ → Второй, F:{'C': 0, 'U': 1, 'T': 0, 'L': 1, 'D': 0}] -> None"
            elif i == index_vec:
                line += "[ВЕКТОР → Направленный отрезок, F:{'C': 0, 'U': 1, 'T': 0, 'L': 1, 'D': 0}] -> None"
            else:
                line += "None"
            expected_lines.append(line)

        expected_output = "\n".join(expected_lines) + "\n"

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.ht.display()
            self.assertEqual(fake_out.getvalue(), expected_output)

    def test_display_with_deleted(self):
        self.ht.insert("ГРАФ", "Вершины и рёбра")
        self.ht.delete("ГРАФ")

        index = self.ht.hash_function("ГРАФ")

        expected_output = "\nПолная таблица:\n" + "\n".join([
            f"{i:2d}: None" if i != index
            else f"{i:2d}: None"  # Удаленные элементы не отображаются
            for i in range(TABLE_SIZE)
        ]) + "\n"

        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            self.ht.display()
            self.assertEqual(fake_out.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()

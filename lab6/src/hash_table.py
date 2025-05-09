alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
alphabet_map = {char: idx for idx, char in enumerate(alphabet)}
TABLE_SIZE = 20


class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.flags = {'C': 0, 'U': 1, 'T': 0, 'L': 1, 'D': 0}
        self.next = None

    def __str__(self):
        return f"{self.key} → {self.value}, F:{self.flags}"


class HashTable:
    def __init__(self):
        self.table = [None] * TABLE_SIZE

    def hash_function(self, key):
        key = key.upper()
        if len(key) < 2:
            key += 'А'
        a = alphabet_map.get(key[0], 0)
        b = alphabet_map.get(key[1], 0)
        V = a * 33 + b
        return V % TABLE_SIZE

    def insert(self, key, value):
        index = self.hash_function(key)
        node = self.table[index]

        if node is None:
            self.table[index] = HashNode(key, value)
        else:
            current = node
            while current:
                if current.key == key:
                    current.value = value
                    current.flags['D'] = 0
                    current.flags['U'] = 1
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = HashNode(key, value)
            node.flags['C'] = 1

    def search(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key and current.flags['D'] == 0:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key and current.flags['D'] == 0:
                current.flags['D'] = 1
                current.flags['U'] = 0
                return True
            current = current.next
        return False

    def update(self, key, new_value):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key and current.flags['D'] == 0:
                current.value = new_value
                return True
            current = current.next
        return False

    def display(self):
        print("\nПолная таблица:")
        for i, node in enumerate(self.table):
            print(f"{i:2d}: ", end='')
            current = node
            empty = True
            while current:
                if current.flags['D'] == 0:
                    print(f"[{current}] -> ", end='')
                    empty = False
                current = current.next
            if empty:
                print("None")
            else:
                print("None")

    def load_factor(self):
        count = 0
        for node in self.table:
            current = node
            while current:
                if current.flags['D'] == 0:
                    count += 1
                current = current.next
        return count / TABLE_SIZE

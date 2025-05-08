# Name: Cassidy Williams
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Due Date: 3/17/2023
# Description: HashMap (Portfolio Assignment)

from a6_include import (DynamicArray, LinkedList,
                        hash_function_0, hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Adds key/value pair to hash map. If key is already in map, update value only.
        If load factor is 1 or more, resize to double capacity.

        param: key to add, value at key
        """
        if self.table_load() >= 1.0:
            # resize to double current capacity
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # if key already in hash map, update value only
        if self.contains_key(key):
            for pos in self._buckets[index]:
                if pos.key == key:
                    pos.value = value
                    return
        # insert new key and value, increase size
        self._buckets[index].insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Counts empty buckets in hash map

        return: int count of empty buckets
        """
        i = 0
        count = 0
        while i < self._capacity:
            # check for empty bucket, increase count
            if self._buckets[i].length() == 0:
                count += 1
            i += 1
        return count

    def table_load(self) -> float:
        """
        Calculate and return hash table load factor

        return: float load factor
        """
        if self.get_size() == 0:
            return 0.0
        return self.get_size()/self._capacity

    def clear(self) -> None:
        """
        Clear the hashmap, retaining capacity
        """
        i = 0
        while i < self.get_capacity():
            # clear each bucket
            self._buckets[i] = LinkedList()
            i += 1
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize hash table capacity as appropriate.
        If not prime, go to next prime.
        Rehash all key/values from original hash map

        param: new_capacity for hash map
        """
        if new_capacity < 1:
            return
        # find next prime for new capacity
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        # check table load is appropriate
        while self.table_load() > 1:
            new_capacity *= 2
            if not self._is_prime(new_capacity):
                new_capacity = self._next_prime(new_capacity)
                self._capacity = new_capacity
        # new DynamicArray for new buckets
        new_buckets = DynamicArray()
        i = 0
        for i in range(new_capacity):
            new_buckets.append(LinkedList())
        i = 0
        while i < self._buckets.length():
            # iterate through bucket
            for pos in self._buckets[i]:
                # rehash and insert key/values to new buckets
                hash = self._hash_function(pos.key)
                index = hash % new_capacity
                new_buckets[index].insert(pos.key, pos.value)
            i += 1
        self._buckets = new_buckets
        self._capacity = new_capacity

    def get(self, key: str):
        """
        Find key in hash map and return value.
        If key is not in hash map, return None.

        param: key to search for
        return: value of key or None
        """
        # find bucket for key in hash map
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # iterate through bucket, return value if matching key found
        for pos in self._buckets[index]:
            if pos.key == key:
                return pos.value
        return None

    def contains_key(self, key: str) -> bool:
        """
        Search for key in hash map and return True if found

        param: key to search for
        return: True if found, False if not
        """
        # find bucket for key in hash map
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # iterate through bucket, return True if key found
        for pos in self._buckets[index]:
            if pos.key == key:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        Find and remove key/value from hash map
        If key not in hash map, do nothing

        param: key to remove
        """
        if not self.contains_key(key):
            return
        # find bucket for key in hash map
        hash = self._hash_function(key)
        index = hash % self._buckets.length()
        # iterate through bucket, removing if match
        for pos in self._buckets[index]:
            if pos.key == key:
                self._buckets[index].remove(pos.key)
                self._size -= 1
                return
        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        Make and return DynamicArray with all key/value pairs as tuples

        return: DynamicArray with key/value tuples
        """
        key_values = DynamicArray()
        i = 0
        while i < self._buckets.length():
            for pos in self._buckets[i]:
                key_values.append((pos.key, pos.value))
            i += 1
        return key_values

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives dynamic array and returns tuple with mode(s) and frequency

    param: da DynamicArray to find mode of
    return: tuple of DynamicArray of mode value(s) and int mode frequency
    """
    map = HashMap()
    i = 0
    # hash each da value as a key, let the value represent the count
    while i < da.length():
        if map.contains_key(da.get_at_index(i)):
            count = map.get(da.get_at_index(i)) + 1
            map.put(da.get_at_index(i), count)
        else:
            map.put(da.get_at_index(i), 1)
        i += 1
    i = 0
    modeCount = 0
    # map key/values to new DynamicArray
    modes = map.get_keys_and_values()
    all_modes = DynamicArray()
    while i < modes.length():
        # check if count is greater than modeCount
        if modeCount < modes.get_at_index(i)[1]:
            modeCount = modes.get_at_index(i)[1]
            # reset all_modes to contain new mode only
            all_modes = DynamicArray()
            all_modes.append(modes.get_at_index(i)[0])
        # if same count as modeCount, add to all_modes
        elif modeCount == modes.get_at_index(i)[1]:
            all_modes.append(modes.get_at_index(i)[0])
        i += 1
    return (all_modes, modeCount)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(7, hash_function_0)
    m.put(55,55)
    m.put(3, 3)
    m.put(33, 33)
    m.put(22, 22)
    m.put(42, 42)
    m.put(76, 76)
    m.put(20, 20)
    print(m)
    print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    '''
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
    '''

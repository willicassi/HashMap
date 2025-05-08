# Name: Cassidy Williams
# Course: CS261 - Data Structures
# Assignment: Assignment 6
# Description: HashMap (Portfolio Assignment)

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        If load factor is 0.5 or more, resize to double capacity.

        param: key to add, value at key
        """
        if self.table_load() >= 0.5:
            # resize to double current capacity
            self.resize_table(self.get_capacity() * 2)
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        new_index = index
        j = 1
        while self._buckets[new_index] is not None and not self._buckets[new_index].is_tombstone:
            # if key already present, update value
            if self._buckets[new_index].key == key:
                self._buckets[new_index].value = value
                self._buckets[new_index].is_tombstone = False
                return
            # quadratic probe
            new_index = (index + (j * j)) % self.get_capacity()
            j += 1
        # insert new key/value and increase size
        self._buckets[new_index] = HashEntry(key, value)
        self._size += 1
        return

    def table_load(self) -> float:
        """
        Calculate and return hash table load factor

        return: float load factor
        """
        if self.get_size() == 0:
            return 0.0
        return self.get_size() / self._capacity

    def empty_buckets(self) -> int:
        """
        Counts empty buckets in hash map

        return: int count of empty buckets
        """
        return self.get_capacity() - self.get_size()

    def resize_table(self, new_capacity: int) -> None:
        """
        Resize hash table capacity as appropriate.
        If not prime, go to next prime.
        Rehash all key/values from original hash map

        param: new_capacity for hash map
        """
        if new_capacity < self.get_size():
            return
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)
        done = False
        while not done:
            # new DynamicArray for new buckets
            new_buckets = DynamicArray()
            old_buckets = self._buckets
            i = 0
            for i in range(new_capacity):
                new_buckets.append(None)
            self._buckets = new_buckets
            self._capacity = new_capacity
            self._size = 0
            i = 0
            # get key/values from old buckets
            while i < old_buckets.length():
                if old_buckets[i] is not None and not old_buckets[i].is_tombstone:
                    # insert key/values to new buckets
                    self.put(old_buckets[i].key, old_buckets[i].value)
                i += 1
            # check table load is appropriate
            if self.table_load() > 0.5:
                new_capacity *= 2
                if not self._is_prime(new_capacity):
                    new_capacity = self._next_prime(new_capacity)
            else:
                done = True

    def get(self, key: str) -> object:
        """
        Find key in hash map and return value.
        If key is not in hash map, return None.

        param: key to search for
        return: value of key or None
        """
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        new_index = index
        j = 1
        while self._buckets[new_index] is not None:
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                return self._buckets[new_index].value
            new_index = (index + (j * j)) % self.get_capacity()
            j += 1
        return None

    def contains_key(self, key: str) -> bool:
        """
        Search for key in hash map and return True if found

        param: key to search for
        return: True if found, False if not
        """
        # find index position
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        new_index = index
        j = 1
        while self._buckets[new_index] is not None:
            # compare key at index
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                return True
            # quadratic probe
            new_index = (index + (j * j)) % self.get_capacity()
            j += 1
        return False

    def remove(self, key: str) -> None:
        """
        Find and remove key/value from hash map
        If key not in hash map, do nothing

        param: key to remove
        """
        # find index position
        hash = self._hash_function(key)
        index = hash % self.get_capacity()
        new_index = index
        j = 1
        while self._buckets[new_index] is not None:
            # compare key at index
            if self._buckets[new_index].key == key and not self._buckets[new_index].is_tombstone:
                # set to tombstone, decrease size
                self._buckets[new_index].is_tombstone = True
                self._size -= 1
                return
            # quadratic probe
            new_index = (index + (j * j)) % self.get_capacity()
            j += 1
        return

    def clear(self) -> None:
        """
        Clear the hashmap, retaining capacity
        """
        i = 0
        # clear each bucket in hash map
        while i < self.get_capacity():
            self._buckets[i] = None
            i += 1
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Make and return DynamicArray with all key/value pairs as tuples

        return: DynamicArray with key/value tuples
        """
        key_values = DynamicArray()
        i = 0
        while i < self.get_capacity():
            # append non-empty non-tombstone buckets to key_values
            if self._buckets[i] is not None and not self._buckets[i].is_tombstone:
                key_values.append((self._buckets[i].key, self._buckets[i].value))
            i += 1
        return key_values

    def __iter__(self):
        """
        Initialize iterator at beginning of hash map
        """
        self._pos = 0
        return self

    def __next__(self):
        """
        Iterate to next key/value in hash map
        """
        self._pos += 1
        # return only buckets with contents
        while self._buckets[self._pos] is None or self._buckets[self._pos].is_tombstone:
            self._pos += 1
            # stop and end of hash map
            if self._pos >= self._capacity:
                raise StopIteration
        return self._buckets[self._pos]



# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

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

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

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
    m = HashMap(11, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

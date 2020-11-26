from enum import Enum
import config

class hashset:
    def __init__(self):
        # TODO: create initial hash table
        self.verbose = config.verbose
        self.mode = config.mode
        self.hash_table_size = config.init_size

        # Variables for counting statistics and sizes/rehashing
        self.conflicts = 0
        self.no_inserts = 0
        self.re_hashes = 0
        self.duplicates = 0
        self.dict_size = 0

        self.hash_table = [] # Hash table which will become a list of cells/chains

        # If function for correctly initializing the right table for the different modes
        if HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
            for i in range(self.hash_table_size):
                self.hash_table.append(chain())
                # Appending array with chain objects
        else:
            for i in range(self.hash_table_size):
                self.hash_table.append(cell(None))
                # Appending array with cell objects
                
    # Helper functions for finding prime numbers
    def isPrime(self, n):
        i = 2
        while (i * i < n):
            if (n % i == 0):
                return False
            i = i + 1
        return True
        
    def nextPrime(self, n):
        while (not self.isPrime(n)):
            n = n + 1
        return n
        
    # def size(self):
        # TODO return number of values stored in table
        # print("Placeholder")

    def insert(self, value):
        # TODO code for inserting into  hash table
        if not self.find(value) or self.no_inserts == 0:
            if HashingModes(self.mode) == HashingModes.HASH_1_LINEAR_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_LINEAR_PROBING:
                # -- INSERT LINEAR PROBING --
                location = self.hash(value)
                location_initial = location
                iterator = 1
                if self.hash_table[location].current_state == state.in_use:
                    self.conflicts = self.conflicts + 1
                while self.hash_table[location].current_state == state.in_use:
                    location = (location_initial + iterator) % self.hash_table_size
                    iterator = (iterator + 1) % self.hash_table_size
                    if self.load_factor() > 0.75 or location_initial == location:
                        self.re_hash(self.nextPrime(self.hash_table_size * 3))
                        location = self.hash(value)
                        location_initial = location
                        iterator = 1
                self.hash_table[location] = cell(value, 1)
                # -- INSERT LINEAR PROBING --

            elif HashingModes(self.mode) == HashingModes.HASH_1_QUADRATIC_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_QUADRATIC_PROBING:
                # -- INSERT QUADRATIC PROBING --
                location = self.hash(value)
                location_initial = location
                iterator = 1
                if self.hash_table[location].current_state == state.in_use:
                    self.conflicts = self.conflicts + 1
                while self.hash_table[location].current_state == state.in_use:
                    location = (location_initial + (iterator ** 2)) % self.hash_table_size
                    iterator = (iterator + 1) % self.hash_table_size
                    if self.load_factor() > 0.75 or location_initial == location:
                        self.re_hash(self.nextPrime(self.hash_table_size * 3))
                        location = self.hash(value)
                        location_initial = location
                        iterator = 1
                self.hash_table[location] = cell(value, 1)
                # -- INSERT QUADRATIC PROBING --

            elif HashingModes(self.mode) == HashingModes.HASH_1_DOUBLE_HASHING or HashingModes(self.mode) == HashingModes.HASH_2_DOUBLE_HASHING:
                # -- INSERT DOUBLE HASHING --
                location = self.hash(value)
                location_initial = location
                location_otherhash = self.other_hash(value)
                iterator = 1
                if self.hash_table[location].current_state == state.in_use:
                    self.conflicts = self.conflicts + 1
                while self.hash_table[location].current_state == state.in_use:
                    location = (location_initial + (iterator * location_otherhash)) % self.hash_table_size
                    iterator = (iterator + 1) % self.hash_table_size
                    if self.load_factor() > 0.75 or location_initial == location:
                        self.re_hash(self.nextPrime(self.hash_table_size * 3))
                        location = self.hash(value)
                        location_initial = location
                        location_otherhash = self.other_hash(value)
                        iterator = 1
                self.hash_table[location] = cell(value, 1)
                # -- INSERT DOUBLE HASHING --

            elif HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
                # -- INSERT SEPARATE CHAINING --
                location = self.hash(value)
                self.hash_table[location].elements.append(value)
                if len(self.hash_table[location].elements) >= 2:
                    self.conflicts = self.conflicts + 1
                if (self.load_factor() > 5):
                    self.re_hash(self.nextPrime(self.hash_table_size * 5))
                # -- INSERT SEPARATE CHAINING --

            else:
                print("Can not determine Probing Mode")
                exit()
            self.no_inserts = self.no_inserts + 1
            self.dict_size = self.dict_size + 1
        else:
            self.duplicates = self.duplicates + 1
            self.dict_size = self.dict_size + 1

    def find(self, value):
        # TODO code for looking up in hash table
        if HashingModes(self.mode) == HashingModes.HASH_1_LINEAR_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_LINEAR_PROBING:
            # -- FIND LINEAR PROBING --
            location = self.hash(value)
            location_initial = location
            iterator = 1
            while not self.hash_table[location].current_state == state.empty:
                if self.hash_table[location].element == value:
                    return True
                location = (location_initial + iterator) % self.hash_table_size
                iterator = (iterator + 1) % self.hash_table_size
            return False
            # -- FIND LINEAR PROBING --

        elif HashingModes(self.mode) == HashingModes.HASH_1_QUADRATIC_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_QUADRATIC_PROBING:
            # -- FIND QUADRATIC PROBING --
            location = self.hash(value)
            location_initial = location
            iterator = 1
            while not self.hash_table[location].current_state == state.empty:
                if self.hash_table[location].element == value:
                    return True
                location = (location_initial + (iterator ** 2)) % self.hash_table_size
                iterator = (iterator + 1) % self.hash_table_size
            return False
            # -- FIND QUADRATIC PROBING --

        elif HashingModes(self.mode) == HashingModes.HASH_1_DOUBLE_HASHING or HashingModes(self.mode) == HashingModes.HASH_2_DOUBLE_HASHING:
            # -- FIND DOUBLE HASHING --
            location = self.hash(value)
            location_initial = location
            location_otherhash = self.other_hash(value)
            iterator = 1
            while not self.hash_table[location].current_state == state.empty:
                if self.hash_table[location].element == value:
                    return True
                location = (location_initial + (iterator * location_otherhash)) % self.hash_table_size
                iterator = (iterator + 1) % self.hash_table_size
            return False
            # -- FIND DOUBLE HASHING --

        elif HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
            # -- FIND SEPARATE CHAINING --
            location = self.hash(value)
            iterator = 0
            while iterator < len(self.hash_table[location].elements):
                if self.hash_table[location].elements[iterator] == value:
                    return True
                iterator = iterator + 1
            return False
            # -- FIND SEPARATE CHAINING --

        else:
            print("Can not determine Probing Mode")
            exit()
        
    def hash(self, hashed_value):
        # Selects which hash function to use
        if HashingModes(self.mode) == HashingModes.HASH_1_LINEAR_PROBING or HashingModes(self.mode) == HashingModes.HASH_1_QUADRATIC_PROBING or HashingModes(self.mode) == HashingModes.HASH_1_DOUBLE_HASHING or HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING:
            # 1st Hash function
            return self.hash_1(hashed_value)
        elif HashingModes(self.mode) == HashingModes.HASH_2_LINEAR_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_QUADRATIC_PROBING or HashingModes(self.mode) == HashingModes.HASH_2_DOUBLE_HASHING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
            # 2nd Hash function
            return self.hash_2(hashed_value)
        else:
            print("Can not determine Hashing Mode")
            exit()

    def hash_1(self, hashed_value):
        # 1st Hash function
        sum = 0
        i = 1
        for char in hashed_value:
            sum = sum + ord(char) * (31 ** (len(hashed_value) - i))
            i = i + 1
        return sum % self.hash_table_size 
        # Sum of character ASCII values * 31 at the power of k-i, with i being the position of the character in the string
        
    def hash_2(self, hashed_value):
        # 2nd Hash function
        sum = 0
        for char in hashed_value:
            sum = sum + ord(char) + (sum * 2 ** 5)
        return sum % self.hash_table_size
        # Sum of character ASCII values in order plus the current Sum * 2 at the power of 5

    def re_hash(self, new_size):
        # Rehashing function
        # Store current values, so that they can be updated after the rehash
        # This is so that the rehash does not interfere with our data 
        self.hash_table_size = new_size
        conflicts_current = self.conflicts
        no_inserts_current = self.no_inserts
        table_current = self.hash_table
        current_dict_size = self.dict_size
        
        self.hash_table = []

        # If statement to check if the mode is separate chaining or something else
        if HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
            # Appending array with chain objects
            for i in range(self.hash_table_size):
                self.hash_table.append(chain())
            # Insert elements from hash table before rehashing to the one that has been rehased
            for obj in table_current:
                if len(obj.elements) > 0:
                    for element in obj.elements:
                        self.insert(element)
        else:
            # Appending array with cell objects
            for i in range(self.hash_table_size):
                self.hash_table.append(cell(None))
            # Insert elements from hash table before rehashing to the one that has been rehased
            for obj in table_current:
                if obj.current_state == state.in_use:
                    self.insert(obj.element)

        # Re assign the correct values
        self.conflicts = conflicts_current
        self.no_inserts = no_inserts_current
        self.dict_size = current_dict_size
        self.re_hashes = self.re_hashes + 1

    def load_factor(self):
        # Calculates the load factor of the hash table
        ld_factor = float(self.no_inserts) / float(self.hash_table_size)
        return ld_factor

    def other_hash(self, value):
        # Method for selecting the other hash
        # Same as hash() method but the other way around
        if HashingModes(self.mode) == HashingModes.HASH_1_DOUBLE_HASHING:
            return self.hash_2(value)
        elif HashingModes(self.mode) == HashingModes.HASH_2_DOUBLE_HASHING:
            return self.hash_1(value)

    def print_set(self):
        # Code for printing hash table
        print("Printing hash table:")
        # print("*location* -> *value*")
        if HashingModes(self.mode) == HashingModes.HASH_1_SEPARATE_CHAINING or HashingModes(self.mode) == HashingModes.HASH_2_SEPARATE_CHAINING:
            # If using separate chaining mode, prints the whole chain of values
            for iterator in range(self.hash_table_size):
                print(str(iterator))
                for iterator_chain in range(len(self.hash_table[iterator].elements)):
                    print(" -> " + str(self.hash_table[iterator].elements[iterator_chain]))
        else:
            # Else prints the location and its value
            for iterator in range(self.hash_table_size):
                print(str(iterator) + " -> " + str(self.hash_table[iterator].element))
        
    def print_stats(self):
        # Code for printing statistics and debugging info
        print("Probing and hashing mode: " + str(HashingModes(self.mode)))
        print("Length of hast table: " + str(self.hash_table_size))
        print("Size of dictionary: " + str(self.dict_size))
        print("Number of inserts: " + str(self.no_inserts))
        print("Duplicates: " + str(self.duplicates))
        print("Conflicts: " + str(self.conflicts))
        print("Collision average: " + str(int(self.conflicts / self.no_inserts * 100)) + "%")
        print("Load factor of the hash table: " + str(self.load_factor()))
        print("Number of re hashes: " + str(self.re_hashes))

# This is a cell structure assuming Open Addressing
# It should contain and element that is the key and a state which is empty, in_use or deleted
# You will need alternative data-structures for separate chaining

class cell:
    def __init__(self, key, recieved_state = 0):
        self.element = key
        self.current_state = state(recieved_state)

class chain:
    # Data-structure for when using separate chaining method
    def __init__(self):
        self.elements = []
        
class state(Enum):
    empty = 0
    in_use = 1
    deleted = 2
        
# Hashing Modes
class HashingModes(Enum):
    HASH_1_LINEAR_PROBING=0
    HASH_1_QUADRATIC_PROBING=1
    HASH_1_DOUBLE_HASHING=2
    HASH_1_SEPARATE_CHAINING=3
    HASH_2_LINEAR_PROBING=4
    HASH_2_QUADRATIC_PROBING=5
    HASH_2_DOUBLE_HASHING=6
    HASH_2_SEPARATE_CHAINING=7

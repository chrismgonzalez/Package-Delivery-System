class HashTable(object):
    # the init method gives the default size value(if not specified when called)
    # to the Hashtable class, it then calls the _create_hash method with the
    # desired size as an argument
    def __init__(self, size=1):
        self._struct = self._create_hash(size)

    # insert will hash key key and find the modulo value
    # it will use the module to find the container to insert it in to
    # Time complexity: 0(n) - where 'n' is the container size.
    def insert(self, key, value):
        hashed_key = hash(key)
        container = self._find_container(hashed_key)
        extent = self._find_kv_pair(hashed_key, container)

        if len(extent) == 0:
            container.append([hashed_key, value])
        else:
            extent[1] = value

        return True

    def find(self, key):
        hashed_key = hash(key)
        container = self._find_container(hashed_key)

        kv_pair = self._find_kv_pair(hashed_key, container)

        if kv_pair:
            return kv_pair[1]

        raise Exception("Sorry, that key-value pair is does not exist!")

    # the _create_hash method loops through the hash table size (in this case 10) and creates buckets
    # to be used for hashing at a later time
    # Time complexity: O(n)
    def _create_hash(self, size):
        struct = []
        for i in range(size):
            struct.append([])

        return struct

    # the _find_container method uses standard hashing practice of using the modulo
    # of the hashed key to find the related value of data
    # Time complexity: 0(1) -- this is why the hash is a great data structure - it's fast!
    def _find_container(self, key):
        return self._struct[key % len(self._struct)]

    # _find_keyval_pair loops through a container and finds the corresponding key-value pair
    # inside the bucket
    # Time complexity: 0(n)
    def _find_kv_pair(self, key, container):
        for kv_pair in container:
            if kv_pair[0] == key:
                return kv_pair

        return []

    # the check_size method determines if the HashTable is too populated
    # it returns a boolean value if the number of items counted is greater
    # the length of the array divided by 2
    # Time complexity: O(n)
    def check_size(self):
        items = 0

        for item in self.array:
            if item is not None:
                items += 1

        return items > len(self.array)/2

    # the resize method resizes the hashtable to be double the current length
    # this helps the HashTable class become self-adjusting when inserting new
    # values into the HashTable
    # Time complexity: 0(n^2)
    def resize(self):
        resized_hash = HashTable(size=len(self.array)*2)
        for i in range(len(self.array)):
            if self.array[i] is None:
                continue

            for kv_pair in self.array[i]:
                resized_hash.insert(kv_pair[0], kv_pair[1])


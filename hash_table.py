# create a hash table using a desired size
# map keys to buckets


class Hashtable:
    def __init__(self, size=10):
        self._struct = self._create_struct(size)

    def _create_struct(self, size):
        struct = []
        for i in range(size):
            struct.append([])

        return struct
# implement methods: insert, find, _find_bucket, find keyval_pair

# Abstract interface for HeapNodes
class HeapNode:
    key = None
    right = None
    child = None


# Abstract interface for heaps
class Heap:

    # Inserts new element to a nodes
    # Can be used with key and value
    # or only with key.
    def insert(self, key, value=None):
        raise NotImplementedError

    # Returns the min node
    def find_min(self):
        raise NotImplementedError

    # Deletes the given node
    def delete(self, node):
        raise NotImplementedError

    # Deletes and returns the min node
    def delete_min(self):
        raise NotImplementedError

    # Merges another heap to this heap
    def merge(self, heap):
        raise NotImplementedError

    # Decrease the value of the key of the given nodes
    # new_key must lower than current key value.
    def decrease_key(self, node, new_key):
        raise NotImplementedError

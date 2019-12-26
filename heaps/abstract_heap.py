# Abstract interface for HeapNodes
class HeapNode:
    key = None
    right = None
    child = None


# Abstract interface for heaps
class Heap:

    # Returns the minimum node
    # Amortized time complexity: O(1)
    def find_min(self):
        raise NotImplementedError

    # Inserts new item as a node to the heap.
    # Can be called with key (key) or value and key (key, value).
    # Returns the node.
    # Amortized time complexity: O(1)
    def insert(self, key, value=None):
        raise NotImplementedError

    # Deletes the given node
    # Amortized time complexity: O(log n)
    def delete(self, node):
        raise NotImplementedError

    # Deletes and returns the minimum node
    # Amortized time complexity: O(log n)
    def delete_min(self):
        raise NotImplementedError

    # Decrease the value of the key of the given nodes.
    # new_key must lower than current key value.
    # Returns the updated node.
    # Amortized time complexity: O(1)
    def decrease_key(self, node, new_key):
        raise NotImplementedError

    # Merges another heap into this heap
    # Amortized time complexity: O(1)
    def merge(self, heap):
        raise NotImplementedError

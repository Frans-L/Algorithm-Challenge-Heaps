# Abstract interface for HeapNodes
class HeapNode:
    key = None
    right = None
    child = None
    val = None


# Abstract interface of the heap
class Heap:

    # Return the minimum node.
    # Amortized time complexity: O(1)
    def find_min(self):
        raise NotImplementedError

    # Insert new item as a node to the heap.
    # Can be called with key (key) or value and key (key, value).
    # Return the node.
    # Amortized time complexity: O(1)
    def insert(self, key, value=None):
        raise NotImplementedError

    # Delete the given node.
    # Amortized time complexity: O(log n)
    def delete(self, node):
        raise NotImplementedError

    # Delete and returns the minimum node.
    # Amortized time complexity: O(log n)
    def delete_min(self):
        raise NotImplementedError

    # Decrease the value of the key of the given nodes.
    # new_key must lower than current key value.
    # Return the updated node.
    # Amortized time complexity: O(1)
    def decrease_key(self, node, new_key):
        raise NotImplementedError

    # Merge another heap into this heap.
    # Amortized time complexity: O(1)
    def merge(self, heap):
        raise NotImplementedError

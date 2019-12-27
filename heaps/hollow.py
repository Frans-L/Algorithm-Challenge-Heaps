import math
import heaps.abstract_heap as heap


class _Node(heap.HeapNode):
    def __init__(self, key, val):
        self.key = key
        self.item = _Item(val, self)
        self.child = self.right = None
        self.ep = None  # extra parent, only hollow can have it
        self.rank = 0


class _Item:
    def __init__(self, val, node):
        self.val = val
        self.node = node


class HollowHeap(heap.Heap):
    def __init__(self):
        self.min = None
        self.no_nodes = 0

    # Returns the minimum node
    # Amortized time complexity: O(1)
    def find_min(self):
        return self.min

    # Inserts new item as a node to the heap.
    # Can be called with key (key) or value and key (key, value).
    # Returns the node.
    # Amortized time complexity: O(1)
    def insert(self, key, value=None):
        if value is None:
            value = key

        n = _Node(key, value)
        self.min = self._meld(n, self.min)
        self.no_nodes += 1
        return n

    # Deletes and returns the minimum node
    # Amortized time complexity: O(log n)
    def delete_min(self):
        prev_min = self.min
        self.delete(self.min)
        return prev_min

    # Deletes the given node
    # Amortized time complexity: O(log n)
    def delete(self, node):
        node.item = None
        node = None

        # lazy deletion
        if self.min.item is not None:
            self.no_nodes -= 1
            return self.min

        A = {}
        h = self.min  # use same naming as in pseudo code
        h.right = None
        while h is not None:
            w = h.child
            v = h
            h = h.right

            # loop through descendants
            while w is not None:
                u = w
                w = w.right

                # if hallow
                if u.item is None:
                    if u.ep is None:
                        u.right = h
                        h = u
                    else:
                        if u.ep == v:
                            w = None
                        else:
                            u.right = None
                        u.ep = None
                else:
                    # does ranked links
                    # similiar to fibonacci heap, unique ranks
                    while u.rank in A:
                        u = self._link(u, A[u.rank])
                        del A[u.rank]
                        u.rank += 1
                    A[u.rank] = u

        # does unranked links
        # combines subtrees with unique rank and finds the root, aka min
        for i in A:
            if h is None:
                h = A[i]
            else:
                h = self._link(h, A[i])  # returns the smaller one

        self.no_nodes -= 1
        # update the min
        self.min = h
        if self.min is not None:
            self.min.right = None

    # Decrease the value of the key of the given nodes.
    # new_key must lower than current key value.
    # Returns the updated node.
    # Amortized time complexity: O(1)
    def decrease_key(self, node, new_key):
        assert (
            node.key > new_key
        ), "The new_key must be lower than current when decreasing key."
        assert (
            node.item is not None
        ), "The node is missing item. It's hollow. Cannot be decreased."

        u = node  # same naming as in pseudo code

        # decreasing min value, simple cases
        if u == self.min:
            u.key = new_key
            return self.min

        # otherwise
        v = _Node(new_key, u.item.val)
        u.item = None

        if u.rank > 2:
            v.rank = u.rank - 2
        v.child = u
        u.ep = v

        h = self._link(v, self.min)
        if h != self.min:
            self.min = h
        return v

    # Merges another heap into this heap
    # Amortized time complexity: O(1)
    def merge(self, heap):
        assert isinstance(heap, HollowHeap)
        self.min = self._meld(self.min, heap.min)
        self.no_nodes += heap.no_nodes

    # Inserts new node as a child
    # Heap do not allow this, but this is only used for debugging
    def _debug_insert_child(self, parent, key, value=None):
        if value is None:
            value = key

        n = _Node(key, value)
        self._add_child(n, parent)
        self.no_nodes += 1
        return n

    # Combines two sub trees
    def _meld(self, n, m):
        if n is None:
            return m
        if m is None:
            return n
        return self._link(n, m)

    # Makes given node to be a child of another given node
    def _add_child(self, child, parent):
        child.right = parent.child
        parent.child = child

    # Links two nodes together
    def _link(self, n, m):
        if m.key > n.key:
            self._add_child(m, n)
            return n
        else:
            self._add_child(n, m)
            return m

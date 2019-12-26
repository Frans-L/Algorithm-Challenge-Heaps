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
        self.max_rank = 0
        self.no_nodes = 0

    # Returns the min node
    def find_min(self):
        return self.min

    # Inserts new node into the heap.
    # Can be used with key and value
    # or only with key.
    def insert(self, key, value=None):
        if value is None:
            value = key

        n = _Node(key, value)
        self.min = self._meld(n, self.min)
        self.no_nodes += 1
        return n

    # Deletes and returns the min node
    def delete_min(self):
        self.delete(self.min)

    # Deletes the given node
    def delete(self, node):
        node.item = None
        node = None

        # lazy deletion
        if self.min.item is not None:
            return self.min

        A = [None] * (self.max_rank * 2 + self.no_nodes)  # rank max size
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
                    while A[u.rank] is not None:
                        u = self._link(u, A[u.rank])
                        A[u.rank] = None
                        u.rank += 1
                    A[u.rank] = u
                    if u.rank > self.max_rank:
                        self.max_rank = u.rank

        # does unranked links
        # combines subtrees with unique rank and finds the root, aka min
        for i in range(self.max_rank + 1):
            if A[i] is not None:
                if h is None:
                    h = A[i]
                else:
                    h = self._link(h, A[i])  # returns the smaller one
                A[i] = None

        # update the min
        self.min = h
        if self.min is not None:
            self.min.right = None
        return self.min

    # Sets a new value to the key of the node.
    # new_key must lower than current key value.
    # node must have an item, cannot be hollow.
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
    def merge(self, heap):
        assert isinstance(heap, HollowHeap)
        self.min = self._meld(self.min, heap.min)
        self.no_nodes += heap.no_nodes

    # Returns the whole layer as a list.
    # One node from the layer must be given
    def _layer_as_list(self, node):
        nodes = []
        n = node
        while n is not None:
            nodes.append(n)
            n = n.right
        return nodes

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

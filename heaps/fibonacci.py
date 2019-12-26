import math
import heaps.abstract_heap as heap


class _Node(heap.HeapNode):
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.parent = self.child = None
        self.left = self.right = self
        self.degree = 0
        self.flag = False


class FibonacciHeap(heap.Heap):
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

        # totally new heap
        if self.no_nodes == 0:
            self.min = n
        # otherwise add to root next to min
        else:
            self._add_root(n)

        self.no_nodes += 1

        return n

    # Deletes the given node
    # Amortized time complexity: O(log n)
    def delete(self, node):
        assert self.min is not None
        self.decrease_key(node, self.min.key - 1)
        self.delete_min()

    # Deletes and returns the minimum node
    # Amortized time complexity: O(log n)
    def delete_min(self):
        prev_min = self.min
        if prev_min is not None:

            # move children to root
            if prev_min.child is not None:
                n = stop = prev_min.child
                first_loop = True
                while first_loop or n != stop:
                    first_loop = False
                    next_node = n.right
                    self._add_node_left(n, self.min)
                    n.parent = None
                    n = next_node

            # remove current min
            if self.min.right != self.min:
                self.min = prev_min.right
                self._remove_node(prev_min)
                self._consolidate()
            # no nodes left
            else:
                self.min = None
                self._remove_node(prev_min)

            self.no_nodes -= 1
        return prev_min

    # Decrease the value of the key of the given nodes.
    # new_key must lower than current key value.
    # Returns the updated node.
    # Amortized time complexity: O(1)
    def decrease_key(self, node, new_key):
        assert (
            node.key > new_key
        ), "The new_key must be lower than current when decreasing key."

        node.key = new_key
        parent = node.parent

        # root element, simple case
        if parent is None:
            if node.key < self.min.key:
                self.min = node
        # otherwise
        elif node.key < parent.key:
            self._cut(node)
            self._cascading_cut(parent)

        return node

    # Merges another heap into this heap
    # Amortized time complexity: O(1)
    def merge(self, heap):
        assert isinstance(heap, FibonacciHeap)

        # if a heap is empty
        if heap.min is None:
            return
        if self.min is None:
            self.min = heap.min
            return

        # moves given heap between min and min.right
        first = self.min
        last = self.min.right
        second = heap.min
        second_last = heap.min.left

        first.right = second
        second.left = first
        last.left = second_last
        second_last.right = last

        self.no_nodes += heap.no_nodes
        if heap.min.key < self.min.key:
            self.min = heap.min

    # Adds node to left side of the given right_node
    def _add_node_left(self, node, right_node):
        node.right = right_node
        node.left = right_node.left
        right_node.left.right = node
        right_node.left = node

    # Adds node to left side of the given right_node
    def _add_root(self, node):
        self._add_node_left(node, self.min)
        if node.key < self.min.key:
            self.min = node

    # Adds node as child to another node
    def _add_child(self, child, parent):
        if parent.child is None:
            parent.child = child
            child.parent = parent
        else:
            self._add_node_left(child, parent.child)
            child.parent = parent
        parent.degree += 1

    # Inserts new node as a child
    # Heap do not allow this, but this is only used for debugging
    def _debug_insert_child(self, parent, key, value=None):
        if value is None:
            value = key
        n = _Node(key, value)
        self.no_nodes += 1
        self._add_child(n, parent)
        return n

    # Swaps variables
    def _swap_vars(self, var1, var2):
        return (var2, var1)

    # Removes element from the double linked list
    def _remove_node(self, node):
        node.left.right = node.right
        node.right.left = node.left
        node.left = node
        node.right = node
        node.parent = None

    # Moves the node root level
    def _cut(self, node):
        parent = node.parent
        parent.degree -= 1

        # if parent has only 1 child
        if parent.child == node and node.right == node:
            parent.child = None
            self._remove_node(node)
        else:
            parent.child = node.right
            self._remove_node(node)

        # add to the root level
        node.flag = False
        self._add_node_left(node, self.min)
        if node.key < self.min.key:
            self.min = node

    # Reorganizing the heap to keep it in optimal form
    def _cascading_cut(self, node):
        parent = node.parent
        if parent is not None:
            if parent.flag:
                self._cut(node)
                self._cascading_cut(parent)
            else:
                parent.flag = True

    # Returns the whole layer as a list.
    # One node from the layer must be given
    def _layer_as_list(self, node):
        items = []
        n = stop = node
        first_loop = True
        while first_loop or n != stop:
            first_loop = False
            items.append(n)
            n = n.right
        return items

    # Makes the degrees of root elements unique
    def _consolidate(self):
        degree_arr = [None for _ in range(int(math.log(self.no_nodes, 2)) + 1)]

        root_items = self._layer_as_list(self.min)
        for n in root_items:

            degree = n.degree
            # combines nodes until no same root degrees exists
            while degree_arr[degree] is not None:
                m = degree_arr[degree]
                # makes sure that n is always smaller
                if m.key < n.key:
                    n, m = self._swap_vars(n, m)
                self._remove_node(m)
                self._add_child(m, n)
                degree_arr[degree] = None
                degree += 1

            degree_arr[degree] = n

        self._update_root_min()

    # Return an item from root layer
    def _find_root_item(self):
        top_item = self.min
        while top_item.parent is not None:
            top_item = top_item.parent
        return top_item

    # Updates self.min to lowest value from the root
    def _update_root_min(self):
        top = self._find_root_item()
        root_layer = self._layer_as_list(top)
        self.min = min(root_layer, key=lambda n: n.key)

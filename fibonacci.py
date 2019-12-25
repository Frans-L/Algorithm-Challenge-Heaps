import math

class _Node:
    def __init__(self,key,val):
        self.key = key
        self.val = val
        self.parent = None
        self.child = None
        self.left = self.right = self
        self.degree = 0
        self.mark = False

class FibonacciHeap:

    def __init__(self):
        self.min = None
        self.no_nodes = 0
        self._debug_nodes = []

    # Draws the FibonacciHeap as a graph
    def vizualize(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        from collections import defaultdict
        import queue

        G = nx.Graph()
        label_dict = {} # maps nodes to labels

        # iterate the heap using breath first
        nodes = queue.Queue()
        used = defaultdict(bool)

        # start from the min node
        root = self._find_root_item()
        G.add_node(root)
        label_dict[root] = f"{root.key}"
        nodes.put(root)

        while(not nodes.empty()):
            n = nodes.get()
            used[n] = True   

            # only makes edges to parents
            if n.parent is not None:
                G.add_edge(n.parent, n, style="root")
            elif n.left != n and n != self.min:
                G.add_edge(n.left, n, style="child")

            # add all neighbour nodes
            neighbors = [n.child, n.right]
            for neighbor in neighbors:
                if not used[neighbor] and neighbor is not None:
                    G.add_node(neighbor)
                    label_dict[neighbor] = f"{neighbor.key}"
                    nodes.put(neighbor)

        pos = nx.spring_layout(G)

        root = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "root"]
        child = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "child"]
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_edges(G, pos, edgelist=root, style="dashed")
        nx.draw_networkx_edges(G, pos, edgelist=child)
        nx.draw_networkx_labels(G, pos, labels=label_dict)
        plt.show()
    

    # Inserts new node into the heap.
    # Can be used with key and value
    # or only with key.
    def insert(self, key, value = None):
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
        self._debug_nodes.append(n)

        return n

    
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
            self._add_node_left(child,parent.child)
            child.parent = parent
        parent.degree += 1

    # Inserts child to a nodes.
    # Heap do not allow this, but this is only used for debugging
    def _debug_insert_child(self, parent, key, value = None):
        if value is None: 
            value = key
        n = _Node(key, value)
        self.no_nodes += 1
        self._debug_nodes.append(n)
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

    # Removes and returns the current min element
    def extract_min(self):
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
            self.min = prev_min.right
            self._remove_node(prev_min)
            if self.min.right == self.min:
                self.min = None
            else:
                self.vizualize()
                self.consolidate()

            self.no_nodes -= 1
        return prev_min

    # Returns the whole layer as a list.
    # One node from the layer must be given
    def layer_as_list(self, node):
        items = []
        n = stop = node
        first_loop = True
        while first_loop or n != stop:
            first_loop = False
            items.append(n)
            n = n.right
        return items

    # Makes the degrees of root elements unique
    def consolidate(self):
        degree_arr = [None for _ in range(int(math.log(self.no_nodes, 2))+1)]
        
        root_items = self.layer_as_list(self.min)
        for n in root_items:

            degree = n.degree
            
            # combines nodes until no same root degrees exists 
            while degree_arr[degree] != None:
                m = degree_arr[degree]
                # makes sure that n is always smaller
                if m.key < n.key:
                    n, m = self._swap_vars(n, m)
                self._remove_node(m)
                self._add_child(m, n)
                self.vizualize()
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
        root_layer = self.layer_as_list(top)
        self.min = min(root_layer, key = lambda n: n.key)

    def _debug_print_nodes(self):
        for n in self._debug_nodes:
            output = f"{n.key} -> {n.left.key} {n.right.key}"
            if n.parent is not None:
                output += f" p: {n.parent.key}"
            if n.child is not None:
                output += f" c: {n.child.key}"
            print(output)

if __name__ == "__main__":

    f = FibonacciHeap()

    # nodes = [4,7,5,3,1,10,2]
    # for n in nodes:
    #     f.insert(n)

    n = f.insert(7)
    f._debug_insert_child(n, 9)

    n = f.insert(2)
    n2 = f._debug_insert_child(n, 4)
    n2 = f._debug_insert_child(n2, 6)
    
    n2 = f._debug_insert_child(n, 3)

    f.vizualize()
    f.extract_min()
    print("min key", f.min.key)
    f.vizualize()
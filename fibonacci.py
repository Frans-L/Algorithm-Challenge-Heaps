import math

class _Node:
    def __init__(self,key,val):
        self.key = key
        self.val = val
        self.parent = self.child = None
        self.left = self.right = self
        self.degree = 0
        self.flag = False

class FibonacciHeap:

    def __init__(self):
        self.min = None
        self.no_nodes = 0
        self._debug_nodes = set()

    # Draws the FibonacciHeap as a graph
    def visualize(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        from collections import defaultdict
        from misc_visualization import hierarchy_pos
        import queue

        G = nx.DiGraph()
        label_dict = {} # maps nodes to labels

        # first nodes
        for n in self._debug_nodes:
            G.add_node(n)
            label_dict[n] = f"{n.key}" 
       
        # parent -> child edges
        isChild = set() # used to find root level
        for n in self._debug_nodes:
            c = n.child
            if c is not None:
                childs = self._layer_as_list(c)
                for m in childs:
                    isChild.add(m)
                    G.add_edge(n, m, style="child")
        
        # parent edges
        G.add_node("root")
        label_dict["root"] = f"" 
        for n in self._debug_nodes:
            if n not in isChild:
                G.add_edge("root", n, style="root")


        # print info
        self._debug_print_nodes()

        # drawing
        layouts = [hierarchy_pos, nx.spring_layout]
        for f in layouts:
            try:
                pos = f(G)
                # root = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "root"]
                child = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "child"]
                nodes = [n for (n, d) in G.nodes(data=True) if n != "root"]
                nx.draw_networkx_nodes(G, pos, nodelist=nodes)
                # nx.draw_networkx_edges(G, pos, edgelist=root, arrows=False, style="dotted")
                nx.draw_networkx_edges(G, pos, edgelist=child)
                nx.draw_networkx_labels(G, pos, labels=label_dict)
                plt.show()
                break
            except:
                print("WARNING: Drawing failed, trying different layout.")
    

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
        self._debug_nodes.add(n)

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

    # Inserts new node as a child
    # Heap do not allow this, but this is only used for debugging
    def _debug_insert_child(self, parent, key, value = None):
        if value is None: 
            value = key
        n = _Node(key, value)
        self.no_nodes += 1
        self._debug_nodes.add(n)
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
            self._debug_nodes.remove(self.min)
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

    # Sets a new value to the key of the node.
    # new_key must lower than current key value.
    def decrease_key(self, node, new_key):
        assert node.key > new_key, \
            "The new_key must be lower than current when decreasing key."

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
        degree_arr = [None for _ in range(int(math.log(self.no_nodes, 2))+1)]
        
        root_items = self._layer_as_list(self.min)
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

    m = f.insert(7)
    n = f.insert(4)
    n = f.insert(2)
    k = f.insert(8)
    n = f.insert(12)
    n = f.insert(5)
   
    f.delete_min()
    print("min key", f.min.key)
    f.visualize()

    f.decrease_key(k, 6)
    print("min key", f.min.key)
    f.visualize()

    f.decrease_key(m, 1)
    print("min key", f.min.key)
    f.visualize()

    for i in range(3):
        print("----")
        f.delete_min()
        print("min key", f.min.key)
        f.visualize()
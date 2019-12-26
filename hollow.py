import math

class _Node:
    def __init__(self,key,val):
        self.key = key
        self.item = _Item(val, self)
        self.child = None
        self.right = None
        self.ep = None # extra parent, only hollow can have it
        self.rank = 0

class _Item:
    def __init__(self,val,node):
        self.val = val
        self.node = node

class HollowHeap:

    def __init__(self):
        self.min = None
        self.max_rank = 0
        self.no_nodes = 0
        self._debug_nodes = set()

    # Draws the FibonacciHeap as a graph
    def vizualize(self):
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
            label_dict[n] = f"{n.key}" if n.item is not None else "H"
            
       
        # parent -> child edges
        isChild = set() # used to find root level
        for n in self._debug_nodes:
            c = n.child
            if c is not None:
                childs = self._layer_as_list(c)
                for m in childs:
                    isChild.add(m)
                    if m.ep != n:
                        G.add_edge(n, m, style="child")
                    else:
                        G.add_edge(n, m, style="ep_child")

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
                ep_child = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "ep_child"]
                child = [(u, v) for (u, v, d) in G.edges(data=True) if d['style'] == "child"]
                nodes = [n for (n, d) in G.nodes(data=True) if n != "root"]
                nx.draw_networkx_nodes(G, pos, nodelist=nodes)
                # nx.draw_networkx_edges(G, pos, edgelist=root, arrows=False, style="dotted")
                nx.draw_networkx_edges(G, pos, edgelist=ep_child, arrows=False, style="dashed")
                nx.draw_networkx_edges(G, pos, edgelist=child)
                nx.draw_networkx_labels(G, pos, labels=label_dict)
                plt.show()
                break
            except:
                print("WARNING: Drawing failed, trying different layout.")

    
    # Returns the whole layer as a list.
    # One node from the layer must be given
    def _layer_as_list(self, node):
        nodes = []
        n = node
        while n is not None:
            nodes.append(n)
            n = n.right
        return nodes

    # Deletes and returns the min element
    def delete_min(self):
        self._delete(self.min.item)

    # Deletes node
    def _delete(self, item):
        item.node.item = None
        item.node = None

        # lazy deletion
        if self.min.item != None: 
            return self.min

        self._debug_nodes.remove(self.min)
        
        A = [None] * (self.max_rank + self.no_nodes + 256) # rank max size
        h = self.min # use same naming as in pseudo code
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
                        u = self._link(u,A[u.rank])
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
                    h = self._link(h,A[i]) # returns the smaller one
                A[i] = None

        # update the min
        self.min = h
        self.min.right = None
        return self.min


    # Decreases the key of the node.
    # new_key must lower than current key value.
    # node must have an item, cannot be hollow.
    def decrease_key(self, node, new_key):
        assert node.key > new_key, \
            "The new_key must be lower than current when decreasing key."
        assert node.item is not None, \
            "The node is missing item. It's hollow. Cannot be decreased."

        u = node # same naming as in pseudo code

        # decreasing min value, simple cases
        if u == self.min:
            u.key = new_key
            return self.min
        
        # otherwise
        v = _Node(new_key, u.item.val)
        self._debug_nodes.add(v)
        u.item = None

        if u.rank > 2:
            v.rank = u.rank - 2
        v.child = u
        u.ep = v

        h = self._link(v, self.min)
        if h != self.min:
            self.min = h
        return h


    # Inserts new node into the heap.
    # Can be used with key and value
    # or only with key.
    def insert(self, key, value = None):
        if value is None: 
            value = key

        n = _Node(key, value)
        self._debug_nodes.add(n)
        self.min = self._meld(n, self.min)
        self.no_nodes += 1
        return n

    # Inserts new node as a child
    # Heap do not allow this, but this is only used for debugging
    def _debug_insert_child(self, parent, key, value = None):
        if value is None: 
            value = key

        n = _Node(key, value)
        self._debug_nodes.add(n)
        self._add_child(n, parent)
        self.no_nodes += 1
        return n

    # Combines safely two hollow heaps 
    def _meld(self, n, m):
        if n is None:
            return m
        if m is None:
            return n
        return self._link(n,m)

    # Makes given node to be a child of another given node
    def _add_child(self, child, parent):
        child.right = parent.child
        parent.child = child
      
    # Links two nodes together
    def _link(self, n, m):
        if m.key > n.key:
            self._add_child(m,n)
            return n
        else:
            self._add_child(n,m)
            return m

    # Prints information of nodes
    def _debug_print_nodes(self):
        for n in self._debug_nodes:
            output = f"{n.key} -> "
            if n.right is not None:
                output += f" r: {n.right.key}"
            if n.child is not None:
                output += f" c: {n.child.key}"
            if n.ep is not None:
                output += f" ep: {n.ep.key}"
            print(output)

if __name__ == "__main__":

    f = HollowHeap()

    # nodes = [4,7,5,3,1,10,2]
    # for n in nodes:
    #     f.insert(n)

    n = f.insert(7)
    n = f.insert(3)
    n = f.insert(10)
    # f._debug_insert_child(n, 11)
    n = f.insert(12)
    # f._debug_insert_child(n, 15)
    n = f.insert(8)
    n = f.insert(4)
    n = f.insert(9)

    print("min", f.min.key)
    f.vizualize()
   
    for i in range(3):
        print("----")
        f.delete_min()
        print("min", f.min.key)
        f.vizualize()
        

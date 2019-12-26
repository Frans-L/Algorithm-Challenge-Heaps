import abstract_heap as heap
from misc import hierarchy_pos
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import queue

# Draws a heap as a graph
def visualize(_heap):
    assert isinstance(_heap, heap.Heap), "Heap must inherit Heap class."

    nodes = find_nodes(_heap)  # get all nodes
    G = nx.DiGraph()
    label_dict = {}  # maps nodes to labels

    # adds nodes to graph
    for n in nodes:
        G.add_node(n)

        # is hollow
        if hasattr(n, "item") and n.item is None:
            label_dict[n] = "H"
        else:
            label_dict[n] = n.key

    # adds parent -> child edges
    isChild = set()  # used to find root level
    for n in nodes:
        c = n.child
        if c is not None:
            childs = find_layer(c)
            for m in childs:
                isChild.add(m)
                if hasattr(m, "ep") and m.ep == n:
                    G.add_edge(n, m, style="ep_child")
                else:
                    G.add_edge(n, m, style="child")

    # root level
    G.add_node("root")
    label_dict["root"] = f""
    for n in nodes:
        if n not in isChild:
            G.add_edge("root", n, style="root")

    # draws, try 2 different layouts if first crashes
    layouts = [hierarchy_pos, nx.spring_layout]
    for f in layouts:
        try:
            pos = f(G)

            ep_child = [
                (u, v) for (u, v, d) in G.edges(data=True) if d["style"] == "ep_child"
            ]
            child = [
                (u, v) for (u, v, d) in G.edges(data=True) if d["style"] == "child"
            ]
            nodes = [n for (n, d) in G.nodes(data=True) if n != "root"]

            nx.draw_networkx_nodes(G, pos, nodelist=nodes)
            nx.draw_networkx_edges(G, pos, edgelist=child)
            nx.draw_networkx_edges(
                G, pos, edgelist=ep_child, arrows=False, style="dashed"
            )
            nx.draw_networkx_labels(G, pos, labels=label_dict)

            plt.show()
            break  # no need to try another layout
        except BaseException:
            print("WARNING: Drawing failed, trying different layout.")


# Gathers all nodes to one list
def find_nodes(heap):
    nodes = set()
    stack = queue.Queue()
    stack.put(heap.find_min())

    while not stack.empty():
        n = stack.get()
        if n is not None and n not in nodes:
            nodes.add(n)
            stack.put(n.child)
            stack.put(n.right)
    return list(nodes)


# Retuns all elements as a list under same node.parent
def find_layer(node):
    items = []
    n = stop = node
    first_loop = True
    while n is not None and (first_loop or n != stop):
        first_loop = False
        items.append(n)
        n = n.right
    return items

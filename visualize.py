import heaps.abstract_heap as heap
from misc import hierarchy_pos
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import queue

# Draws a heap as a graph
def visualize(_heap, title="Heap", debug_print=True):
    assert isinstance(_heap, heap.Heap), "Heap must inherit Heap class."

    nodes = find_nodes(_heap)  # get all nodes
    G = nx.DiGraph()
    label_dict = {}  # maps nodes to labels

    # print all node data
    if debug_print:
        print("-" * 40)
        print(title)
        print_nodes(nodes)

    # adds nodes to graph
    for n in nodes:
        # is min
        style = "normal" if n is not _heap.find_min() else "min"
        # is hollow
        if hasattr(n, "item") and n.item is None:
            label_dict[n] = ""
            style = "hollow"
        else:
            label_dict[n] = n.key

        G.add_node(n, style=style)

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
    G.add_node("root", style="hidden")
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
            nx_nodes = [n for (n, d) in G.nodes(data=True) if d["style"] == "normal"]
            nx_nodes_min = [n for (n, d) in G.nodes(data=True) if d["style"] == "min"]
            nx_nodes_hollow = [
                n for (n, d) in G.nodes(data=True) if d["style"] == "hollow"
            ]

            nx.draw_networkx_nodes(G, pos, nodelist=nx_nodes)
            nx.draw_networkx_nodes(G, pos, nodelist=nx_nodes_min, node_color="#fc2003")
            nx.draw_networkx_nodes(
                G, pos, nodelist=nx_nodes_hollow, node_color="#7d7978"
            )
            nx.draw_networkx_edges(G, pos, edgelist=child)
            nx.draw_networkx_edges(
                G, pos, edgelist=ep_child, arrows=False, style="dashed"
            )
            nx.draw_networkx_labels(G, pos, labels=label_dict)

            plt.title(title)
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


# Print nodes information as a table
def print_nodes(nodes):
    for n in nodes:
        output = ""
        if n is not None:
            output += f"Key: {n.key:02d} -> "
            output += f"  r: {n.right.key:02d}" if n.right is not None else "  r:  -"
            output += f"  c: {n.child.key:02d}" if n.child is not None else "  c:  -"
            output += (
                f"  p: {n.parent.key:02d}"
                if hasattr(n, "parent") and n.parent is not None
                else "  p:  -"
            )
            output += (
                f"  ep: {n.ep.key:02d}"
                if hasattr(n, "ep") and n.ep is not None
                else "  ep:  -"
            )
        print(output)

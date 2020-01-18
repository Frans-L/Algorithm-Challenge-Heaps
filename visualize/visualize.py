from visualize.misc import hierarchy_pos
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import queue

# Draw the heap as a graph.
# If file_name is given, the graph will be saved as a file.
def visualize(_heap, title="Heap", debug_print=True, file_name=None):
    nodes = _find_nodes(_heap)
    G = nx.DiGraph()
    label_dict = {}  # maps nodes to their labels

    def add_nodes():
        for n in nodes:
            # set style and label
            label_dict[n] = n.key
            style = "normal" if n is not _heap.find_min() else "min"
            # override if hollow node (hollow heap)
            if hasattr(n, "item") and n.item is None:
                label_dict[n] = ""
                style = "hollow"

            G.add_node(n, style=style)

    def add_edges():
        isChild = set()  # used to find root level
        for n in nodes:
            c = n.child
            if c is None:
                continue

            childs = _find_layer(c)
            for m in childs:
                isChild.add(m)
                # is child of extra parent (hollow heap)
                if hasattr(m, "ep") and m.ep == n:
                    G.add_edge(n, m, style="ep_child")
                else:
                    G.add_edge(n, m, style="child")

        # add hidden root node, to make visualization easier
        G.add_node("root", style="hidden")
        label_dict["root"] = f""
        for n in nodes:
            if n not in isChild:
                G.add_edge("root", n, style="root")

    # Draw graph as a tree.
    # If fails, draw it as a normal graph.
    def draw_graph():
        layouts = [hierarchy_pos, nx.spring_layout]
        for l in layouts:
            try:
                _draw_graph_with_layout(l)
                break
            except BaseException:
                print("WARNING: Drawing failed, trying different layout.")

    def _draw_graph_with_layout(layout):
        pos = layout(G)
        nx_nodes = [n for (n, d) in G.nodes(data=True) if d["style"] == "normal"]
        nx_nodes_min = [n for (n, d) in G.nodes(data=True) if d["style"] == "min"]
        nx_nodes_hollow = [n for (n, d) in G.nodes(data=True) if d["style"] == "hollow"]
        child = [(u, v) for (u, v, d) in G.edges(data=True) if d["style"] == "child"]
        ep_child = [
            (u, v) for (u, v, d) in G.edges(data=True) if d["style"] == "ep_child"
        ]

        nx.draw_networkx_nodes(G, pos, nodelist=nx_nodes)
        nx.draw_networkx_nodes(G, pos, nodelist=nx_nodes_min, node_color="#fc2003")
        nx.draw_networkx_nodes(G, pos, nodelist=nx_nodes_hollow, node_color="#7d7978")
        nx.draw_networkx_edges(G, pos, edgelist=child)
        nx.draw_networkx_edges(G, pos, edgelist=ep_child, arrows=False, style="dashed")
        nx.draw_networkx_labels(G, pos, labels=label_dict)

        plt.title(title)
        if file_name is not None:
            plt.savefig(f"visualize/visual_output/{file_name}")
        plt.show()

    # print all node data
    if debug_print:
        _debug_print_nodes(nodes, title)

    add_nodes()
    add_edges()
    draw_graph()


# Gather all nodes to one list.
def _find_nodes(heap):
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


# Return all elements under same parent as a list
def _find_layer(node):
    items = []
    n = stop = node
    first_loop = True
    while n is not None and (first_loop or n != stop):
        first_loop = False
        items.append(n)
        n = n.right
    return items


# Print the graph as a table
def _debug_print_nodes(nodes, title):
    print("-" * 40)
    print(title)
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

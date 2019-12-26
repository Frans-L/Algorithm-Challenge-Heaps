from heaps.hollow import HollowHeap
from heaps.fibonacci import FibonacciHeap
from visualize import visualize

# Visual examples how FibonacciHeap and HollowHeap works.
# The code halts while a graph window is open. To continue,
# close the graph window.

# HollowHeap and FibonacciHeap do not require any
# extra packages. But the visualization requires some
# packages. You can install them by running:
# > pip install -r visual_requirements.txt


def example_run(heap_type, title):
    heap = heap_type()

    nodes = []
    values = [22, 16, 8, 13, 4, 12, 6, 5, 11]
    for n in values:
        node = heap.insert(n)
        nodes.append(node)
    visualize(heap, title=title + ": 1. Inserted values - " + str(values))

    heap.delete_min()
    visualize(heap, title=title + ": 2. Deleted the minimum node (node 4)")

    heap.delete_min()
    visualize(heap, title=title + ": 3. Deleted the minimum node (node 5)")

    nodes[0] = heap.decrease_key(nodes[0], 10)
    visualize(heap, title=title + ": 4. Decreased the value of the node 22 to 10")

    heap.delete_min()
    visualize(heap, title=title + ": 5. Deleted the minimum node (node 6)")

    heap.delete(nodes[0])
    visualize(heap, title=title + ": 6. Deleted the non-minumum node 10")

    heap2 = heap_type()
    values = [32, 10, 15]
    for n in values:
        node = heap2.insert(n)
    heap.merge(heap2)
    visualize(heap, title=title + ": 7. Merged with another heap - " + str(values))


if __name__ == "__main__":
    print("--- Running FibonacciHeap ---")
    example_run(FibonacciHeap, "Fibonacci")

    print("--- Running HollowHeap ---")
    example_run(HollowHeap, "Hollow")

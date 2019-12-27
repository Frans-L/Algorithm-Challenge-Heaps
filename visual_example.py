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

# The graphs are also saved as .png images into to the folder
# visual_output/.


def example_run(heap_type, title):
    heap = heap_type()

    # add nodes to empty heap
    nodes = []
    values = [22, 16, 8, 13, 4, 12, 6, 5, 11]
    for n in values:
        node = heap.insert(n)
        nodes.append(node)
    visualize(
        heap,
        title=title + ": 1. Inserted values - " + str(values),
        file_name=title + "1.png",
    )

    # delete min, first time
    heap.delete_min()
    visualize(
        heap,
        title=title + ": 2. Deleted the minimum node (node 4)",
        file_name=title + "2.png",
    )

    # delete min, second time
    heap.delete_min()
    visualize(
        heap,
        title=title + ": 3. Deleted the minimum node (node 5)",
        file_name=title + "3.png",
    )

    # decrease key
    nodes[0] = heap.decrease_key(nodes[0], 10)
    visualize(
        heap,
        title=title + ": 4. Decreased the value of the node 22 to 10",
        file_name=title + "4.png",
    )

    # delete min after decrease key
    heap.delete_min()
    visualize(
        heap,
        title=title + ": 5. Deleted the minimum node (node 6)",
        file_name=title + "5.png",
    )

    # delete non minimum
    heap.delete(nodes[0])
    visualize(
        heap,
        title=title + ": 6. Deleted the non-minumum node 10",
        file_name=title + "6.png",
    )

    # merge with another heap
    heap2 = heap_type()
    values = [32, 10, 15]
    for n in values:
        node = heap2.insert(n)
    heap.merge(heap2)
    visualize(
        heap,
        title=title + ": 7. Merged with another heap - " + str(values),
        file_name=title + "7.png",
    )


if __name__ == "__main__":
    print("--- Running FibonacciHeap ---")
    example_run(FibonacciHeap, "Fibonacci")

    print("--- Running HollowHeap ---")
    example_run(HollowHeap, "Hollow")

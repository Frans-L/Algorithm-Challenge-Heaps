from hollow import HollowHeap
from fibonacci import FibonacciHeap
from visualize import visualize


# Example commands to a heap and their visualization.
# The code will stop running while visualization.
# To go forward, the appeared window must be closed
def example_run(heap, title):
    values = [22, 16, 8, 13, 4, 12, 6, 5, 11]
    nodes = []

    for n in values:
        node = heap.insert(n)
        nodes.append(node)

    visualize(heap, title=title + ": 1. Inserted values")

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


if __name__ == "__main__":
    print("--- Running FibonacciHeap ---")
    example_run(FibonacciHeap(), "Fibonacci")

    print("--- Running HollowHeap ---")
    example_run(HollowHeap(), "Hollow")

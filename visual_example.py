import random
from visualize.visualize import visualize
from abstract_heap import Heap
from hollow_heap import HollowHeap
from fibonacci_heap import FibonacciHeap

# Visual step by step example about deleting nodes
# from FibonacciHeap and HollowHeap.

# Install prerequirements:
# > pip install -r visual_requirements.txt

max_key = 15
node_amount = 15
delete_amount = 10


def visual_delete_one_by_one(heap_type, title):
    heap = heap_type()

    # generate random numbers and add them to the heap
    nodes = []
    values = random.sample(range(max_key), node_amount)
    for n in values:
        node = heap.insert(n)  # add node to heap
        nodes.append(node)
    visualize(
        heap,
        title=f"{title}: 0. Inserted values",
        highlight=min(nodes, key=lambda n: n.key),
    )

    # remove nodes from heap one be one
    nodes = sorted(nodes, key=lambda n: n.key, reverse=True)
    delete_next = nodes.pop()
    for i in range(1, delete_amount + 1):
        heap.delete(delete_next)
        if i % 3 == 0:
            delete_next = nodes.pop()
        else:
            delete_next = nodes.pop(random.randrange(len(nodes)))

        visualize(
            heap,
            title=f"{title}: {i}. Deleting the node {delete_next.key}",
            highlight=delete_next,
        )


if __name__ == "__main__":
    random_seed = 3

    print("--- Running FibonacciHeap ---")
    random.seed(random_seed)
    visual_delete_one_by_one(FibonacciHeap, "Fibonacci")

    print("--- Running HollowHeap ---")
    random.seed(random_seed)
    visual_delete_one_by_one(HollowHeap, "Hollow")

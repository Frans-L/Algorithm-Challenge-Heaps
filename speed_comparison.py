from heaps.hollow import HollowHeap
from heaps.fibonacci import FibonacciHeap
import random
import timeit

# few basic speed test


def insert_test(heap_type, scale):
    random.seed(1)
    heap = heap_type()
    start = timeit.default_timer()
    for _ in range(scale):
        heap.insert(random.random())
    end = timeit.default_timer()

    print("Insert:", end - start)


def delete_min_test(heap_type, scale):
    random.seed(1)
    heap = heap_type()

    for _ in range(scale + 1):
        heap.insert(random.random())

    start = timeit.default_timer()
    for _ in range(scale):
        heap.delete_min()
    end = timeit.default_timer()

    print("Delete min:", end - start)


def delete_test(heap_type, scale):
    random.seed(1)
    heap = heap_type()

    nodes = []
    for _ in range(scale):
        nodes.append(heap.insert(random.random()))

    start = timeit.default_timer()
    for i in range(scale):
        heap.delete(nodes[i])
    end = timeit.default_timer()

    print("Delete:", end - start)


def decrease_test(heap_type, scale):
    random.seed(1)
    heap = heap_type()

    nodes = []
    for _ in range(scale + 1):
        nodes.append(heap.insert(random.random()))

    random.shuffle(nodes)
    start = timeit.default_timer()
    for i in range(scale):
        heap.decrease_key(nodes[i], nodes[i].key - random.random())
    end = timeit.default_timer()

    print("Decrease", end - start)


# mixing insert, delte, decrease_key
def mixed_test(heap_type, scale):
    random.seed(1)
    heap = heap_type()

    # insert min elements
    for _ in range(int(scale / 4)):
        heap.insert(-random.random())

    # insert base nodes
    nodes = []
    for _ in range(scale + 1):
        nodes.append(heap.insert(random.random()))

    # start testing
    random.shuffle(nodes)
    start = timeit.default_timer()
    for i in range(scale):
        if i % 4 == 0:
            heap.insert(random.random())
        elif i % 4 == 1:
            heap.delete_min()
        elif i % 4 == 2:
            heap.delete(nodes[i])
        else:
            heap.decrease_key(nodes[i], nodes[i].key - random.random())

    end = timeit.default_timer()
    print("Mixed", end - start)


def all_tests(heap_type):
    scale = 10 ** 5
    insert_test(heap_type, scale)
    delete_test(heap_type, scale)
    delete_min_test(heap_type, scale)
    decrease_test(heap_type, scale)
    mixed_test(heap_type, scale)


if __name__ == "__main__":
    print("--- Running FibonacciHeap ---")
    all_tests(FibonacciHeap)

    print("--- Running HollowHeap ---")
    all_tests(HollowHeap)

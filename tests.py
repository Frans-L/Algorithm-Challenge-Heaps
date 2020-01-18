import unittest
import random
from hollow_heap import HollowHeap
from fibonacci_heap import FibonacciHeap

random_seed = 1

# Tests methods of the both heaps, Fibonacci heap and Hollow heap
class TestHeaps(unittest.TestCase):
    # tests if insert() works
    def insert_key_test(self, heap_type):
        heap = heap_type()
        for k in [-10, 0, 10, -1.1, 1.1]:
            n = heap.insert(k)
            self.assertEqual(n.key, k)
            self.assertEqual(n.val, k)

    # tests if insert() support parameter .val properly
    def insert_key_value_test(self, heap_type):
        heap = heap_type()
        for k, v in [(-10, 0), (0, "A"), (10, [1, 2]), (-1.1, {}), (1.1, 1.1)]:
            n = heap.insert(k, v)
            self.assertEqual(n.key, k)
            self.assertEqual(n.val, v)

    # tests if find_min() returns the min node
    def find_min_test(self, heap_type):
        heap = heap_type()
        random.seed(random_seed)
        keys = random.sample(range(-1000, 1000), 100)
        added_keys = []
        for k in keys:
            added_keys.append(k)
            heap.insert(k)
            self.assertEqual(heap.find_min().key, min(added_keys))

    # tests if delete_min() deletes the min node
    def delete_min_test(self, heap_type):
        heap = heap_type()
        random.seed(random_seed)
        keys = random.sample(range(-1000, 1000), 100)
        for k in keys:
            heap.insert(k)
        keys = sorted(keys)

        while len(keys) > 0:
            min_key = keys.pop(0)
            heap_min = heap.delete_min()
            self.assertEqual(heap_min.key, min_key)

    # tests if delete() works, and find_min() returns min node
    def delete_test(self, heap_type):
        heap = heap_type()
        random.seed(random_seed)
        keys = random.sample(range(-1000, 1000), 100)
        nodes = []
        for k in keys:
            nodes.append(heap.insert(k))

        while len(nodes) > 1:
            node = nodes.pop(random.randrange(len(nodes)))
            heap.delete(node)
            self.assertEqual(heap.find_min(), min(nodes, key=lambda n: n.key))

    # tests if decrease_key() works, and find_min() returns correct min node
    def decrease_key_test(self, heap_type):
        heap = heap_type()
        random.seed(random_seed)
        keys = random.sample(range(-1000, 1000), 100)
        nodes = []
        for k in keys:
            nodes.append(heap.insert(k))

        for _ in range(100):
            index = random.randrange(len(nodes))
            key_new = nodes[index].key - random.randint(1, 1000)
            nodes[index] = heap.decrease_key(nodes[index], key_new)
            self.assertEqual(nodes[index].key, key_new)
            self.assertEqual(heap.find_min(), min(nodes, key=lambda n: n.key))

    # tests if merge() works, and find_min() returns correct min node
    def merge_test(self, heap_type):
        heap = heap_type()
        random.seed(random_seed)

        heap.insert(1)
        all_keys = [1]
        for _ in range(10):
            new_heap = heap_type()
            keys = random.sample(range(-1000, 1000), 100)
            for k in keys:
                new_heap.insert(k)

            heap.merge(new_heap)
            all_keys.extend(keys)
            self.assertEqual(heap.find_min().key, min(all_keys))

    def test_fibo_insert(self):
        self.insert_key_test(FibonacciHeap)
        self.insert_key_value_test(FibonacciHeap)

    def test_hollow_insert(self):
        self.insert_key_test(HollowHeap)
        self.insert_key_value_test(HollowHeap)

    def test_fibo_find_min(self):
        self.find_min_test(FibonacciHeap)

    def test_hollow_find_min(self):
        self.find_min_test(HollowHeap)

    def test_fibo_delete_min(self):
        self.delete_min_test(FibonacciHeap)

    def test_hollow_delete_min(self):
        self.delete_min_test(HollowHeap)

    def test_fibo_delete(self):
        self.delete_test(FibonacciHeap)

    def test_hollow_delete(self):
        self.delete_test(HollowHeap)

    def test_fibo_decrease_key(self):
        self.decrease_key_test(FibonacciHeap)

    def test_hollow_decrease_key(self):
        self.decrease_key_test(HollowHeap)

    def test_fibo_merge(self):
        self.merge_test(FibonacciHeap)

    def test_hollow_merge(self):
        self.merge_test(HollowHeap)


if __name__ == "__main__":
    unittest.main()

# Fibonacci Heap & Hollow Heap

Python 3 implementations of a Fibonacci heap and a Hollow heap.

Both are data structures for priority queue operations, in which you can find e.g. the minimum value with time complexity O(1).

### Amortized Time Complexity

The special thing about Fibonacci Heap and Hollow Heap is their low amortized time complexity.

For instance, the amortized running times are lower than _binary heap_ or _binomial heap_ has.

| Method       | Fibonacci | Hollow   | Binary   | Binomial |
| ------------ | --------- | -------- | -------- | -------- |
| find_min     | O(1)      | O(1)     | O(1)     | O(1)     |
| insert       | O(1)      | O(1)     | O(log n) | O(1)     |
| delete       | O(log n)  | O(log n) | O(log n) | O(log n) |
| decrease_key | O(1)      | O(1)     | O(log n) | O(log n) |
| merge        | O(1)      | O(1)     | O(n)     | O(log n) |

### Fibonacci Heap

The Fibonacci heap uses multiple trees. Every node has degree at most _log(n)_ and the size of subtrees are related to Fibonacci sequence. You can read more about from [Wikipedia](https://en.wikipedia.org/wiki/Fibonacci_heap).

Here is a visualiation of the Fibonacci heap when nodes are deleted.

<p align="center">
  <img src="https://github.com/Frans-L/Code-Challenge-Hollow-Fibo/blob/master/visualize/fibonacci.gif?raw=true" alt="Deleting nodes"/>
</p>

### Hollow Heap

The Hollow heap achives the same running times as the Fibonacci heap by using lazy deletion and a directed acyclic graph instead of a tree. You can read more about from the white paper [Hollow Heaps](https://arxiv.org/abs/1510.06535).

Here is a visualiation of the Hollow heap when nodes are deleted.

<p align="center">
  <img src="https://github.com/Frans-L/Code-Challenge-Hollow-Fibo/blob/master/visualize/hollow.gif?raw=true" alt="Deleting nodes"/>
</p>

### How To Use

```python
from hollow_heap import HollowHeap
from fibonacci_heap import FibonacciHeap

# Create an empty heap
heap = FibonacciHeap()  # = HollowHeap()

# Insert a node with properties
#   key = 10
#   val = 10
node10 = heap.insert(10)

# Insert a node with properties
#   key = 12
#   val = "B"
nodeB = heap.insert(12, "B")

# Return the smallest node, node10
n = heap.find_min()

# Decrease the key of node nodeB
nodeB = heap.decrease_key(nodeB, 3)

# Delete the nodeB
heap.delete(nodeB)

# Delete the min node, node10
heap.delete_min()

# Merge heap2 into heap
heap2 = FibonacciHeap()  # = HollowHeap()
heap2.insert(8)
heap.merge(heap2)

```

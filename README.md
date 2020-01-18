# Coding Challenge: Fibonacci Heap & Hollow Heap

Here are implementations of a Fibonacci heap and a Hollow heap.

Both are data structures for priority queue operations. The special thing is that their amortized running times are really great. The amortized running times are lower than _binary heap_ or _binomial heap_ has.

### Amortized Time Complexity

| Method       | Time complexity |
| ------------ | --------------- |
| find_min     | O(1)            |
| insert       | O(1)            |
| delete_min   | O(log n)        |
| delete       | O(log n)        |
| decrease_key | O(1)            |
| merge        | O(1)            |

The both heaps achieves the same amortized running times but with different approach.

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

### Example

```python
from hollow_heap import HollowHeap
from fibonacci_heap import FibonacciHeap

# Create the heap
heap = FibonacciHeap()  # = HollowHeap()

# Insert node with properties
#   .key = 10
#   .val = 10
node10 = heap.insert(10)

# Insert node with properties
#   .key = 12
#   .val = "B"
nodeB = heap.insert(12, "B")

# Return the smallest node, node10
n = heap.find_min()

# Decrease the key of node nodeB
nodeB = heap.decrease_key(nodeB, 3)

# Deletes the nodeB
heap.delete(nodeB)

# Deletes the min node, node10
heap.delete_min()

# Merges heap2 into heap
heap2 = FibonacciHeap()  # = HollowHeap()
heap2.insert(8)
heap.merge(heap2)

```

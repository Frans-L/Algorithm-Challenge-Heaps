from heaps.hollow import HollowHeap
from heaps.fibonacci import FibonacciHeap

# List of all commands with a simple example
# NOTE: Recommend to try "visual_example.py" to see what is happening

# Create heaps
fibo = FibonacciHeap()
hollow = HollowHeap()

# Inserts key (key) or key and value (key, value)
# returns the inserted node
f1 = fibo.insert(10)
f2 = fibo.insert(5)
f3 = fibo.insert(7)
h1 = hollow.insert(10)
h2 = hollow.insert(5)
h3 = hollow.insert(7)

# Finds the minimum node
# returns the minimum node
m1 = fibo.find_min()
m2 = hollow.find_min()

# Deletes the minimum node
fibo.delete_min()
hollow.delete_min()

# Deletes the given node
fibo.delete(f1)
hollow.delete(h1)

# Decrease the key to given value
# returns updated node
f3 = fibo.decrease_key(f3, 2)
h3 = hollow.decrease_key(h3, 2)

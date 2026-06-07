# Attempt 030 - 2026-06-06T21:32:24.475963+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource Limit Race in sorted()
# Fill memory to near limit, then sort - MemoryError mid-sort may corrupt state

# First, allocate to near limit (1MB = ~130000 integers)
# Leave room for sort overhead
base = [0] * 100000
print("Base allocation: 100000")

# Create items to sort - tuples compare by elements
items = []
for i in range(500):
    items.append((i % 100, i, i * 2))

print("Items to sort:", len(items))

# Try sort - this should work
try:
    result = sorted(items)
    print("Sort 1 succeeded")
except MemoryError as e:
    print("Sort 1 MemoryError:", str(e)[:60])

# Allocate more to push closer to limit
base2 = [0] * 20000
print("Added 20000 more")

# Create more items
items2 = []
for i in range(1000):
    items2.append((i % 50, -i, i))

print("Items2 to sort:", len(items2))

# Try sort near limit
try:
    result2 = sorted(items2)
    print("Sort 2 succeeded, len:", len(result2))
    # Verify
    for i in range(len(result2) - 1):
        if result2[i] > result2[i + 1]:
            print("CORRUPTION at", i)
            break
    else:
        print("Sort 2 verified OK")
except MemoryError as e:
    print("Sort 2 MemoryError:", str(e)[:60])

# Allocate even more
base3 = [0] * 10000
print("Added 10000 more")

# Final sort attempt
items3 = list(range(2000))
items3.reverse()  # Worst case for some sort algos
print("Items3 (reversed):", len(items3))

try:
    result3 = sorted(items3)
    print("Sort 3 succeeded")
    if result3[0] == 0 and result3[-1] == 1999:
        print("Sort 3 correct")
    else:
        print("SORT CORRUPTION: first=", result3[0], "last=", result3[-1])
except MemoryError as e:
    print("Sort 3 MemoryError:", str(e)[:60])
```

## Result
Context: AllocRace - MemoryError during allocation before sort could run
Score: 0/5 - Nothing - standard error or expected sandbox behavior

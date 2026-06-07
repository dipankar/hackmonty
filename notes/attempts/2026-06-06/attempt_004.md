# Attempt 003 - 2026-06-06T19:36:52.845719+00:00
## Template: G | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template G: Resource Limit Race in sorted()
# Fill allocation counter, then sort to trigger MemoryError mid-sort

# Pre-allocate to drift counter near limit
print('Phase 1: Pre-allocating...')
buffers = []
for i in range(400):
    buffers.append([0] * 1000)
print('Buffers allocated:', len(buffers))

# Create a large list to sort
print('Phase 2: Creating sort target...')
items = list(range(1000, 0, -1))
print('Items to sort:', len(items))

# Try to sort - might hit MemoryError mid-sort
print('Phase 3: Sorting...')
try:
    items.sort()
    print('Sort succeeded')
    print('First 5:', items[:5])
    print('Last 5:', items[-5:])
    print('Length after sort:', len(items))
except MemoryError as e:
    print('MemoryError during sort:', e)
    # Check if list is corrupted
    print('List length after error:', len(items))
    print('List type:', type(items))
    # Try to access elements
    try:
        print('First element:', items[0])
    except Exception as ex:
        print('Cannot access elements:', ex)

# Try another operation to see if VM is stable
print('Phase 4: Stability check...')
x = [1, 2, 3]
x.sort()
print('Small sort works:', x)
```

## Result
Context: MemoryError: memory limit exceeded: 1059296 bytes > 1048576 bytes; mem(1059296/1048576)
Score: 0/5 - Nothing - standard error or expected sandbox behavior

# Attempt 075 - 2026-06-06T22:09:39.391137+00:00
## Template: E | Score: 0 - Nothing - standard error or expected sandbox behavior
## Exploit code
```python
# Template E: MemDrift - exploit allocation/free mismatch
# on_free uses saturating_sub, might create ghost memory

print("=== MemDrift Test ===")

# Create many large lists, then let them go out of scope
def create_and_free():
    big_lists = []
    for i in range(100):
        big_lists.append([0] * 1000)
    print(f"Created {len(big_lists)} lists of 1000 zeros")
    # Let them go out of scope when function returns

create_and_free()
print("Lists freed (out of scope)")

# Now try to allocate - if drift worked, we have more headroom
print("\nTrying large allocations after free:")
try:
    # Try to allocate something large
    huge = [0] * 50000
    print(f"Allocated list of {len(huge)} zeros")
except MemoryError as e:
    print(f"MemoryError: {e}")

# Try multiple allocations
allocations = []
for i in range(20):
    try:
        alloc = [0] * 10000
        allocations.append(alloc)
        print(f"Allocation {i+1}: {len(alloc)} items")
    except MemoryError:
        print(f"MemoryError at allocation {i+1}")
        break

print(f"\nTotal successful allocations: {len(allocations)}")
print("Done")
```

## Result
Context: MemoryError hit at 1059328 bytes, no drift exploited
Score: 0/5 - Nothing - standard error or expected sandbox behavior

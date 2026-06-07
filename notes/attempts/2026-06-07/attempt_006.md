# Attempt 137 - 2026-06-07T10:14:15.005328+00:00
## Template: C | Score: 0 - Nothing - completed normally
## Exploit code
```python
import sys

def safe_sorted_test():
    data = [i for i in range(120)]
    saved = data[:]
    def heavy_key(x):
        _ = [j for j in range(400)]
        _ = {k: k for k in range(200)}
        _ = (x * y for y in range(100))
        return 0
    try:
        out = sorted(data, key=heavy_key)
        print("OK: sorted completed")
    except MemoryError:
        print("MemoryError during sorted key computation")
        if data == saved:
            print("Data intact after MemoryError")
        else:
            print("DATA CORRUPTED!")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")

def min_mutation_test():
    nums = [4, 2, 7, 1, 5]
    saved = nums[:]
    def mutator(x):
        if x == 2:
            nums.clear()
            nums.extend([99, 88, 77])
        return x
    try:
        result = min(nums, key=mutator)
        print(f"min result: {result}")
    except Exception as e:
        print(f"min error: {type(e).__name__}: {e}")
    print(f"nums changed: {saved} -> {nums}")

safe_sorted_test()
min_mutation_test()
```

## Result
Context: Template C SortCmp - sorted with key= completed, min with mutation changed list but result was still old min
Score: 0/5 - Nothing - completed normally

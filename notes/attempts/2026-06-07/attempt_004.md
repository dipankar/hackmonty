# Attempt 135 - 2026-06-07T09:18:07.447207+00:00
## Template: A | Score: 0 - Nothing
## Exploit code
```python
import json

d = {}
for i in range(10):
    d[i] = i

def f(k):
    for i in list(d.keys()):
        d[i] = d[i] * 2
    return d[k]

try:
    r = max(d, key=f)
    print(json.dumps({"vulnerable": True, "result": r}))
except RuntimeError as e:
    print(json.dumps({"vulnerable": False, "error": str(e)}))
```

## Result
Context: Template A DictReentry - max(dict, key=...) with key function mutating dict. checks_mutation caught size change? Actually no size change since values just multiplied. But max() completed normally, no corruption.
Score: 0/5 - Nothing

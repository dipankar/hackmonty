# Traceback
## Last updated: 2026-06-03T13:11:58.293314+00:00
## Confidence: LOW (from automated probing)

### What we observed
- Score 3: Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; NotImplementedError: The monty syntax parser does not yet support the 'del' statement
Traceback: Traceback (most recent call last):
  File "main.py", line 19, in <module>
    del temp
    ~~~~~~~~
NotImplementedError: The monty syntax parser does not yet support the 'del' statement
- Code that triggered this: import sys
import os
from pathlib import Path

results = []
gc_events = []
secret_leaks = []

# === UTILITY: Force GC pressure ===
def create_gc_pressure(n=500):
    """Create and drop objects to trigger tracing GC"""
    temp = []
    for i in range(n):
        # Create cycles that tracing GC must ...


## Update: 2026-06-03T13:20:54.423377+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 93, in <module>
    mapped = list(map(gc_map, map_data))
                  ~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 88, in gc_map
    gc_pressure(250)
    ~~~~~~~~~~~~~~~~
  File "main.py", line 13, in gc_pressure
    b = {'cycle': a, 'data': 'Y' * 50, 'id': i + 1000}
                                             ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T13:24:52.649513+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 58, in <module>
    s = f"INTERN_TEST_STRING_{i:05d}_PAD_" + "X" * 50
                                             ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T13:25:39.558281+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: memory limit exceeded: 1048582 bytes > 1048576 bytes
Traceback: Traceback (most recent call last):
  File "main.py", line 89, in <module>
    test_list = [i * 2 for i in range(size)]
                 ~~~~~
MemoryError: memory limit exceeded: 1048582 bytes > 1048576 bytes


## Update: 2026-06-03T14:18:45.155089+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 33, in <module>
    result = sorted(objects, key=pure_gc_key)
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 27, in pure_gc_key
    gc_pressure(350)
    ~~~~~~~~~~~~~~~~
  File "main.py", line 14, in gc_pressure
    b = {'cycle': a, 'data': 'Y' * 50, 'id': i + 1000}
                             ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:20:28.680702+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 66, in <module>
    create_gc_storm(50)
    ~~~~~~~~~~~~~~~~~~~
  File "main.py", line 14, in create_gc_storm
    node = {'prev': None, 'next': None, 'data': 'D' * 30, 'iter': iteration}
                                                ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:27:57.365553+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 41, in <module>
    alloc_objects.append(count_alloc())
                         ~~~~~~~~~~~~~
  File "main.py", line 12, in count_alloc
    return {'id': alloc_counter[0], 'pad': 'P' * 20}
                                           ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:28:30.059399+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 67, in <module>
    batch_objs = [alloc_tracker() for _ in range(45)]  # 45 per batch
                  ~~~~~~~~~~~~~~~
  File "main.py", line 11, in alloc_tracker
    return {'id': allocation_count[0], 'data': 'X' * 100}
                                               ~~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:29:18.804010+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 60, in <module>
    pressure_data.append({'id': i, 'pad': 'P' * 100})
                                          ~~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:31:54.319213+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 89, in <module>
    gc_burst(30)
    ~~~~~~~~~~~~
  File "main.py", line 29, in gc_burst
    a = {'data': 'X' * 50, 'i': i}
                 ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:33:50.367372+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 240, in <module>
    result = sorted(exhaust_data, key=exhaust_key)
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 232, in exhaust_key
    temp.append({'k': exhaust_counter[0], 'v': i, 'pad': 'E' * 50})
                                                         ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T14:49:05.117954+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 93, in <module>
    count = mem_exhaust_and_read(f'T{target}', target)
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 65, in mem_exhaust_and_read
    big_list.append({'id': i, 'data': 'M' * 100})
                                      ~~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T15:25:40.869225+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 115, in <module>
    result = list(map(gc_map_func, map_data))
                  ~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 109, in gc_map_func
    gc_pressure(200)
    ~~~~~~~~~~~~~~~~
  File "main.py", line 12, in gc_pressure
    a = {'cycle': None, 'data': 'X' * 30, 'id': i}
                                                ~
MemoryError: allocation limit exceeded: 500


## Update: 2026-06-03T15:26:52.995367+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 127, in <module>
    result = list(filter(gc_filter_callback, filter_data))
                  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 47, in gc_filter_callback
    gc_pressure(300)
    ~~~~~~~~~~~~~~~~
  File "main.py", line 13, in gc_pressure
    a = {'data': 'X' * 30, 'id': i}
                                 ~
MemoryError: allocation limit exceeded: 5


## Update: 2026-06-03T15:33:23.779888+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 125, in <module>
    interning_attack(sp)
    ~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 102, in interning_attack
    s = f"INTERN_STRING_{i:05d}_PAD_" + base[:30]
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T15:34:36.980195+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: memory limit exceeded: 1050563 bytes > 1048576 bytes
Traceback: Traceback (most recent call last):
  File "main.py", line 240, in <module>
    result = mem_exhaust_and_probe('MEM_PHASE_1', 0.8)
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 21, in mem_exhaust_and_probe
    chunk = {'id': i, 'data': 'M' * 2000}
                              ~~~~~~~~~~
MemoryError: memory limit exceeded: 1050563 bytes > 1048576 bytes


## Update: 2026-06-03T15:35:24.720813+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; RecursionError: maximum recursion depth exceeded
Traceback: Traceback (most recent call last):
  File "main.py", line 263, in <module>
    exception_chain_attack()
    ~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 215, in exception_chain_attack
    secrets.append(f"POST_EXC_{sp}: {c[:100]}")
RecursionError: maximum recursion depth exceeded


## Update: 2026-06-03T16:05:53.732365+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 52, in <module>
    sorted_gc_attack()
    ~~~~~~~~~~~~~~~~~~
  File "main.py", line 39, in sorted_gc_attack
    result = sorted(data, key=gc_key)
             ~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 29, in gc_key
    a = {'cycle': None, 'data': 'X' * 20, 'id': i}
                                ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T16:19:02.275602+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 164, in <module>
    print_overflow_attack()
    ~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 136, in print_overflow_attack
    line = f"LINE_{i:05d}_" + "X" * 100
                   ~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T16:25:03.332879+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: memory limit exceeded: 1048584 bytes > 1048576 bytes
Traceback: Traceback (most recent call last):
  File "main.py", line 55, in <module>
    mem_exhaust_and_read(f"PHASE1", sp)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 31, in mem_exhaust_and_read
    chunk = {'id': i, 'data': 'M' * 200}
                              ~~~~~~~~~
MemoryError: memory limit exceeded: 1048584 bytes > 1048576 bytes


## Update: 2026-06-03T16:33:05.230455+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T16:55:50.863623+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 63, in <module>
    r = probe_at_boundary(target)
        ~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 36, in probe_at_boundary
    alloc_and_count(20)
    ~~~~~~~~~~~~~~~~~~~
  File "main.py", line 30, in alloc_and_count
    _ = {'id': alloc_count[0], 'pad': 'A' * 50}
                                      ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T16:57:34.087196+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T16:58:42.474208+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 93, in <module>
    alloc_results = alloc_exhaust_during_read()
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 87, in alloc_exhaust_during_read
    result = pressure_and_read(sp)
             ~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 71, in pressure_and_read
    obj = {'id': i, 'pad': 'A' * 50, 'path': path}
                                          


## Update: 2026-06-03T17:06:34.556994+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 62, in <module>
    phase1_results = gc_during_external_call()
                     ~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 31, in gc_during_external_call
    a = {'id': i, 'iter': iteration, 'pad': 'S' * 20}
                                            ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T17:39:00.840657+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 55, in <module>
    result = alloc_and_read(sp)
             ~~~~~~~~~~~~~~~~~~
  File "main.py", line 32, in alloc_and_read
    obj = {'id': alloc_count[0], 'pad': 'A' * 30}
                                        ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T17:47:18.669198+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 46, in <module>
    save(f'RAPID_ERR_{iteration}', err_str[:120])
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  File "main.py", line 15, in save
    secrets.append(f"{label}: {preview}")
                      ~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T18:15:24.287743+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 123, in <module>
    gc_pool.append({'iter': iteration, 'i': i, 'pad': 'G' * 20})
                                                      ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T18:26:06.428972+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 33, in <module>
    alloc_pool.append(alloc_one())
                      ~~~~~~~~~~~
  File "main.py", line 28, in alloc_one
    return {'id': alloc_count[0], 'pad': 'X' * 50}
                                         ~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000


## Update: 2026-06-03T18:27:34.013738+00:00 (Score 3)
- Host Info - Rust traceback, OS details, file paths, binary info leaked
- Got a traceback/backtrace; MemoryError: allocation limit exceeded: 5001 > 5000
Traceback: Traceback (most recent call last):
  File "main.py", line 87, in <module>
    output_buffer.append(f"BUFFER_{iteration}_{i}_" + "Y" * 100)
                         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
MemoryError: allocation limit exceeded: 5001 > 5000

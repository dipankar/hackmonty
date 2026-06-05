"""One-time static scan of Monty Rust source for attack surface.

Scans /tmp/monty-source/crates/monty/src/ for:
- unsafe blocks/functions (count, key locations)
- #[pyfunction] decorators
- extern "C" FFI boundaries  
- Functions accepting &mut VM (callback entry points)

Writes results to notes/source_scan.json for template generation.
"""

import json, re, os
from pathlib import Path
from collections import defaultdict


MONTY_SRC = "/tmp/monty-source/crates/monty/src"


def scan_unsafe_blocks():
    """Find all unsafe blocks and functions."""
    results = []
    for root, dirs, files in os.walk(MONTY_SRC):
        for f in files:
            if not f.endswith(".rs"):
                continue
            path = Path(root) / f
            content = path.read_text(errors="replace")
            lines = content.split("\n")

            # Count unsafe blocks
            unsafe_blocks = []
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("unsafe fn"):
                    unsafe_blocks.append((i, "fn", stripped))
                elif "unsafe {" in stripped:
                    unsafe_blocks.append((i, "block", stripped[:80]))

            if unsafe_blocks:
                results.append({
                    "file": str(path.relative_to(MONTY_SRC)),
                    "count": len(unsafe_blocks),
                    "locations": unsafe_blocks[:10],  # first 10
                })

    return results


def scan_pyfunctions():
    """Find all #[pyfunction] or #[pymethod] decorated functions."""
    results = []
    for root, dirs, files in os.walk(MONTY_SRC):
        for f in files:
            if not f.endswith(".rs"):
                continue
            path = Path(root) / f
            content = path.read_text(errors="replace")
            if "#[pyfunction]" in content or "#[pymethod]" in content:
                rel = str(path.relative_to(MONTY_SRC))
                count = len(re.findall(r"#\[py(function|method)\]", content))
                results.append({"file": rel, "count": count})
    return results


def scan_extern_c():
    """Find extern C blocks."""
    results = []
    for root, dirs, files in os.walk(MONTY_SRC):
        for f in files:
            if not f.endswith(".rs"):
                continue
            path = Path(root) / f
            content = path.read_text(errors="replace")
            if 'extern "C"' in content:
                rel = str(path.relative_to(MONTY_SRC))
                count = content.count('extern "C"')
                results.append({"file": rel, "count": count})
    return results


def scan_callback_points():
    """Find functions accepting &mut VM (potential callback entry points)."""
    results = defaultdict(list)
    for root, dirs, files in os.walk(MONTY_SRC):
        for f in files:
            if not f.endswith(".rs"):
                continue
            path = Path(root) / f
            content = path.read_text(errors="replace")
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if "&mut VM" in line and "fn " in line and "//" not in line[:line.index("fn") if "fn" in line else 0]:
                    rel = str(path.relative_to(MONTY_SRC))
                    results[rel].append({"line": i, "signature": line.strip()[:120]})
    return dict(results)


def scan_module_imports():
    """Find the module whitelist (StandardLib enum)."""
    path = Path(MONTY_SRC) / "modules" / "mod.rs"
    if not path.exists():
        return {}
    content = path.read_text(errors="replace")
    modules = re.findall(r'(\w+),', content)
    return {"file": "modules/mod.rs", "whitelisted_modules": modules[:20]}


def main():
    print(f"Scanning {MONTY_SRC}...")

    report = {
        "unsafe_blocks": scan_unsafe_blocks(),
        "pyfunctions": scan_pyfunctions(),
        "extern_c": scan_extern_c(),
        "callback_points": scan_callback_points(),
        "module_whitelist": scan_module_imports(),
    }

    # Summary
    total_unsafe = sum(r["count"] for r in report["unsafe_blocks"])
    total_pyfn = sum(r["count"] for r in report["pyfunctions"])
    total_extern = sum(r["count"] for r in report["extern_c"])
    total_callback_files = len(report["callback_points"])

    report["summary"] = {
        "total_unsafe_blocks": total_unsafe,
        "total_pyfunctions": total_pyfn,
        "total_extern_c": total_extern,
        "callback_entry_files": total_callback_files,
        "unsafe_files": len(report["unsafe_blocks"]),
    }

    out_path = Path(__file__).parent / "notes" / "source_scan.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, default=str))

    print(f"  unsafe blocks:    {total_unsafe} across {len(report['unsafe_blocks'])} files")
    print(f"  pyfunctions:      {total_pyfn}")
    print(f"  extern C:         {total_extern}")
    print(f"  callback files:   {total_callback_files}")
    print(f"  Saved to:         {out_path}")

    # Top unsafe files
    print("\n  Top files by unsafe count:")
    for r in sorted(report["unsafe_blocks"], key=lambda x: x["count"], reverse=True)[:5]:
        print(f"    {r['file']:50s} — {r['count']} blocks")


if __name__ == "__main__":
    main()

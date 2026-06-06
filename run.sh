#!/bin/bash
# Hack Monty — Autonomous Sandbox Security Assessment
#
# Requires: ollama daemon running (ollama serve)
# The daemon proxies cloud models automatically — no pull needed.
#
# Usage:
#   ./run.sh              # 500 iterations
#   ./run.sh 20           # 20 iterations (test)
#   ./run.sh -i            # interactive REPL

set -e
ABS_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ABS_DIR"
export USER_SECRET="${USER_SECRET:-cipher-zenith-quantum-drift-hm2026}"

TOKENWORM="${TOKENWORM_BIN:-/home/dipankar/Github/tokenworm/zig-out/bin/tokenworm}"

if [ "${1:-}" = "-i" ] || [ "${1:-}" = "--interactive" ]; then
    exec "$TOKENWORM" \
        --config-dir "$ABS_DIR/tokenworm" \
        --workspace "$ABS_DIR" \
        -p ollama_native \
        -i
fi

ITERATIONS="${1:-500}"
exec "$TOKENWORM" \
    --config-dir "$ABS_DIR/tokenworm" \
    --workspace "$ABS_DIR" \
    -p ollama_native \
    "/orchestrator $ITERATIONS"

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
cd "$(dirname "$0")"
export USER_SECRET="${USER_SECRET:-cipher-zenith-quantum-drift-hm2026}"

TOKENWORM="${TOKENWORM_BIN:-/home/dipankar/Github/tokenworm/zig-out/bin/tokenworm}"

if [ "$1" = "--interactive" ] || [ "$1" = "-i" ]; then
    exec "$TOKENWORM" \
        --config-dir ./tokenworm \
        --workspace . \
        -p ollama \
        -i
fi

ITERATIONS="${1:-500}"
exec "$TOKENWORM" \
    --config-dir ./tokenworm \
    --workspace . \
    -p ollama \
    "/orchestrator $ITERATIONS"

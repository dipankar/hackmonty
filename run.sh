#!/bin/bash
# Hack Monty — Autonomous Sandbox Security Assessment
#
# Production launcher using the tokenworm Zig binary with:
#   - Native Ollama Cloud API provider
#   - MCP stdio boundary tools
#   - Bwrap sandbox (enabled)
#   - Progress hooks for CLI logging
#   - Self-contained config at ./tokenworm/config.json
#
# Usage:
#   ./run.sh              # 500 iterations (default)
#   ./run.sh 20           # 20 iterations (test)
#   ./run.sh --interactive # REPL mode

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

#!/bin/bash
set -e

echo "============================================"
echo "  OpenCode Server — Starting Up"
echo "============================================"

# 3. Launch
export PATH="/opt/venv/bin:$HOME/.opencode/bin:$HOME/.local/bin:$PATH"
PORT="${OPENCODE_PORT:-4096}"
HOST="${OPENCODE_HOST:-0.0.0.0}"

echo "[OK] Serving on $HOST:$PORT"
exec opencode serve --hostname "$HOST" --port "$PORT"

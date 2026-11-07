#!/usr/bin/env bash
# Start script for Gateway on Arduino UNO Q
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

export PYTHONPATH="$DIR:$PYTHONPATH"
echo "Starting Vector Edge Gateway on Arduino UNO Q..."
python3 -m gateway.main

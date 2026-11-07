#!/usr/bin/env bash
# Start script for PC Workstation Agent (Linux/WSL)
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

export PYTHONPATH="$DIR:$PYTHONPATH"
echo "Starting Vector Workstation Agent & Dashboard on PC (port 8080)..."
echo "Open dashboard at: http://localhost:8080/dashboard"
python3 -m pc_agent.server

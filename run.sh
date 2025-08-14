#!/bin/bash
# Activate venv
source "$(dirname "$0")/.venv/bin/activate"

# Pass all arguments to the CLI
python -m app.cli "$@"

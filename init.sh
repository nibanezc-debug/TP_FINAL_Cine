#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
printf 'Entorno preparado. Activar con: source .venv/bin/activate\n'

#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Error: python3 no está instalado." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "Creando entorno virtual en .venv..."
  if ! python3 -m venv .venv; then
    echo "Error al crear .venv. En Debian/Ubuntu instalá: sudo apt install python3-venv" >&2
    exit 1
  fi
fi

source .venv/bin/activate

echo "Instalando dependencias..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
  echo "Se creó .env desde .env.example. Completá tus credenciales antes de ejecutar ./correr.sh."
fi

if ! command -v mysql >/dev/null 2>&1; then
  echo "Aviso: no se encontró el cliente 'mysql' en el PATH (necesario para que ./correr.sh inicialice la BD)." >&2
fi

chmod +x correr.sh 2>/dev/null || true

printf '\nEntorno preparado.\n'
printf '1) Revisá .env (DB, OMDb, SMTP y claves secretas).\n'
printf '2) Ejecutá ./correr.sh para inicializar la base y levantar backend (5000) + frontend (5001).\n'
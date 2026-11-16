#!/usr/bin/env bash
# Levanta la base de datos, el backend (5000) y el frontend (5001).
# Uso:  ./correr.sh      (se puede ejecutar desde cualquier carpeta)
set -euo pipefail
cd "$(dirname "$0")"

echo "========================================="
echo ":popcorn: INICIANDO CINE PARADISO..."
echo "========================================="

# 1. Variables de entorno desde .env (ese archivo NO se sube a Git)
if [ ! -f .env.example ]; then
  echo ":x: Falta el archivo .env.example." >&2
  exit 1
fi
set -a
source .env.example
set +a
: "${FLASK_SECRET_KEY:?Falta FLASK_SECRET_KEY en .env}"
: "${FRONT_SECRET_KEY:?Falta FRONT_SECRET_KEY en .env}"

# 2. Entorno virtual
source .venv/bin/activate

# 3. Base de datos (la contraseña va por variable de entorno, no por la línea de comandos)
export MYSQL_PWD="$DB_PASSWORD"
MYSQL=(mysql -h "$DB_HOST" -P "$DB_PORT" -u "$DB_USER" --protocol=tcp)

echo ":arrow_right: Comprobando base de datos..."
if ! "${MYSQL[@]}" -e "CREATE DATABASE IF NOT EXISTS \`$DB_NAME\`;"; then
  echo ":x: No se pudo conectar a MySQL. Revisá DB_HOST, DB_PORT, DB_USER y DB_PASSWORD en .env" >&2
  echo "   y que el servidor esté corriendo (por ejemplo, el contenedor de Docker)." >&2
  exit 1
fi
TABLAS=$("${MYSQL[@]}" -N -B -e "SHOW TABLES FROM \`$DB_NAME\`;")

if [ -z "$TABLAS" ]; then
  SQL_DIR=""
  for d in cine_src/db schema_sql db; do
    if [ -f "$d/schema_tablas_cine.sql" ]; then SQL_DIR="$d"; break; fi
  done
  if [ -z "$SQL_DIR" ]; then
    echo ":x: No encontré schema_tablas_cine.sql (busqué en cine_src/db/, schema_sql/ y db/)." >&2
    exit 1
  fi
  echo ":arrow_right: Base de datos vacía. Cargando esquema desde $SQL_DIR/ ..."
  "${MYSQL[@]}" "$DB_NAME" < "$SQL_DIR/schema_tablas_cine.sql"
  if [ -f "$SQL_DIR/seed.sql" ]; then
    echo ":arrow_right: Cargando datos de ejemplo..."
    "${MYSQL[@]}" "$DB_NAME" < "$SQL_DIR/seed.sql"
  fi
  echo ":white_check_mark: Base de datos cargada con éxito."
else
  echo ":white_check_mark: La base de datos ya tiene tablas. Saltando inicialización."
fi
unset MYSQL_PWD

# 4. Backend
echo ":arrow_right: Levantando Backend (Puerto 5000)..."
cd cine_src
python3 app.py &
BACKEND_PID=$!
cd ..

# 5. Frontend (usa su propia clave secreta, distinta de la del backend)
echo ":arrow_right: Levantando Frontend (Puerto 5001)..."
cd API_FRONTEND
FLASK_SECRET_KEY="$FRONT_SECRET_KEY" API_URL="http://127.0.0.1:5000/api" python3 app.py &
FRONTEND_PID=$!
cd ..

echo "========================================="
echo ":white_check_mark: ¡SISTEMA ONLINE! :point_right: http://127.0.0.1:5001"
echo ":octagonal_sign: Presioná Ctrl+C para apagar todo."
echo "========================================="

trap 'echo; echo "Apagando servidores..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true; exit' INT TERM
wait
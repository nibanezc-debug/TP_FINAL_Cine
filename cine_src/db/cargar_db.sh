#!/bin/bash
# Recrea la base desde cero. BORRA los datos existentes solo para desarrollo.
set -e
if [ -z "$DB_PASSWORD" ]; then
  echo "Falta exportar DB_PASSWORD" >&2
  exit 1
fi
export MYSQL_PWD="$DB_PASSWORD"
MYSQL="mysql -h ${DB_HOST:-127.0.0.1} -P ${DB_PORT:-3306} -u ${DB_USER:-root}"
cd "$(dirname "$0")" || exit 1
$MYSQL -e "DROP DATABASE IF EXISTS cine_paradiso;"
$MYSQL < schema_tablas_cine.sql
$MYSQL < seed.sql
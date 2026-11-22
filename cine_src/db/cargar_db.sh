#!/bin/bash
# Recrea la base desde cero dentro del contenedor Docker. BORRA los datos existentes.
set -e

DB_PASSWORD="${DB_PASSWORD:-lanzillotta}"
DB_USER="${DB_USER:-root}"
CONTAINER_NAME="${CONTAINER_NAME:-docker-db-1}"

cd "$(dirname "$0")" || exit 1

MYSQL="docker exec -i -e MYSQL_PWD=$DB_PASSWORD $CONTAINER_NAME mysql -u $DB_USER --default-character-set=utf8mb4"

$MYSQL -e "DROP DATABASE IF EXISTS cine_paradiso;"
$MYSQL < schema_tablas_cine.sql
$MYSQL cine_paradiso < seed.sql

echo "Base de datos cine_paradiso recreada correctamente."
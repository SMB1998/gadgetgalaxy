#!/bin/bash
set -e

echo "Esperando 10 segundos..."

sleep 10

echo "Terminó el tiempo de espera de 10 segundos."

exec "$@"


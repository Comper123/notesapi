#!/bin/sh
set -eu

base_url="http://localhost:${PORT:-8201}"

curl -fsS "$base_url/health"
curl -fsS -X POST "$base_url/notes" \
  -H "Content-Type: application/json" \
  -d '{"text":"Дымовая проверка"}'
curl -fsS "$base_url/notes"

bad_code=$(curl -sS -o /dev/null -w '%{http_code}' -X POST "$base_url/notes" \
  -H "Content-Type: application/json" -d '{"text":""}')
[ "$bad_code" = "400" ]

missing_code=$(curl -sS -o /dev/null -w '%{http_code}' "$base_url/missing")
[ "$missing_code" = "404" ]

echo "Smoke tests passed"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)
ROOT_DIR=$(cd -- "$SCRIPT_DIR/.." && pwd)

export $(grep -v '^#' "$ROOT_DIR/.env" 2>/dev/null | xargs -r) || true

printf "[1/4] Starting Supabase (db+postgrest+realtime)\n"
docker compose -f "$ROOT_DIR/infra/supabase/docker-compose.yml" up -d

printf "[2/4] Applying schema & seed\n"
# Wait for DB using service name
until docker compose -f "$ROOT_DIR/infra/supabase/docker-compose.yml" exec -T db pg_isready -U postgres -h localhost; do
  sleep 1
  printf "."
done
# Apply schema and seed using service name 'db'
docker compose -f "$ROOT_DIR/infra/supabase/docker-compose.yml" exec -T db psql -U postgres -d postgres < "$ROOT_DIR/infra/supabase/schema.sql"
docker compose -f "$ROOT_DIR/infra/supabase/docker-compose.yml" exec -T db psql -U postgres -d postgres < "$ROOT_DIR/infra/supabase/seed.sql"

printf "\n[3/4] Starting control-api and runner (dev mode)\n"
# Python venvs are optional; run directly if available
python -m pip install -r "$ROOT_DIR/apps/control-api/requirements.txt" || true
python -m pip install -r "$ROOT_DIR/apps/runner/requirements.txt" || true

# Start API
python "$ROOT_DIR/apps/control-api/main.py" &
API_PID=$!
# Start Runner
python "$ROOT_DIR/apps/runner/main.py" &
RUNNER_PID=$!

printf "[4/4] Building dashboard (first run may take time)\n"
if command -v npm >/dev/null 2>&1; then
  (cd "$ROOT_DIR/apps/dashboard" && npm install && npm run start) &
else
  echo "npm not found. Please build dashboard manually."
fi

printf "\nDemo running. API: http://localhost:8001, Dashboard: http://localhost:4200\n"
wait $API_PID $RUNNER_PID


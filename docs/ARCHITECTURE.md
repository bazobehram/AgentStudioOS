# Architecture

- Supabase (Postgres + PostgREST + Realtime)
- Control API (FastAPI) exposes REST/WS and talks to DB
- Runner polls tasks from DB and executes using adapters and plugins
- Dashboard connects to API/WS and Supabase endpoints


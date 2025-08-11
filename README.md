# AgentStudioOS

AgentStudioOS is a monorepo for "Agent Studio" — a self-hosted multi-agent studio built on Supabase (Postgres+Auth+Realtime), FastAPI, Python Runner, Angular Dashboard, and Ollama. It is extendable via a Plugin SDK and ships with initial agent templates and example plugins.

Highlights:
- Monorepo with apps (dashboard, control-api, runner), packages (Python/TS SDKs, plugins), infra (Supabase, reverse proxy, CI), and docs.
- Reproducible local demo via one command: ./infra/local_demo.sh
- Conventional commits, changelog, logs in both filesystem and DB, approval-gated public actions, retries with backoff, and tests (unit/integration/e2e).

Quick start
- Prereqs: Docker Desktop, Node 20+, Python 3.11, Git, (optional) Ollama, Playwright deps.
- Copy .env.example to .env and adjust if needed.
- Run the local demo: ./infra/local_demo.sh
- Open dashboard at http://localhost:4200 (first run builds dashboard dev server) and API at http://localhost:8001

Repo layout
- apps/
  - dashboard/ (Angular PWA shell)
  - control-api/ (FastAPI REST + WebSocket)
  - runner/ (Python agent/job executor)
- packages/
  - sdk-py/ (Python SDK: agent/flow API, plugin base)
  - sdk-ts/ (TypeScript client SDK for web)
  - plugins/ (example plugins: X, Bluesky, GitHub, ffmpeg, arXiv)
- infra/
  - supabase/ (docker-compose, schema.sql, seed.sql)
  - reverse-proxy/ (Caddyfile for HTTPS)
  - ci/ (GitHub Actions)
- docs/ (INSTALL, RUNBOOK, ARCHITECTURE, PLUGINS, API_REFERENCE)

License
- Apache-2.0. See LICENSE.


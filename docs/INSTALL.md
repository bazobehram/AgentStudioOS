# Install

Prereqs: Docker Desktop, Node 20+, Python 3.11.

Supabase Realtime
- Ensure SUPABASE_URL and SUPABASE_ANON_KEY are configured (self-host: PostgREST anon).
- Runtime env injection for Angular (assets/env.js or script tag in index.html):
  <script>
    window.__env = {
      SUPABASE_URL: "http://localhost:8000",
      SUPABASE_ANON_KEY: "local-dev-anon",
      API_BASE: "http://localhost:8001"
    };
  </script>

1) Copy .env.example to .env and edit if needed.
2) Launch local demo: ./infra/local_demo.sh (or .\infra\local_demo.ps1 on Windows)
3) Open http://localhost:4200 (Angular dashboard) and http://localhost:8001/healthz (API).


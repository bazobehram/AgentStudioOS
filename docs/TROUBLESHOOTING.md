# Troubleshooting

- Supabase Realtime permissions
  - Ensure the anon key can subscribe to postgres_changes on public tables (agents, tasks, approvals). For local dev, permissive RLS is acceptable; for production, tighten policies.
- CSP and env.js
  - If CSP blocks inline scripts, use the static assets/env.js file (already referenced in Angular index.html). Bust caches by appending a query string, e.g., assets/env.js?v=1.
- Playwright on CI
  - Install Chromium with dependencies. The CI workflow uses playwright install --with-deps chromium. Headless mode is enabled.
- PowerShell ExecutionPolicy
  - If local_demo.ps1 is blocked, run: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
- Realtime vs polling
  - If realtime isn’t working, lists will still refresh via manual reload. Verify SUPABASE_URL/ANON key and network access.
- Secrets not visible
  - Logs are designed to avoid printing secrets. If you suspect leakage, search logs/ for known tokens. Unit tests include negative cases (wrong key decryption returns None).

# API Reference

- GET /healthz: API and DB heartbeat

Agents
- GET /agents
- POST /agents { name, type, mode?, model?, profile? }
- PATCH /agents/{id}

Tasks
- GET /tasks
- POST /tasks { agent_id, type, payload }

Approvals
- GET /approvals
- POST /approvals { kind, content, status?, reviewer_note? }
- PATCH /approvals/{id} { status, reviewer_note? }

Workflows & Routines
- POST /workflows/run { name }
- POST /routines { name, cron, template_task, enabled? }

WS
- /ws: realtime placeholder


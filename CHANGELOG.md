# Changelog

All notable changes to this project will be documented in this file.

The format is based on Conventional Commits.

## [0.1.0-MVP] - 2025-08-11
### Added
- Control API endpoints: /healthz, /agents (GET/POST/PATCH), /tasks (GET/POST), /approvals (GET/POST/PATCH), /workflows/run, /routines, /secrets (AES-GCM encrypted).
- Runner adapters: OllamaAdapter (generate/embed with mock fallback), BrowserAdapter (Playwright screenshot with mock), VectorMemory (mock storage).
- Approval gating in runner for public actions (post_x) with wait loop.
- Env updates: CHROMA_PATH, SECRETS_MASTER_KEY, and Docker compose exec by service name in local_demo.
- Schema: agents.last_heartbeat column.

### Changed
- Runner processes draft_post, post_x, post_bsky, browser_screenshot, store_note, run_workflow; logs steps and outputs.
- API docs updated; requirements extended.


-- Schema for AgentStudioOS
create table if not exists agents (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  type text not null,
  status text not null default 'stopped',
  mode text not null default 'approved',
  model text,
  profile jsonb default '{}',
  memory_ref text,
  last_heartbeat timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid references agents(id) on delete cascade,
  type text not null,
  payload jsonb not null,
  status text not null default 'queued',
  scheduled_at timestamptz,
  started_at timestamptz,
  finished_at timestamptz,
  error text
);

create table if not exists approvals (
  id uuid primary key default gen_random_uuid(),
  kind text not null,
  content jsonb not null,
  status text not null default 'pending',
  reviewer_note text,
  created_at timestamptz not null default now()
);

create table if not exists workflows (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  graph jsonb not null,
  auto boolean not null default false,
  owner_id text,
  created_at timestamptz not null default now()
);

create table if not exists routines (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  cron text not null,
  template_task jsonb not null,
  enabled boolean not null default true
);

create table if not exists notes (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid references agents(id) on delete cascade,
  topic text,
  content_md text,
  sources jsonb,
  created_at timestamptz not null default now()
);

create table if not exists metrics (
  id uuid primary key default gen_random_uuid(),
  agent_id uuid references agents(id) on delete cascade,
  target text,
  kpi text,
  value double precision,
  ts timestamptz not null default now()
);

create table if not exists secrets (
  id uuid primary key default gen_random_uuid(),
  owner_id text,
  key text not null,
  value_enc bytea not null,
  scope text
);

-- Indexes
create index if not exists idx_tasks_status on tasks(status);
create index if not exists idx_tasks_agent on tasks(agent_id);
create index if not exists idx_approvals_status on approvals(status);
create index if not exists idx_notes_agent on notes(agent_id);
create index if not exists idx_metrics_agent on metrics(agent_id);

-- RLS (basic placeholders)
alter table agents enable row level security;
alter table tasks enable row level security;
alter table approvals enable row level security;
alter table workflows enable row level security;
alter table routines enable row level security;
alter table notes enable row level security;
alter table metrics enable row level security;
alter table secrets enable row level security;

-- Simple permissive policies for local single-user dev
create policy if not exists p_select_all_agents on agents for select using (true);
create policy if not exists p_insert_all_agents on agents for insert with check (true);
create policy if not exists p_update_all_agents on agents for update using (true);
create policy if not exists p_select_all_tasks on tasks for select using (true);
create policy if not exists p_modify_all_tasks on tasks for all using (true) with check (true);
create policy if not exists p_all_approvals on approvals for all using (true) with check (true);
create policy if not exists p_all_workflows on workflows for all using (true) with check (true);
create policy if not exists p_all_routines on routines for all using (true) with check (true);
create policy if not exists p_all_notes on notes for all using (true) with check (true);
create policy if not exists p_all_metrics on metrics for all using (true) with check (true);
create policy if not exists p_all_secrets on secrets for all using (true) with check (true);


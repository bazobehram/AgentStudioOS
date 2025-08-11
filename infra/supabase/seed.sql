insert into agents (name, type, status, mode, model, profile, memory_ref)
values
 ('Social Scout', 'social', 'stopped', 'approved', 'llama3.1:8b', '{"roles":["scout","scriptwriter"]}'::jsonb, 'social_scout'),
 ('Theory Builder', 'research', 'stopped', 'approved', 'llama3.1:8b', '{"roles":["theory"]}'::jsonb, 'theory_builder');

insert into workflows (name, graph, auto, owner_id)
values
 ('Social Daily', '{"nodes":[],"edges":[]}'::jsonb, false, 'local'),
 ('Theory Weekly', '{"nodes":[],"edges":[]}'::jsonb, false, 'local');

insert into routines (name, cron, template_task, enabled)
values
 ('Social Daily Drafts', '0 9 * * *', '{"type":"social_drafts","agent":"Social Scout"}'::jsonb, true),
 ('Daily Note', '0 20 * * *', '{"type":"daily_note","agent":"Theory Builder"}'::jsonb, true);

insert into approvals (kind, content, status)
values
 ('post', '{"service":"x","text":"Hello world"}'::jsonb, 'pending');


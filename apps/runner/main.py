import os
import asyncio
import asyncpg
import datetime as dt
import json
from pathlib import Path
from typing import Any, Dict
from adapters.ollama_adapter import OllamaAdapter
from adapters.browser_adapter import BrowserAdapter
from adapters.vector_memory import VectorMemory

DB_DSN = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:54322/postgres")
LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)

RETRY_LIMIT = 2

async def log_task(task_id: str, message: str):
    day_dir = LOG_DIR / dt.date.today().isoformat()
    day_dir.mkdir(parents=True, exist_ok=True)
    with (day_dir / f"{task_id}.md").open("a", encoding="utf-8") as f:
        f.write(f"- [{dt.datetime.now().isoformat()}] {message}\n")

async def ensure_approval(conn, task_id: str, kind: str, content: Dict[str, Any], mode: str) -> None:
    if mode == 'auto':
        return
    # create approval entry and wait until approved
    row = await conn.fetchrow(
        "insert into approvals(kind, content, status) values($1,$2,'pending') returning *",
        kind, json.dumps(content)
    )
    approval_id = str(row['id'])
    await log_task(task_id, f"Approval created: {approval_id} waiting for approval")
    while True:
        row = await conn.fetchrow("select status from approvals where id=$1", approval_id)
        status = row['status'] if row else 'rejected'
        if status == 'approved':
            await log_task(task_id, f"Approval approved: {approval_id}")
            return
        if status == 'rejected':
            raise RuntimeError("Approval rejected")
        await asyncio.sleep(1)

async def process_task(conn, task):
    task_id = str(task["id"])
    agent = await conn.fetchrow("select * from agents where id=$1", task['agent_id'])
    mode = (agent['mode'] or 'approved') if agent else 'approved'
    ttype = task['type']
    payload = task['payload']
    await log_task(task_id, f"Processing type={ttype}")

    ollama = OllamaAdapter()
    browser = BrowserAdapter()
    memory = VectorMemory(namespace=(agent['memory_ref'] or str(agent['id'])) if agent else 'default')

    if ttype == 'draft_post':
        prompt = payload.get('prompt','Write a short post about AgentStudio.')
        model = (agent['model'] or os.getenv('MODEL_GENERAL','llama3.1:8b')) if agent else os.getenv('MODEL_GENERAL','llama3.1:8b')
        text = await ollama.generate(prompt, model)
        await log_task(task_id, f"Draft: {text[:120]}...")
        return {"draft": text}
    elif ttype == 'post_x':
        content = payload
        await ensure_approval(conn, task_id, 'post', content, mode)
        # mock posting by writing file
        out = Path('outputs'); out.mkdir(exist_ok=True)
        fp = out / f"x_{task_id}.txt"
        fp.write_text(content.get('text',''), encoding='utf-8')
        await log_task(task_id, f"Posted to X (mock): {fp}")
        return {"posted": str(fp)}
    elif ttype == 'post_bsky':
        out = Path('outputs'); out.mkdir(exist_ok=True)
        fp = out / f"bsky_{task_id}.txt"
        fp.write_text(payload.get('text',''), encoding='utf-8')
        await log_task(task_id, f"Posted to Bluesky (mock): {fp}")
        return {"posted": str(fp)}
    elif ttype == 'browser_screenshot':
        url = payload.get('url','https://example.com')
        out = Path('outputs'); out.mkdir(exist_ok=True)
        img = out / f"shot_{task_id}.png"
        await browser.screenshot(url, img)
        await log_task(task_id, f"Screenshot saved: {img}")
        return {"screenshot": str(img)}
    elif ttype == 'store_note':
        topic = payload.get('topic','note')
        content = payload.get('content_md','')
        await conn.execute("insert into notes(agent_id, topic, content_md, sources) values($1,$2,$3,$4)", task['agent_id'], topic, content, json.dumps(payload.get('sources') or []))
        await memory.store(content)
        await log_task(task_id, "Note stored and embedded")
        return {"stored": True}
    elif ttype == 'run_workflow':
        name = payload.get('name','unknown')
        await log_task(task_id, f"Workflow run requested: {name} (no-op)")
        return {"workflow": name}
    else:
        await log_task(task_id, f"Unknown task type: {ttype}")
        return {}

async def handle_task(conn, task):
    task_id = str(task["id"])
    await conn.execute("update tasks set status='running', started_at=now() where id=$1", task_id)
    await log_task(task_id, "Task started")
    tries = 0
    while True:
        try:
            result = await process_task(conn, task)
            await conn.execute("update tasks set status='done', finished_at=now(), error=null where id=$1", task_id)
            await log_task(task_id, f"Task completed: {result}")
            break
        except Exception as e:
            tries += 1
            await log_task(task_id, f"Error: {e}. Try {tries}/{RETRY_LIMIT}")
            if tries > RETRY_LIMIT:
                await conn.execute("update tasks set status='failed', finished_at=now(), error=$2 where id=$1", task_id, str(e))
                break
            await asyncio.sleep(2 ** tries)

async def heartbeat(conn):
    # update agents.last_heartbeat (add column if missing is out-of-scope; we log instead)
    await asyncio.sleep(0)

async def main():
    pool = await asyncpg.create_pool(dsn=DB_DSN)
    async with pool.acquire() as conn:
        while True:
            task = await conn.fetchrow("select * from tasks where status='queued' order by scheduled_at nulls first, started_at nulls first nulls first limit 1 for update skip locked")
            if task:
                await handle_task(conn, task)
            else:
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())


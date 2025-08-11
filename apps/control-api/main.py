import os
import uvicorn
from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
import json
from typing import Optional
from datetime import datetime
from base64 import urlsafe_b64decode, urlsafe_b64encode
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import secrets as pysecrets

PORT = int(os.getenv("CONTROL_API_PORT", "8001"))
DB_DSN = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:54322/postgres")
MASTER_KEY_B64 = os.getenv("SECRETS_MASTER_KEY", "")

app = FastAPI(title="AgentStudio Control API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentIn(BaseModel):
    name: str
    type: str
    mode: Optional[str] = "approved"
    model: Optional[str] = None
    profile: Optional[dict] = None

class TaskIn(BaseModel):
    agent_id: str
    type: str
    payload: dict

class ApprovalIn(BaseModel):
    kind: str
    content: dict
    status: Optional[str] = "pending"
    reviewer_note: Optional[str] = None

class ApprovalPatch(BaseModel):
    status: str
    reviewer_note: Optional[str] = None

class SecretIn(BaseModel):
    owner_id: Optional[str] = None
    key: str
    value: str
    scope: Optional[str] = None

@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(dsn=DB_DSN)

@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()

@app.get("/healthz")
async def healthz():
    # Basic DB check
    try:
        async with app.state.pool.acquire() as conn:
            await conn.fetchval("select 1")
        return {"ok": True, "ts": datetime.utcnow().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Agents
@app.get("/agents")
async def list_agents():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch("select * from agents order by created_at desc")
        return [dict(r) for r in rows]

@app.post("/agents")
async def create_agent(agent: AgentIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "insert into agents(name, type, mode, model, profile, status) values($1,$2,$3,$4,$5,'stopped') returning *",
            agent.name, agent.type, agent.mode, agent.model, json.dumps(agent.profile or {})
        )
        return dict(row)

@app.patch("/agents/{agent_id}")
async def update_agent(agent_id: str, agent: AgentIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "update agents set name=$2, type=$3, mode=$4, model=$5, profile=$6 where id=$1 returning *",
            agent_id, agent.name, agent.type, agent.mode, agent.model, json.dumps(agent.profile or {})
        )
        if not row:
            raise HTTPException(status_code=404, detail="Agent not found")
        return dict(row)

# Tasks
@app.get("/tasks")
async def list_tasks():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch("select * from tasks order by scheduled_at nulls first, started_at nulls first")
        return [dict(r) for r in rows]

@app.post("/tasks")
async def create_task(task: TaskIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "insert into tasks(agent_id, type, payload) values($1,$2,$3) returning *",
            task.agent_id, task.type, json.dumps(task.payload)
        )
        return dict(row)

# Approvals
@app.get("/approvals")
async def list_approvals():
    async with app.state.pool.acquire() as conn:
        rows = await conn.fetch("select * from approvals order by created_at desc")
        return [dict(r) for r in rows]

@app.post("/approvals")
async def create_approval(ap: ApprovalIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "insert into approvals(kind, content, status, reviewer_note) values($1,$2,$3,$4) returning *",
            ap.kind, json.dumps(ap.content), ap.status, ap.reviewer_note
        )
        return dict(row)

@app.patch("/approvals/{approval_id}")
async def patch_approval(approval_id: str, body: ApprovalPatch):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "update approvals set status=$2, reviewer_note=$3 where id=$1 returning *",
            approval_id, body.status, body.reviewer_note
        )
        if not row:
            raise HTTPException(status_code=404, detail="Approval not found")
        return dict(row)

# Workflows & routines (stubs)
class WorkflowRunIn(BaseModel):
    name: str

@app.post("/workflows/run")
async def run_workflow(body: WorkflowRunIn):
    # For MVP: enqueue a task representing the workflow name
    async with app.state.pool.acquire() as conn:
        agent_id = await conn.fetchval("select id from agents order by created_at asc limit 1")
        if not agent_id:
            raise HTTPException(status_code=400, detail="No agents available")
        row = await conn.fetchrow(
            "insert into tasks(agent_id, type, payload) values($1,$2,$3) returning *",
            agent_id, "run_workflow", json.dumps({"name": body.name})
        )
        return dict(row)

class RoutineIn(BaseModel):
    name: str
    cron: str
    template_task: dict
    enabled: bool = True

@app.post("/routines")
async def create_routine(body: RoutineIn):
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "insert into routines(name, cron, template_task, enabled) values($1,$2,$3,$4) returning *",
            body.name, body.cron, json.dumps(body.template_task), body.enabled
        )
        return dict(row)

# Secrets (AES-GCM)

def _get_aesgcm():
    if not MASTER_KEY_B64:
        raise HTTPException(status_code=500, detail="SECRETS_MASTER_KEY not configured")
    key = urlsafe_b64decode(MASTER_KEY_B64 + "==")
    if len(key) != 32:
        raise HTTPException(status_code=500, detail="SECRETS_MASTER_KEY must be 32 bytes")
    return AESGCM(key)

@app.post("/secrets")
async def store_secret(sec: SecretIn):
    aes = _get_aesgcm()
    nonce = os.urandom(12)
    ct = aes.encrypt(nonce, sec.value.encode("utf-8"), None)
    value_enc = nonce + ct
    async with app.state.pool.acquire() as conn:
        row = await conn.fetchrow(
            "insert into secrets(owner_id, key, value_enc, scope) values($1,$2,$3,$4) returning id, owner_id, key, scope",
            sec.owner_id, sec.key, value_enc, sec.scope
        )
        return dict(row)

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"type":"welcome","msg":"AgentStudio Control WS"})
    await ws.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)


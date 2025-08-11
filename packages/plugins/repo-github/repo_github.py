from agent_sdk import AgentTool, ToolContext

class CreateRepo(AgentTool):
  name = "create_repo"
  async def run(self, payload, ctx: ToolContext):
    return {"status":"mocked","repo": payload.get("name","demo"), "agent": ctx.agent_id}


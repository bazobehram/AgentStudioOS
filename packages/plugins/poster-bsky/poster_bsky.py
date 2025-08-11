from agent_sdk import AgentTool, ToolContext

class PostToBsky(AgentTool):
  name = "post_to_bsky"
  async def run(self, payload, ctx: ToolContext):
    return {"status":"mocked","text": payload.get("text",""), "agent": ctx.agent_id}


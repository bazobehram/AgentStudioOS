from agent_sdk import AgentTool, ToolContext

class PostToX(AgentTool):
  name = "post_to_x"
  async def run(self, payload, ctx: ToolContext):
    # mock: return the message without posting
    return {"status":"mocked","text": payload.get("text",""), "agent": ctx.agent_id}


from agent_sdk import AgentTool, ToolContext

class RenderVideo(AgentTool):
  name = "render_video"
  async def run(self, payload, ctx: ToolContext):
    preset = payload.get("preset","1080x1920@30")
    return {"status":"mocked","output":"output/video.mp4","preset":preset}


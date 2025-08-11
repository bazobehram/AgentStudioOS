from agent_sdk import AgentTool, ToolContext

class SearchArxiv(AgentTool):
  name = "search_arxiv"
  async def run(self, payload, ctx: ToolContext):
    query = payload.get("q","machine learning")
    return {"status":"mocked","results":[{"title":"Sample Paper","q":query}]}


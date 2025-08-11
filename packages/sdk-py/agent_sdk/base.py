from typing import Any, Dict, Callable
from pydantic import BaseModel

class ToolContext(BaseModel):
  agent_id: str
  task_id: str
  metadata: Dict[str, Any] = {}

class AgentTool:
  name: str = "tool"
  schema: BaseModel | None = None

  async def run(self, payload: Dict[str, Any], ctx: ToolContext) -> Any:
    raise NotImplementedError

class AgentPlugin:
  def register(self, tools_registry: Dict[str, AgentTool]) -> None:
    raise NotImplementedError


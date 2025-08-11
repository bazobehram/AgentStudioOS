export type Agent = { id: string; name: string; type: string; status: string };
export async function listAgents(base = 'http://localhost:8001'): Promise<Agent[]> {
  const r = await fetch(`${base}/agents`);
  return r.json();
}


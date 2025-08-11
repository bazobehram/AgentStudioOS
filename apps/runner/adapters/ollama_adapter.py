import os
import httpx

class OllamaAdapter:
    def __init__(self):
        self.base = os.getenv('OLLAMA_HOST', 'http://127.0.0.1:11434')

    async def generate(self, prompt: str, model: str):
        url = f"{self.base}/api/generate"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(url, json={"model": model, "prompt": prompt, "stream": False})
                r.raise_for_status()
                data = r.json()
                return data.get('response') or data.get('content') or ""
        except Exception:
            # Fallback mock
            return f"[mock:{model}] {prompt[:120]}..."

    async def embed(self, text: str, model: str | None = None):
        url = f"{self.base}/api/embeddings"
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(url, json={"model": model or "nomic-embed-text", "input": text})
                r.raise_for_status()
                data = r.json()
                return data.get('embedding') or []
        except Exception:
            return [0.0] * 10

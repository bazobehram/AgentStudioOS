import os
from pathlib import Path
import json

class VectorMemory:
    def __init__(self, namespace: str):
        self.base = Path(os.getenv('CHROMA_PATH', '.chroma')) / namespace
        self.base.mkdir(parents=True, exist_ok=True)

    async def store(self, content_md: str):
        # Mock: append to a jsonl file to simulate storage
        fp = self.base / 'memory.jsonl'
        with fp.open('a', encoding='utf-8') as f:
            f.write(json.dumps({"content_md": content_md}) + "\n")

import os
from typing import Dict, Any

class KnowledgeBase:
    def __init__(self, kb_path="data/knowledge/"):
        self.kb_path = kb_path
        os.makedirs(kb_path, exist_ok=True)

    async def add_document(self, file):
        file_path = os.path.join(self.kb_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        return {"status": "ok", "path": file_path}

    def query(self, question: str) -> str:
        # 简化示例：基于文件名的关键词匹配
        docs = os.listdir(self.kb_path)
        matched = [doc for doc in docs if question in doc]
        if matched:
            return f"匹配到相关文档: {', '.join(matched)}"
        return "未找到相关知识"
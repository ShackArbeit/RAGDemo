# 檔案說明: 以簡易關聯圖資料，根據問題中的實體回傳鄰接資訊。
from app.db.seed import GRAPH

class GraphRetriever:
    def expand(self, question: str, tenant: str):
        # tenant unused in demo graph, but keep the interface
        q = question.lower()
        hits = []
        for entity, neighbors in GRAPH.items():
            if entity.lower() in q:
                hits.append({
                    "kind": "graph",
                    "id": f"graph-{entity}",
                    "title": f"Graph: {entity} relations",
                    "text": f"{entity} -> " + ", ".join(neighbors),
                    "score": 0.8,
                    "source": {"type": "graph", "uri": f"graph://entity/{entity}"},
                })
        return hits

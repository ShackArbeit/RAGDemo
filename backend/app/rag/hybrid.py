# 檔案說明: 協調向量、SQL、圖三種檢索策略並排序回傳。
from .vector_store import VectorStore
from .sql_retriever import SQLRetriever
from .graph_retriever import GraphRetriever

class HybridRetriever:
    def __init__(self):
        self.vs = VectorStore()
        self.sql = SQLRetriever()
        self.graph = GraphRetriever()

    def retrieve(self, question: str, tenant: str, k: int = 6):
        v = self.vs.search(question, tenant, k=3)
        s = self.sql.query(question, tenant)
        g = self.graph.expand(question, tenant)

        all_items = v + s + g
        all_items.sort(key=lambda x: x["score"], reverse=True)
        return all_items[:k]

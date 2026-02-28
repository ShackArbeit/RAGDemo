# 檔案說明: 使用簡化 TF-IDF 建立向量並以餘弦相似度做檢索。
import math
from collections import Counter
from app.db.seed import DOCS

def _tokenize(s: str) -> list[str]:
    return [w.lower() for w in s.replace("/", " ").replace(">", " ").split() if w.strip()]

def _tfidf(docs: list[str]):
    # extremely small demo TF-IDF
    tokenized = [_tokenize(d) for d in docs]
    df = Counter()
    for toks in tokenized:
        df.update(set(toks))
    N = len(docs)
    vectors = []
    for toks in tokenized:
        tf = Counter(toks)
        vec = {}
        for t, c in tf.items():
            idf = math.log((N + 1) / (df[t] + 1)) + 1
            vec[t] = (c / max(1, len(toks))) * idf
        vectors.append(vec)
    return vectors

def _cosine(a: dict, b: dict) -> float:
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in set(a) | set(b))
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

class VectorStore:
    def __init__(self):
        self._docs = DOCS
        self._texts = [d["title"] + "\n" + d["text"] for d in self._docs]
        self._doc_vecs = _tfidf(self._texts)

    def search(self, query: str, tenant: str, k: int = 3):
        q_vec = _tfidf([query])[0]
        scored = []
        for d, v in zip(self._docs, self._doc_vecs):
            if d["tenant"] != tenant:
                continue
            scored.append((d, _cosine(q_vec, v)))
        scored.sort(key=lambda x: x[1], reverse=True)
        results = []
        for d, score in scored[:k]:
            results.append({
                "kind": "vector",
                "id": d["id"],
                "title": d["title"],
                "text": d["text"],
                "score": float(score),
                "source": d["source"],
            })
        return results

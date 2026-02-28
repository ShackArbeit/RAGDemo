# 檔案說明: 將檢索結果整理成前端可顯示的引用列表。
def format_citations(items: list[dict]):
    cites = []
    for i, it in enumerate(items, start=1):
        cites.append({
            "n": i,
            "kind": it["kind"],
            "title": it["title"],
            "source": it["source"],
        })
    return cites

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
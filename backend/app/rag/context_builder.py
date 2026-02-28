# 檔案說明: 去重並裁剪檢索結果，組合成供 LLM 使用的上下文字串。
def build_context(items: list[dict], max_chars: int = 900):
    seen = set()
    ctx_parts = []
    kept = []
    total = 0
    for it in items:
        key = (it["kind"], it["id"])
        if key in seen:
            continue
        seen.add(key)

        chunk = f"[{it['kind'].upper()}] {it['title']}\n{it['text']}\n"
        if total + len(chunk) > max_chars:
            break
        ctx_parts.append(chunk)
        kept.append(it)
        total += len(chunk)

    context = "\n---\n".join(ctx_parts)
    return context, kept

# 檔案說明: Chat API (SSE)；串接 RBAC/租戶、混合檢索、LLM 回答與稽核寫入。
import json
import time
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.core.auth import User
from app.core.tenant import get_tenant
from app.core.rbac import require_role
from app.core.security import detect_prompt_injection
from app.rag.hybrid import HybridRetriever
from app.rag.context_builder import build_context
from app.rag.llm_gateway import LLMGateway
from app.rag.citations import format_citations
from app.db.init_db import SessionLocal
from app.db.models import AuditLog

router = APIRouter(prefix="/chat", tags=["chat"])

retriever = HybridRetriever()
llm = LLMGateway()

# SSE headers (important for EventSource / fetch streaming)
SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # prevents proxy buffering (nginx etc.). harmless locally.
    "X-Accel-Buffering": "no",
}

@router.get("/dev-token")
def dev_token():
    # For quick local testing (remove in real)
    from app.core.auth import issue_dev_token
    return {"token": issue_dev_token()}

@router.get("/stream")
def chat_stream(
    q: str,
    tenant: str = Depends(get_tenant),
    user: User = Depends(require_role("viewer", "admin")),
):
    # helper to send SSE event
    def sse(event: str, data: dict) -> str:
        return f"event: {event}\n" f"data: {json.dumps(data, ensure_ascii=False)}\n\n"

    # basic prompt-injection guard
    if detect_prompt_injection(q):
        def gen_blocked():
            yield sse("error", {"message": "Prompt injection detected"})
        return StreamingResponse(gen_blocked(), media_type="text/event-stream", headers=SSE_HEADERS)

    start = time.perf_counter()
    trace_id = f"{user.sub}-{int(time.time())}"

    def gen():
        try:
            # --- Retrieval ---
            items = retriever.retrieve(q, tenant)
            context, kept = build_context(items, max_chars=900)

            # --- LLM ---
            answer, tokens_est = llm.answer(q, context)
            citations = format_citations(kept)

            latency_ms = int((time.perf_counter() - start) * 1000)

            # --- Audit log ---
            db = SessionLocal()
            try:
                db.add(
                    AuditLog(
                        trace_id=trace_id,
                        tenant=tenant,
                        user_sub=user.sub,
                        question=q,
                        latency_ms=latency_ms,
                        cost_tokens_est=tokens_est,
                        retrieval_hits=len(kept),
                    )
                )
                db.commit()
            finally:
                db.close()

            # --- Stream meta first ---
            yield sse(
                "meta",
                {
                    "trace_id": trace_id,
                    "latency_ms": latency_ms,
                    "retrieval_hits": len(kept),
                    "tokens_est": tokens_est,
                },
            )

            # --- Stream answer in chunks ---
            chunk_size = 120
            for i in range(0, len(answer), chunk_size):
                yield sse("chunk", {"text": answer[i : i + chunk_size]})
                time.sleep(0.03)

            # --- Done with citations ---
            yield sse("done", {"citations": citations})

        except Exception as e:
            # Make errors visible to frontend via SSE
            yield sse("error", {"message": f"Server error: {str(e)}"})

    return StreamingResponse(gen(), media_type="text/event-stream", headers=SSE_HEADERS)

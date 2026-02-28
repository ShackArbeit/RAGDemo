# 檔案說明: LLM 介面；可用 mock 回答或 OpenAI Responses API，並估算 token。
from app.core.config import settings
from app.core.security import sanitize_output
from openai import OpenAI

def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)

class LLMGateway:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    def answer(self, question: str, context: str) -> tuple[str, int]:
        provider = (settings.llm_provider or "mock").lower()

        # ---- MOCK ----
        if provider != "openai":
            if not context.strip():
                text = "I couldn't find relevant internal knowledge. Please refine your question."
            else:
                text = (
                    "Based on internal sources, here's a concise answer:\n"
                    f"- Question: {question}\n"
                    "- Key points extracted from retrieved context.\n"
                    "If you need exact numbers, ask specifically (e.g., 'ACME orders')."
                )
            text = sanitize_output(text)
            return text, estimate_tokens(context + question + text)

        # ---- OPENAI ----
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY is missing but LLM_PROVIDER=openai")

        # 你可以改成 gpt-4.1 / gpt-4.1-mini / o4-mini / o3
        model = "gpt-4.1-mini"

        system = (
            "You are an enterprise assistant. Use ONLY the provided context. "
            "If context is insufficient, say so and ask for clarification. "
            "Keep answer concise and factual."
        )

        # Responses API: create a response with input items
        resp = self.client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system},
                {
                    "role": "user",
                    "content": f"QUESTION:\n{question}\n\nCONTEXT:\n{context}",
                },
            ],
        )

        # Extract text output (robustly)
        out_text = ""
        for item in getattr(resp, "output", []) or []:
            for c in getattr(item, "content", []) or []:
                if getattr(c, "type", "") == "output_text":
                    out_text += getattr(c, "text", "")

        out_text = sanitize_output(out_text.strip() or "No output.")
        tokens_est = estimate_tokens(context + question + out_text)  # demo估算
        return out_text, tokens_est

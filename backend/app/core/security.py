# 檔案說明: Prompt injection 偵測與基本輸出清理。
import re

BLOCK_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"reveal\s+system\s+prompt",
    r"dump\s+secrets?",
]

def detect_prompt_injection(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in BLOCK_PATTERNS)

def sanitize_output(text: str) -> str:
    # basic output hardening (demo-level)
    return text.replace("\x00", "")

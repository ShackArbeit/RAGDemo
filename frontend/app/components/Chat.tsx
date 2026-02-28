"use client";

// 檔案說明: 聊天 UI；取得 dev token，透過 SSE 呼叫後端 /chat/stream，並顯示 Meta/答案/引用。

import { useEffect, useMemo, useState } from "react";

type Citation = { n: number; kind: string; title: string; source: any };

export default function Chat() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
  const [token, setToken] = useState<string>("");
  const [q, setQ] = useState("Show ACME orders");
  const [answer, setAnswer] = useState("");
  const [meta, setMeta] = useState<any>(null);
  const [cites, setCites] = useState<Citation[]>([]);
  const [error, setError] = useState<string>("");

  useEffect(() => {
    fetch(`${API_BASE}/chat/dev-token`)
      .then((r) => r.json())
      .then((d) => setToken(d.token))
      .catch(() => setToken(""));
  }, [API_BASE]);

  const headers = useMemo(() => {
    return token ? { Authorization: `Bearer ${token}` } : {};
  }, [token]);

  const ask = async () => {
    setError("");
    setAnswer("");
    setMeta(null);
    setCites([]);

    const url = new URL(`${API_BASE}/chat/stream`);
    url.searchParams.set("q", q);

    // SSE via fetch + ReadableStream
    const res = await fetch(url.toString(), { headers });
    if (!res.ok || !res.body) {
      setError(`HTTP ${res.status}`);
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buf = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buf += decoder.decode(value, { stream: true });

      // parse SSE frames
      const parts = buf.split("\n\n");
      buf = parts.pop() || "";

      for (const frame of parts) {
        const lines = frame.split("\n").filter(Boolean);
        const evt = lines.find((l) => l.startsWith("event:"))?.replace("event:", "").trim();
        const dataLine = lines.find((l) => l.startsWith("data:"))?.replace("data:", "").trim();
        if (!evt || !dataLine) continue;

        const data = JSON.parse(dataLine);

        if (evt === "error") setError(data.message || "error");
        if (evt === "meta") setMeta(data);
        if (evt === "chunk") setAnswer((prev) => prev + (data.text || ""));
        if (evt === "done") setCites(data.citations || []);
      }
    }
  };

  return (
    <div style={{ marginTop: 16, maxWidth: 900 }}>
      <div style={{ display: "flex", gap: 8 }}>
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          style={{ flex: 1, padding: 10, borderRadius: 8, border: "1px solid #ccc" }}
        />
        <button onClick={ask} style={{ padding: "10px 14px", borderRadius: 8 }}>
          Ask
        </button>
      </div>

      {error && <p style={{ color: "crimson" }}>⚠️ {error}</p>}

      {meta && (
        <div style={{ marginTop: 12, padding: 12, border: "1px solid #eee", borderRadius: 10 }}>
          <b>Meta</b>
          <div style={{ color: "#555" }}>
            trace_id: {meta.trace_id} <br />
            latency_ms: {meta.latency_ms} <br />
            hits: {meta.retrieval_hits} <br />
            tokens_est: {meta.tokens_est}
          </div>
        </div>
      )}

      <div style={{ marginTop: 12, padding: 12, border: "1px solid #eee", borderRadius: 10 }}>
        <b>Answer</b>
        <pre style={{ whiteSpace: "pre-wrap", marginTop: 8 }}>{answer || "..."}</pre>
      </div>

      <div style={{ marginTop: 12, padding: 12, border: "1px solid #eee", borderRadius: 10 }}>
        <b>Citations</b>
        {cites.length === 0 ? (
          <p style={{ color: "#666" }}>No citations</p>
        ) : (
          <ol>
            {cites.map((c) => (
              <li key={c.n}>
                [{c.kind}] {c.title} — <code>{JSON.stringify(c.source)}</code>
              </li>
            ))}
          </ol>
        )}
      </div>

      <div style={{ marginTop: 12, color: "#666" }}>
        Try:
        <ul>
          <li><code>Show ACME orders</code> (SQL)</li>
          <li><code>ACME relations</code> (Graph)</li>
          <li><code>How to reset password</code> (Vector)</li>
        </ul>
      </div>
    </div>
  );
}

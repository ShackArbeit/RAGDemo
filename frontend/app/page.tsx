// 檔案說明: 首頁，呈現專案標題與聊天元件。
import Chat from "./components/Chat";

export default function Page() {
  return (
    <main style={{ padding: 20, fontFamily: "system-ui" }}>
      <h1>Systex Mini Hybrid-RAG Demo</h1>
      <p style={{ color: "#666" }}>
        Demo: Mock SSO + Tenant + RBAC + Hybrid Retrieval (Vector/SQL/Graph) + Citations + Observability
      </p>
      <Chat />
    </main>
  );
}

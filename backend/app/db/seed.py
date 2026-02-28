from app.db.init_db import SessionLocal
from app.db.models import Customer, Order

def seed_sql():
    db = SessionLocal()
    try:
        if db.query(Customer).count() > 0:
            return
        db.add_all([
            Customer(id=1, tenant="t1", name="ACME", status="active"),
            Customer(id=2, tenant="t1", name="Beta Corp", status="inactive"),
        ])
        db.add_all([
            Order(id=100, tenant="t1", customer_id=1, total=120000),
            Order(id=101, tenant="t1", customer_id=1, total=9000),
            Order(id=200, tenant="t1", customer_id=2, total=3000),
        ])
        db.commit()
    finally:
        db.close()

# "Docs" for vector retrieval (in-memory)
DOCS = [
    {
        "id": "doc-001",
        "tenant": "t1",
        "title": "FAQ - Password Reset",
        "text": "To reset password: go to Settings > Security > Reset Password. SSO users must contact admin.",
        "source": {"type": "doc", "uri": "kb://faq/password-reset"},
    },
    {
        "id": "doc-002",
        "tenant": "t1",
        "title": "User Manual - Orders",
        "text": "Orders belong to a customer. Use customer_id to join. High-value orders are above 100000.",
        "source": {"type": "doc", "uri": "kb://manual/orders"},
    },
]

# simple "graph" edges (customer -> related entities)
GRAPH = {
    "ACME": ["Order#100", "Order#101", "AccountManager:Alice"],
    "Beta Corp": ["Order#200", "AccountManager:Bob"],
}
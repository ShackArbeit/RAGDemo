from sqlalchemy import select
from app.db.init_db import SessionLocal
from app.db.models import Customer, Order

class SQLRetriever:
    def query(self, question: str, tenant: str):
        # demo heuristic "NL -> SQL"
        q = question.lower()
        db = SessionLocal()
        try:
            if "order" in q and "acme" in q:
                cust = db.execute(select(Customer).where(Customer.tenant==tenant, Customer.name=="ACME")).scalar_one()
                orders = db.execute(select(Order).where(Order.tenant==tenant, Order.customer_id==cust.id)).scalars().all()
                text = "ACME orders: " + ", ".join([f"#{o.id} total={o.total}" for o in orders])
                return [{
                    "kind": "sql",
                    "id": "sql-acme-orders",
                    "title": "SQL: ACME Orders",
                    "text": text,
                    "score": 0.9,
                    "source": {"type": "db", "uri": "sqlite://orders?customer=ACME"},
                }]
            if "customer" in q and "status" in q:
                customers = db.execute(select(Customer).where(Customer.tenant==tenant)).scalars().all()
                text = "Customers: " + ", ".join([f"{c.name}({c.status})" for c in customers])
                return [{
                    "kind": "sql",
                    "id": "sql-customers",
                    "title": "SQL: Customers",
                    "text": text,
                    "score": 0.7,
                    "source": {"type": "db", "uri": "sqlite://customers"},
                }]
            return []
        finally:
            db.close()
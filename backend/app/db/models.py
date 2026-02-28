from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Text

class Base(DeclarativeBase):
    pass

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trace_id: Mapped[str] = mapped_column(String(64))
    tenant: Mapped[str] = mapped_column(String(32))
    user_sub: Mapped[str] = mapped_column(String(64))
    question: Mapped[str] = mapped_column(Text)
    latency_ms: Mapped[int] = mapped_column(Integer)
    cost_tokens_est: Mapped[int] = mapped_column(Integer)
    retrieval_hits: Mapped[int] = mapped_column(Integer)

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant: Mapped[str] = mapped_column(String(32))
    name: Mapped[str] = mapped_column(String(64))
    status: Mapped[str] = mapped_column(String(32))

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant: Mapped[str] = mapped_column(String(32))
    customer_id: Mapped[int] = mapped_column(Integer)
    total: Mapped[int] = mapped_column(Integer)
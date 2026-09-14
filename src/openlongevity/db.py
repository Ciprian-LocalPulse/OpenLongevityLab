"""Optional async PostgreSQL persistence boundary."""

from dataclasses import dataclass
from typing import Any

try:
    from sqlalchemy import JSON, Float, Integer, String, Text, text
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
except ImportError:  # pragma: no cover - optional dependency
    SQLALCHEMY_AVAILABLE = False
else:
    SQLALCHEMY_AVAILABLE = True


if SQLALCHEMY_AVAILABLE:

    class Base(DeclarativeBase):
        """Declarative base for the persistence layer."""

    class PublicationRow(Base):
        __tablename__ = "publications"
        identifier: Mapped[str] = mapped_column(String(160), primary_key=True)
        title: Mapped[str] = mapped_column(Text)
        source: Mapped[str] = mapped_column(String(80), index=True)
        doi: Mapped[str | None] = mapped_column(String(255), unique=True, index=True)
        publication_date: Mapped[str | None] = mapped_column(String(32), index=True)
        provenance: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    class EvidenceRow(Base):
        __tablename__ = "evidence_records"
        identifier: Mapped[str] = mapped_column(String(160), primary_key=True)
        publication_identifier: Mapped[str | None] = mapped_column(String(160), index=True)
        study_type: Mapped[str] = mapped_column(String(64), index=True)
        evidence_level: Mapped[str] = mapped_column(String(1), index=True)
        species: Mapped[str] = mapped_column(String(120))
        endpoint: Mapped[str] = mapped_column(Text)
        confidence: Mapped[float] = mapped_column(Float)
        sample_size: Mapped[int | None] = mapped_column(Integer)
        provenance: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    class GraphEdgeRow(Base):
        __tablename__ = "graph_edges"
        subject: Mapped[str] = mapped_column(String(160), primary_key=True)
        relation: Mapped[str] = mapped_column(String(80), primary_key=True)
        object: Mapped[str] = mapped_column(String(160), primary_key=True)

else:
    Base = None  # type: ignore[assignment,misc]
    PublicationRow = None  # type: ignore[assignment,misc]
    EvidenceRow = None  # type: ignore[assignment,misc]
    GraphEdgeRow = None  # type: ignore[assignment,misc]


@dataclass
class Database:
    """Create sessions and health checks for a configured async database URL."""

    url: str
    engine: Any = None
    sessions: Any = None

    def __post_init__(self) -> None:
        if not SQLALCHEMY_AVAILABLE:
            raise RuntimeError("Install openlongevity[db] for PostgreSQL persistence")
        self.engine = create_async_engine(self.url, pool_pre_ping=True, pool_recycle=1800)
        self.sessions = async_sessionmaker(self.engine, expire_on_commit=False)

    async def create_schema(self) -> None:
        async with self.engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def health(self) -> str:
        try:
            async with self.engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
            return "ok"
        except Exception:  # noqa: BLE001 - health must never crash the API
            return "unavailable"

    async def close(self) -> None:
        await self.engine.dispose()

"""Async PostgreSQL storage. Schema changes are exclusively Alembic migrations."""
from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class PublicationRow(Base):
    __tablename__ = "publications"
    __table_args__ = (UniqueConstraint("provider", "source_identifier"),)
    identifier: Mapped[str] = mapped_column(String(160), primary_key=True)
    provider: Mapped[str] = mapped_column(String(40))
    source_identifier: Mapped[str] = mapped_column(String(100))
    title: Mapped[str] = mapped_column(Text)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    content_hash: Mapped[str] = mapped_column(String(64))
    revision: Mapped[int] = mapped_column(Integer)
    first_retrieved_at: Mapped[str] = mapped_column(String(40))
    last_retrieved_at: Mapped[str] = mapped_column(String(40))


class PublicationRevisionRow(Base):
    __tablename__ = "publication_revisions"
    publication_id: Mapped[str] = mapped_column(
        ForeignKey("publications.identifier", ondelete="CASCADE"), primary_key=True
    )
    revision: Mapped[int] = mapped_column(Integer, primary_key=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)
    content_hash: Mapped[str] = mapped_column(String(64))
    retrieved_at: Mapped[str] = mapped_column(String(40))


class Database:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url, pool_pre_ping=True)
        self.sessions = async_sessionmaker(self.engine, expire_on_commit=False)

    async def health(self) -> str:
        try:
            async with self.engine.connect() as connection:
                await connection.execute(text("SELECT version_num FROM alembic_version"))
            return "ok"
        except Exception:
            return "unavailable"

    async def close(self) -> None:
        await self.engine.dispose()


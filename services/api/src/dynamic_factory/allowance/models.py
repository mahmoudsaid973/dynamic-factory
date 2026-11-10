"""Allowance ledger ORM models."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dynamic_factory.db import Base


class AllowanceLedger(Base):
    """Tracks per-scope budget windows and consumption."""

    __tablename__ = "allowance_ledgers"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    scope: Mapped[str] = mapped_column(String(32), nullable=False)
    scope_id: Mapped[str] = mapped_column(String(255), nullable=False)
    window_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    window_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    max_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    used_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reserved_units: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    extra: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))

    reservations: Mapped[list["AllowanceReservation"]] = relationship(
        back_populates="ledger",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class AllowanceReservation(Base):
    """A hold against an allowance ledger for a pending operation."""

    __tablename__ = "allowance_reservations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    ledger_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("allowance_ledgers.id", ondelete="CASCADE"),
        nullable=False,
    )
    run_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    invocation_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    units: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        default="held",
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(UTC))
    released_at: Mapped[datetime | None] = mapped_column(nullable=True)

    ledger: Mapped["AllowanceLedger"] = relationship(back_populates="reservations")

"""Allowance ledger API routes."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dynamic_factory.allowance.models import AllowanceLedger, AllowanceReservation
from dynamic_factory.allowance.schemas import (
    AllowanceLedgerCreate,
    AllowanceLedgerRead,
    AllowanceReservationCreate,
    AllowanceReservationRead,
)
from dynamic_factory.db import get_db

router = APIRouter(prefix="/api/v1/allowance", tags=["allowance"])


@router.post("/ledgers", response_model=AllowanceLedgerRead, status_code=status.HTTP_201_CREATED)
async def create_ledger(
    data: AllowanceLedgerCreate,
    session: AsyncSession = Depends(get_db),
) -> AllowanceLedger:
    """Create a new allowance ledger for a scope."""
    ledger = AllowanceLedger(
        scope=data.scope,
        scope_id=data.scope_id,
        window_start=data.window_start,
        window_end=data.window_end,
        max_units=data.max_units,
        extra=data.extra,
    )
    session.add(ledger)
    await session.commit()
    await session.refresh(ledger)
    return ledger


@router.get("/ledgers", response_model=list[AllowanceLedgerRead])
async def list_ledgers(
    scope: str | None = None,
    session: AsyncSession = Depends(get_db),
) -> list[AllowanceLedger]:
    """List allowance ledgers."""
    query = select(AllowanceLedger)
    if scope:
        query = query.where(AllowanceLedger.scope == scope)
    result = await session.execute(query.order_by(AllowanceLedger.created_at.desc()))
    return list(result.scalars().all())


@router.get("/ledgers/{ledger_id}", response_model=AllowanceLedgerRead)
async def get_ledger(
    ledger_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> AllowanceLedger:
    """Fetch a single ledger."""
    ledger = await session.get(AllowanceLedger, ledger_id)
    if ledger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ledger not found")
    return ledger


@router.post(
    "/ledgers/{ledger_id}/reserve",
    response_model=AllowanceReservationRead,
    status_code=status.HTTP_201_CREATED,
)
async def reserve_units(
    ledger_id: uuid.UUID,
    data: AllowanceReservationCreate,
    session: AsyncSession = Depends(get_db),
) -> AllowanceReservation:
    """Reserve units against a ledger."""
    ledger = await session.get(AllowanceLedger, ledger_id)
    if ledger is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ledger not found")

    available = ledger.max_units - ledger.used_units - ledger.reserved_units
    if data.units > available:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Insufficient allowance",
        )

    reservation = AllowanceReservation(
        ledger_id=ledger_id,
        run_id=data.run_id,
        invocation_id=data.invocation_id,
        units=data.units,
        status="held",
    )
    ledger.reserved_units += data.units
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)
    return reservation


@router.post("/reservations/{reservation_id}/release", response_model=AllowanceReservationRead)
async def release_reservation(
    reservation_id: uuid.UUID,
    session: AsyncSession = Depends(get_db),
) -> AllowanceReservation:
    """Release a held reservation."""
    reservation = await session.get(AllowanceReservation, reservation_id)
    if reservation is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")

    if reservation.status == "held":
        ledger = await session.get(AllowanceLedger, reservation.ledger_id)
        if ledger is not None:
            ledger.reserved_units -= reservation.units
        reservation.status = "released"
        from datetime import UTC, datetime

        reservation.released_at = datetime.now(UTC)
        await session.commit()
        await session.refresh(reservation)

    return reservation

from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import ResourceNotFoundException
from app.models import Consumer


async def get_consumers(db: AsyncSession, priority_gte: int = 1) -> Sequence[Consumer]:
    """Get all consumers including its power requirements"""

    result = await db.execute(
        select(Consumer)
        .options(selectinload(Consumer.power_requirements))
        .filter(Consumer.priority >= priority_gte))
    return result.scalars().all()


async def get_consumer(db: AsyncSession, consumer_id: int) -> Consumer:
    """Get a consumer by ID, including its power requirements"""
    result = await db.execute(
        select(Consumer)
        .options(selectinload(Consumer.power_requirements))
        .filter(Consumer.id == consumer_id)
    )
    consumer = result.scalar_one_or_none()
    if not consumer:
        raise ResourceNotFoundException(
            type="Consumer", identifier=f"{consumer_id}")

    return consumer

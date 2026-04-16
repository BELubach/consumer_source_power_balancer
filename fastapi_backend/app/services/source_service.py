from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import ResourceNotFoundException
from app.models import Source


async def get_sources(db: AsyncSession, include_power_details: bool = True) -> Sequence[Source]:
    """Get all sources including its power requirements"""

    query = select(Source)
    if include_power_details:
        query = query.options(selectinload(Source.power_requirements))

    result = await db.execute(query)

    return result.scalars().all()


async def get_source(db: AsyncSession, source_id: int) -> Source:
    """Get a source by ID, including its power requirements"""
    result = await db.execute(
        select(Source)
        .options(selectinload(Source.power_requirements))
        .filter(Source.id == source_id)
    )
    source = result.scalar_one_or_none()
    if not source:
        raise ResourceNotFoundException(
            type="Source", identifier=f"{source_id}")

    return source


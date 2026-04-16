from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import ResourceNotFoundException
from app.models import Source
from app.schemas.sources import SourceResponse, RequiredPowerBase


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



async def map_source_to_response(source: Source, include_power_details: bool = True) -> SourceResponse:
    """Map a Source model to a SourceResponse schema, optionally including power requirements"""

    required_power = [
        RequiredPowerBase(
            consumer_id=pr.consumer_id,
            source_id=pr.source_id,
            capacity=pr.capacity,
            is_active=pr.is_active
        )
        for pr in source.power_requirements
    ] if include_power_details else []

    requested_power = sum(
        pr.capacity for pr in source.power_requirements
    ) if include_power_details else 0

    if source.capacity > 0 and requested_power is not None:
        utilization = requested_power / source.capacity
    else:        
        utilization = 0.0
    
    return SourceResponse(
        id=source.id,
        name=source.name,
        capacity=source.capacity,
        required_power=required_power,
        utilization=utilization,
        requested_power=requested_power
    )
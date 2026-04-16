from typing import Sequence, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.core.exceptions import ResourceNotFoundException
from app.models import Consumer, ConsumerPowerRequirement
from app.schemas.consumers import ConsumerResponse, RequiredPowerBase

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


async def update_consumer_power(db: AsyncSession, consumer_id: int, is_active: bool) -> Consumer:
    """Update ConsumerPowerRequirements power status for a specific source"""

    # check if the consumer exists
    await get_consumer(db, consumer_id)

    result = await db.execute(
        select(ConsumerPowerRequirement).filter(
            ConsumerPowerRequirement.consumer_id == consumer_id,
        )
    )

    for row in result.scalars().all():
        await _update_power_requirement(db, row, is_active)

    result = await db.execute(
        select(Consumer)
        .options(selectinload(Consumer.power_requirements))
        .filter(Consumer.id == consumer_id)
    )
    return result.scalar_one_or_none()


async def reduce_consumer_power_by_priority(db: AsyncSession, priority_threshold: int) -> None:
    """Reduce power requirements based on priority threshold"""

    consumers_with_higher_priority = await db.execute(
        select(Consumer)
        .options(selectinload(Consumer.power_requirements))
        .filter(Consumer.priority >= priority_threshold)
    )

    for consumer in consumers_with_higher_priority.scalars().all():
        for pr in consumer.power_requirements:
            await _update_power_requirement(db, pr, False)

async def _update_power_requirement(db: AsyncSession, required_power_obj: ConsumerPowerRequirement, is_active: bool) -> Optional[ConsumerPowerRequirement]:
    """Update ConsumerPowerRequirements power status for a specific source"""

    required_power_obj.is_active = is_active

    db.add(required_power_obj)

    await db.flush()
    await db.refresh(required_power_obj)
    return required_power_obj




async def map_consumer_to_response(consumer: Consumer, include_power_details: bool = True) -> ConsumerResponse:
    """Map Consumer model to ConsumerResponse schema"""

    active_power=sum(pr.capacity for pr in consumer.power_requirements if pr.is_active)

    if include_power_details:
        return ConsumerResponse(
            id=consumer.id,
            name=consumer.name,
            priority=consumer.priority,
            required_power=[RequiredPowerBase(
                consumer_id=pr.consumer_id,
                source_id=pr.source_id,
                capacity=pr.capacity,
                is_active=pr.is_active
            ) for pr in consumer.power_requirements],
            active_power=active_power
        )
    else:
        return ConsumerResponse(
            id=consumer.id,
            name=consumer.name,
            priority=consumer.priority,
            active_power=active_power
        )



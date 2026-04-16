from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import ConsumerResponse, ToggleConsumerRequest, ReduceConsumerPowerRequest
from app.services.consumer_service import map_consumer_to_response, update_consumer_power, get_consumers, reduce_consumer_power_by_priority


router = APIRouter()


@router.post("/deactivate-by-priority", response_model=List[ConsumerResponse])
async def reduce_consumer_power(
    reduce_power_request: ReduceConsumerPowerRequest,
    db: AsyncSession = Depends(get_db),
):
    """ Reduce consumer power requirement """
    await reduce_consumer_power_by_priority(db, reduce_power_request.priority_threshold)

    consumers = await get_consumers(db)
    response_data = [await map_consumer_to_response(c) for c in consumers]

    return response_data


@router.get("", response_model=List[ConsumerResponse])
async def list_consumers(db: AsyncSession = Depends(get_db),
                         priority_gte: int = 1,
                         include_power_details: bool = True
                         ) -> List[ConsumerResponse]:
    
    """Returns all consumers and power requirements
    Query param priority_threshold for filtering consumers, all consumers with priority greater than or equal to the threshold will be returned. 
    """

    consumers = await get_consumers(db, priority_gte=priority_gte)

    data = [
        await map_consumer_to_response(c, include_power_details=include_power_details)
        for c in consumers]
    return data


@router.patch("/{consumer_id}", response_model=ConsumerResponse)
async def modify_consumer_power(
    consumer_id: int,
    consumer_update: ToggleConsumerRequest,
    db: AsyncSession = Depends(get_db),
):
    """ Update a consumers' power status, allows turning the consumer on/off. """
    updated_consumer = await update_consumer_power(db, consumer_id, consumer_update.is_active)

    return await map_consumer_to_response(updated_consumer)

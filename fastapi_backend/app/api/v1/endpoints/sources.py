
from fastapi import APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.db.session import get_db
from app.services.source_service import get_sources, map_source_to_response


router = APIRouter()


@router.get("", response_model=list)
async def list_sources(
    db: AsyncSession = Depends(get_db),
    include_power_details: bool = True
):
    """Returns all sources and their power requirements"""

    sources = await get_sources(db, include_power_details=include_power_details)

    data = [
        await map_source_to_response(s, include_power_details=include_power_details) 
        for s in sources]
    return data
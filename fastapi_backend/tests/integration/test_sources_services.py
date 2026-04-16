import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.exceptions import ResourceNotFoundException
from app.db.base import Base
from app.models.powergrid_models import Consumer, Source, ConsumerPowerRequirement
from app.services.source_service import (
    get_source,
    get_sources,
)

@pytest.fixture
async def test_db():
    """ Setup in mem db, using aiossqlite for asyn testing wihthout full docker setup """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture 
async def generate_sources(test_db: AsyncSession):
    source1 = Source(id=1, name="Source 1", capacity=250)
    source2 = Source(id=2, name="Source 2", capacity=430)

    consumer1 = Consumer(id=1, name="Consumer 1", priority=1)
    consumer1.power_requirements.append(ConsumerPowerRequirement(
        consumer_id=1,
        source_id=1,
        capacity=100,
        is_active=True
    ))
    
    consumer2 = Consumer(id=2, name="Consumer 2", priority=2)
    consumer2.power_requirements.append(ConsumerPowerRequirement(
        consumer_id=2,
        source_id=1,
        capacity=150,
        is_active=True
    ))
    consumer2.power_requirements.append(ConsumerPowerRequirement(
        consumer_id=2,
        source_id=2,
        capacity=200,
        is_active=True
    ))
    
    test_db.add_all([consumer1, consumer2, source1, source2])
    await test_db.commit()
    return {"consumer1": consumer1, "consumer2": consumer2, "source1": source1, "source2": source2}
 

@pytest.mark.integration
async def test_get_all_sources(test_db: AsyncSession, generate_sources: dict):  # type: ignore , unused-argument but called to geenrate data
    sources = await get_sources(test_db, include_power_details=False)
    
    assert sources[0].name == "Source 1"
    assert sources[0].capacity == 250

    assert sources[1].name == "Source 2"
    assert sources[1].capacity == 430


@pytest.mark.integration
async def test_get_all_sources_with_powerdetails(test_db: AsyncSession, generate_sources: dict):  # type: ignore , unused-argument but called to geenrate data

    result = await get_sources(test_db, include_power_details=True)
    
    assert result[0].name == "Source 1"
    assert result[0].capacity == 250
    assert len(result[0].power_requirements) == 2
    assert result[0].power_requirements[0].consumer_id == 1
    assert result[0].power_requirements[0].capacity == 100
    assert result[0].power_requirements[0].is_active == True
    assert result[0].power_requirements[1].consumer_id == 2
    assert result[0].power_requirements[1].capacity == 150
    assert result[0].power_requirements[1].is_active == True

    assert result[1].name == "Source 2"
    assert result[1].capacity == 430
    assert len(result[1].power_requirements) == 1
    assert result[1].power_requirements[0].consumer_id == 2
    assert result[1].power_requirements[0].capacity == 200
    assert result[1].power_requirements[0].is_active == True
    

@pytest.mark.integration
async def test_get_source(test_db: AsyncSession, generate_sources: dict):  #
    result = await get_source(test_db, 1)
    
    assert result.name == "Source 1"
    assert result.capacity == 250
    assert len(result.power_requirements) == 2
    assert result.power_requirements[0].consumer_id == 1
    assert result.power_requirements[0].capacity == 100
    assert result.power_requirements[0].is_active == True
    assert result.power_requirements[1].consumer_id == 2
    assert result.power_requirements[1].capacity == 150
    assert result.power_requirements[1].is_active == True


@pytest.mark.integration
async def test_get_source_not_found(test_db: AsyncSession):
    with pytest.raises(ResourceNotFoundException):
        await get_source(test_db, 999)




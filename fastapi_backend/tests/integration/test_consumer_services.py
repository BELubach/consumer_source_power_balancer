import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.exceptions import ResourceNotFoundException
from app.db.base import Base
from app.models.powergrid_models import Consumer, ConsumerPowerRequirement
from app.services.consumer_service import (
    _update_power_requirement,          # pyright: ignore[reportPrivateUsage]
    get_consumer,
    get_consumers, 
    update_consumer_power, 
    reduce_consumer_power_by_priority, 
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
async def generate_consumers(test_db: AsyncSession):
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
    
    test_db.add_all([consumer1, consumer2])
    await test_db.commit()
    return {"consumer1": consumer1, "consumer2": consumer2}
 

@pytest.mark.integration
async def test_get_all_consumers(test_db: AsyncSession, generate_consumers: dict):  # type: ignore , unused-argument but called to geenrate data
    consumers = await get_consumers(test_db)
    
    assert consumers[0].name == "Consumer 1"
    assert len(consumers[0].power_requirements) == 1
    assert consumers[0].power_requirements[0].capacity == 100
    assert consumers[0].power_requirements[0].is_active == True

    assert consumers[1].name == "Consumer 2"
    assert len(consumers[1].power_requirements) == 2
    assert consumers[1].power_requirements[0].capacity == 150
    assert consumers[1].power_requirements[0].is_active == True
    assert consumers[1].power_requirements[1].capacity == 200
    assert consumers[1].power_requirements[1].is_active == True


@pytest.mark.integration
async def test_get_consumer(test_db: AsyncSession, generate_consumers: dict):  # type: ignore , unused-argument but called to geenrate data

    result = await get_consumer(test_db, 1)
    
    assert len(result.power_requirements) == 1

@pytest.mark.integration
async def test_get_consumer_not_found(test_db: AsyncSession):
    with pytest.raises(ResourceNotFoundException):
        await get_consumer(test_db, 999)



@pytest.mark.integration
async def test_update_consumer_power(test_db: AsyncSession, generate_consumers: dict):  # type: ignore , unused-argument but called to geenrate data

    updated_consumer = await update_consumer_power(test_db, 2, False)
    
    assert updated_consumer.id == 2
    assert len(updated_consumer.power_requirements) == 2
    assert updated_consumer.power_requirements[0].is_active == False
    assert updated_consumer.power_requirements[0].capacity == 150
    assert updated_consumer.power_requirements[1].is_active == False
    assert updated_consumer.power_requirements[1].capacity == 200


@pytest.mark.integration
async def test_update_consumer_power_not_found(test_db: AsyncSession):
    with pytest.raises(ResourceNotFoundException):
        await update_consumer_power(test_db, 999, False)


@pytest.mark.integration
async def test_reduce_consumer_power_by_priority(test_db: AsyncSession, generate_consumers: dict):  # type: ignore , unused-argument but called to geenrate data

    await reduce_consumer_power_by_priority(test_db, priority_threshold=2)

    consumer1 = await get_consumer(test_db, 1)
    consumer2 = await get_consumer(test_db, 2)

    assert consumer1.power_requirements[0].is_active == True
    assert consumer2.power_requirements[0].is_active == False
    assert consumer2.power_requirements[1].is_active == False


@pytest.mark.integration
async def test_reduce_consumer_power_by_priority_no_match(test_db: AsyncSession, generate_consumers: dict):   # type: ignore , unused-argument but called to geenrate data

    await reduce_consumer_power_by_priority(test_db, priority_threshold=3)

    consumer1 = await get_consumer(test_db, 1)
    consumer2 = await get_consumer(test_db, 2)

    assert consumer1.power_requirements[0].is_active == True
    assert consumer2.power_requirements[0].is_active == True
    assert consumer2.power_requirements[1].is_active == True


@pytest.mark.integration
async def test_update_power_requirement(test_db: AsyncSession, generate_consumers: dict[str, Consumer]):
    consumer2 = generate_consumers["consumer2"]
    existing_requirement = consumer2.power_requirements[0]   

    updated_power = await _update_power_requirement(test_db, existing_requirement, False)

    assert updated_power != None 
    assert updated_power.id == 2
    assert updated_power.consumer_id == 2
    assert updated_power.source_id == 1
    assert updated_power.capacity == 150
    assert updated_power.is_active == False

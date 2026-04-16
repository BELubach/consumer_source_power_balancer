
import pytest
from app.schemas.consumers import ConsumerResponse
from app.models import Consumer, ConsumerPowerRequirement
from app.services.consumer_service import map_consumer_to_response

@pytest.fixture 
async def generate_consumers():
    consumer1 = Consumer(id=1, name="Consumer 1", priority=1)
    consumer1.power_requirements.append(ConsumerPowerRequirement(
        id=1,
        consumer_id=1,
        source_id=1,
        capacity=100,
        is_active=True
    ))
    
    consumer2 = Consumer(id=2, name="Consumer 2", priority=2)
    consumer2.power_requirements.append(ConsumerPowerRequirement(
        id=2,
        consumer_id=2,
        source_id=1,
        capacity=150,
        is_active=True
    ))
    consumer2.power_requirements.append(ConsumerPowerRequirement(
        id=3,
        consumer_id=2,
        source_id=2,
        capacity=200,
        is_active=True
    ))
    
    return {"consumer1": consumer1, "consumer2": consumer2}

@pytest.mark.unit
async def test_map_consumer_to_response(generate_consumers: dict[str, Consumer]): 

    consumer = generate_consumers["consumer1"]
    consumer_response_obj = await map_consumer_to_response(consumer)

    assert type(consumer_response_obj) == ConsumerResponse
    assert consumer_response_obj.name == "Consumer 1"
    assert consumer_response_obj.priority == 1
    assert consumer_response_obj.active_power == 100
    assert consumer_response_obj.required_power is not None
    assert len(consumer_response_obj.required_power) == 1
    assert consumer_response_obj.required_power[0].source_id == 1
    assert consumer_response_obj.required_power[0].capacity == 100
    assert consumer_response_obj.required_power[0].is_active == True

    consumer = generate_consumers["consumer2"]
    consumer_response_obj = await map_consumer_to_response(consumer)
    assert type(consumer_response_obj) == ConsumerResponse
    assert consumer_response_obj.name == "Consumer 2"
    assert consumer_response_obj.priority == 2
    assert consumer_response_obj.active_power == 350
    assert consumer_response_obj.required_power is not None
    assert len(consumer_response_obj.required_power) == 2
    assert consumer_response_obj.required_power[0].source_id == 1
    assert consumer_response_obj.required_power[0].capacity == 150
    assert consumer_response_obj.required_power[0].is_active == True
    assert consumer_response_obj.required_power[1].source_id == 2
    assert consumer_response_obj.required_power[1].capacity == 200
    assert consumer_response_obj.required_power[1].is_active == True

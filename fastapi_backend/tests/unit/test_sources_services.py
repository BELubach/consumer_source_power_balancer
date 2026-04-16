
import pytest
from app.models import Consumer, ConsumerPowerRequirement, Source
from app.schemas.sources import SourceResponse
from app.services.source_service import map_source_to_response

@pytest.fixture 
async def generate_sources():
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

    source1.power_requirements.append(consumer1.power_requirements[0])
    source1.power_requirements.append(consumer2.power_requirements[0])
    source2.power_requirements.append(consumer2.power_requirements[1])
    
    return {"consumer1": consumer1, "consumer2": consumer2, "source1": source1, "source2": source2}
 

@pytest.mark.unit
async def test_map_source_to_response(generate_sources: dict[str, Source]): 

    source = generate_sources["source1"]
    source_response_obj = await map_source_to_response(source)

    assert isinstance(source_response_obj, SourceResponse)
    assert source_response_obj.name == "Source 1"
    assert source_response_obj.capacity == 250
    assert source_response_obj.utilization == 1.0
    assert source_response_obj.requested_power == 250
    assert source_response_obj.required_power is not None
    assert len(source_response_obj.required_power) == 2
    assert source_response_obj.required_power[0].consumer_id == 1
    assert source_response_obj.required_power[0].capacity == 100
    assert source_response_obj.required_power[0].is_active == True
    assert source_response_obj.required_power[1].consumer_id == 2
    assert source_response_obj.required_power[1].capacity == 150
    assert source_response_obj.required_power[1].is_active == True

    source = generate_sources["source2"]
    source_response_obj = await map_source_to_response(source)
    assert isinstance(source_response_obj, SourceResponse)
    assert source_response_obj.name == "Source 2"
    assert source_response_obj.capacity == 430
    assert source_response_obj.utilization == 200/430
    assert source_response_obj.requested_power == 200
    assert source_response_obj.required_power is not None
    assert len(source_response_obj.required_power) == 1
    assert source_response_obj.required_power[0].consumer_id == 2
    assert source_response_obj.required_power[0].capacity == 200
    assert source_response_obj.required_power[0].is_active == True
    


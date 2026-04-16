from pydantic import BaseModel
from typing import Optional


class ConsumerBase(BaseModel):
    id: int
    name: str
    priority: int

class RequiredPowerBase(BaseModel):
    source_id: int
    consumer_id: int
    capacity: int
    is_active: bool

class ConsumerResponse(ConsumerBase):
    required_power: Optional[list[RequiredPowerBase]] = None
    active_power: Optional[int] = None

class ToggleConsumerRequest(BaseModel):
    is_active: bool

class ReduceConsumerPowerRequest(BaseModel):
    priority_threshold: int
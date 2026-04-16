from pydantic import BaseModel
from app.schemas.consumers import RequiredPowerBase

class SourceBase(BaseModel):
    id: int
    name: str
    capacity: int


class SourceResponse(SourceBase):
    required_power: list[RequiredPowerBase] = []
    requested_power: int = 0
    utilization: float = 0.0

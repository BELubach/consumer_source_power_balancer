
from sqlalchemy import Integer, String
from app.db.session import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Consumer(Base):
    """Consumer model with name"""
    __tablename__ = "consumers"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f"<Consumer(id={self.id}, name={self.name}, priority={self.priority})>"
    

class Source(Base):
    """Source model with capacity"""
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
   
    def __repr__(self):
        return f"<Source(id={self.id}, name={self.name}, capacity={self.capacity})>"

class ConsumerPowerRequirement(Base):
    """ConsumerPowerRequirements model linking Consumer and Source with required power"""
    __tablename__ = "required_power"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    consumer_id: Mapped[int] = mapped_column(Integer, ForeignKey("consumers.id"), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey("sources.id"), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True) 
    
    consumer: Mapped["Consumer"] = relationship(back_populates="power_requirements")
    source: Mapped["Source"] = relationship(back_populates="power_requirements")

    def __repr__(self):
        return f"<ConsumerPowerRequirements(id={self.id}, consumer_id={self.consumer_id}, source_id={self.source_id}, capacity={self.capacity})>"


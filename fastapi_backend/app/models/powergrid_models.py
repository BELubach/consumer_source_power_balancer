
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


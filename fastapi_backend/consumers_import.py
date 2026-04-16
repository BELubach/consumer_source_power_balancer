
import json

from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine
from app.models import Consumer, Source, ConsumerPowerRequirement
from sqlalchemy import select

Base = declarative_base()
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL.replace("asyncpg", "psycopg2"), echo=True)


if __name__ == "__main__":
    session = Session(engine)
    
    sources = session.execute(select(Source)).scalars().all()

    with open("./data/consumers.json", "r") as f:
        data = json.load(f)

        for item in data["consumers"]:
            
            consumer = Consumer(name=item["name"], priority=item["priority"])
            session.add(consumer)
            session.flush()  # Flush to get the consumer.id
            
            required_powers = item.get("requiredPower", [])

            for rp in required_powers:
                sourceId = rp["sourceId"]
                capacity = rp["capacity"]

                if not any(int(s.id) == int(sourceId) for s in sources):
                    print(f"Source with id {sourceId} not found for consumer {consumer.name}")
                    continue
                
                required_power = ConsumerPowerRequirement(
                    consumer_id=consumer.id,
                    source_id=sourceId,
                    capacity=capacity
                )
                session.add(required_power)
    session.commit()  
    session.close()
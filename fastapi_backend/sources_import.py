
import json

from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import create_engine
from app.models import Source

Base = declarative_base()
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL.replace("asyncpg", "psycopg2"), echo=True)


if __name__ == "__main__":
    session = Session(engine)
    
    with open("./data/sources.json", "r") as f:
        data = json.load(f)
        for item in data["sources"]:
            source = Source(id=item["id"],name=item["name"], capacity=item["capacity"])
            session.add(source)

    session.commit()  
    session.close()
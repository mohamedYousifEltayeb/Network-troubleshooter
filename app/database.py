from app.models.ping_history import PingHistory
from sqlmodel import SQLModel, create_engine
from sqlmodel import Session

DATABASE_URL= "sqlite:///network.db"

engine = create_engine(DATABASE_URL, echo= True)

def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session (engine) as session:
        yield session

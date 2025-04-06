from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dashboard.database.models import Base

DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

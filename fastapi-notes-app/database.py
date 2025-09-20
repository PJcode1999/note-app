from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# SQLite database file path one level back
DATABASE_URL = os.getenv("DATABASE_URL")


# Engine creation
engine = create_engine(DATABASE_URL, echo=True)

# Create DB tables
def init_db():
    SQLModel.metadata.create_all(engine)

# Dependency for DB session
def get_session():
    with Session(engine) as session:
        yield session

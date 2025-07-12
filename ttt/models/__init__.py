from sqlmodel import SQLModel, create_engine, Session

from .model_user import *
from .model_activity import *

engine = create_engine("sqlite:///database.db")
session = Session(engine)


def create_db_and_tables():
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")

from .database import Base, engine, get_db
from . import models, crud

def create_tables():
    Base.metadata.create_all(bind=engine) 
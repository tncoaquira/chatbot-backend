from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import database
from sqlalchemyseed import load_entities_from_json
from sqlalchemyseed import Seeder

DATABASE_URL = database.Config.PG_RECORD_MANAGER
# TODO: cambiar el nombre de la base de datos por chatbot

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
db = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_seeds():
    entities = load_entities_from_json('/src/database/seeds/usuarios.json')
    seeder = Seeder(db)
    seeder.seed(entities)
    db.commit()
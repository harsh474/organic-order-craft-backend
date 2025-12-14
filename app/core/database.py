from sqlmodel import SQLModel, create_engine, Session
from app.config.settings import settings
from typing import Generator
from urllib.parse import quote_plus

MYSQL_DB_URL = (
    f"mysql+pymysql://{quote_plus(settings.MYSQL_USER)}:"
    f"{quote_plus(settings.MYSQL_PASSWORD)}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/"
    f"{settings.MYSQL_DB}"
)
engine = create_engine(MYSQL_DB_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

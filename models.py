from atexit import register

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

PG_USER = "postgres"
PG_PASSWORD = "111"
PG_DB = "flask_ad_db"
PG_HOST = "127.0.0.1"
PG_PORT = 5400
PG_DSN = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

Base = declarative_base()
engine = create_engine(PG_DSN)
register(engine.dispose)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = "users_adv"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


class Advertisements(Base):
    __tablename__ = "advertisements_table"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users_adv.id"), nullable=False)


def get_session():
    return Session()


Base.metadata.create_all(engine)

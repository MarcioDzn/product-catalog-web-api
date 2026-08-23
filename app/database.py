import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

Base = declarative_base()

url = URL.create(
    drivername=os.getenv("DRIVER"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    port=int(os.getenv("PORT")),
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)

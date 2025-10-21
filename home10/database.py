
import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from sqlalchemy.orm import declarative_base


BASE_DIR = os.path.dirname(__file__)
DB_DIR = os.path.join(BASE_DIR, 'db')
os.makedirs(DB_DIR, exist_ok=True)
Base = declarative_base()

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

DB_PATH = os.path.join(DB_DIR, 'fastapi.db')


engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}", echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)



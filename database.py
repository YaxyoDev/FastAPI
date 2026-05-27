# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:1@localhost:5434/TodoApplicationDatabase'

# Asinxron SQLite uchun URL manzil
SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///./TodoApplicationDatabase.db'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:177oo817!@127.0.0.1:3306/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

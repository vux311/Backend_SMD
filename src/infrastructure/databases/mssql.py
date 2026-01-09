from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from infrastructure.databases.base import Base

# Database configuration
DATABASE_URI = Config.DATABASE_URI

# For SQLite in a multithreaded Flask dev server, allow check_same_thread=False
connect_args = {}
if DATABASE_URI and DATABASE_URI.startswith('sqlite'):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URI, connect_args=connect_args)

# Use scoped_session for thread-local sessions and avoid instance expiration
# after commit to prevent DetachedInstanceError when serializing objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
session = scoped_session(SessionLocal)

def init_mssql(app):
    Base.metadata.create_all(bind=engine)
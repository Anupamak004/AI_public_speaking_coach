from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

database_name = "test"
username = "user"
password = "password"

DATABASE_URL = f"postgresql://{username}:{password}@localhost:5432/{database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse 

# 1. Try to get the Cloud DB URL from Environment Variable
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. If no cloud DB, use local fallback (Your hardcoded one)
if not DATABASE_URL:
    raw_password = "Somu@2006" 
    encoded_password = urllib.parse.quote_plus(raw_password)
    DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost:5432/command_gateway"
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
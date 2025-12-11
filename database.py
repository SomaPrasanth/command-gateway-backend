from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse

raw_password = "Somu@2006"
encoded_password = urllib.parse.quote_plus(raw_password)

# FORMAT: postgresql://user:password@localhost/dbname
DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost/command_gateway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session in endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
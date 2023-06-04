from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import DatabaseError

from src.conf.config import settings


DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, max_overflow=5)  #  echo=True,

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except DatabaseError:
        db.rollback()
    finally:
        db.close()

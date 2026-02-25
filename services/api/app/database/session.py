"""
Project: NishadRaj OS
Author: Jawahar R Mallah
Organization: AITDL
License: AGPL-3.0 + Governance Protection Terms
Copyright © Jawahar R Mallah | AITDL
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import time

# Retry logic — MariaDB may take a few seconds to start
engine = None
for attempt in range(10):
    try:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"✅ Auth DB connected (attempt {attempt + 1})")
        break
    except Exception as e:
        print(f"⏳ Auth DB attempt {attempt + 1}/10 failed: {e}")
        time.sleep(3)

if engine is None:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

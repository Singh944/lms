from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
from library_mgmt.config import get_settings


settings = get_settings()


class Base(DeclarativeBase):
    pass


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {},
    echo=settings.DEBUG,
)

SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



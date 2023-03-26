import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.main import app, get_db
from app.models import Base

engine = create_engine(
    "sqlite:///./test.sqlite3", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    """
    Create/destroy the test database on very test
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    """
    Use this fixture to query the test database
    """
    with TestingSessionLocal() as session:
        yield session


@pytest.fixture
def create(db: Session):
    """
    Use this fixture to save SQLModel instances to the database
    """

    def _create(obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    return _create

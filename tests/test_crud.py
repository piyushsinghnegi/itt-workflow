import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import crud, models
from app.database import Base

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_item(db):
    item = crud.create_item(db, name="Test Item", description="Test Desc")
    assert item.id is not None
    assert item.name == "Test Item"
    assert item.description == "Test Desc"


def test_get_items(db):
    crud.create_item(db, name="Item1", description="Desc1")
    crud.create_item(db, name="Item2", description="Desc2")
    items = crud.get_items(db)
    assert len(items) >= 2
    names = [item.name for item in items]
    assert "Item1" in names and "Item2" in names


def test_get_item(db):
    item = crud.create_item(db, name="Unique Item", description="Unique Desc")
    fetched = crud.get_item(db, item.id)
    assert fetched is not None
    assert fetched.name == "Unique Item"


def test_update_item(db):
    item = crud.create_item(db, name="Old Name", description="Old Desc")
    updated = crud.update_item(db, item.id, name="New Name", description="New Desc")
    assert updated.name == "New Name"
    assert updated.description == "New Desc"


def test_delete_item(db):
    item = crud.create_item(db, name="DeleteMe", description="To Delete")
    crud.delete_item(db, item.id)
    fetched = crud.get_item(db, item.id)
    assert fetched is None

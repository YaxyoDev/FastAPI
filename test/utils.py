from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker      
from main import app 
from fastapi.testclient import TestClient
import pytest
from models import Todos, Base, User
from router.auth import bcrypt_context

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Doing',
        description="Doing something",
        priority=3,
        complete=True,
        owner_id=1
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    db.refresh(todo)
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'yaxyo', 'user_id': 1, 'user_role': 'admin'}

@pytest.fixture
def test_user():
    user = User(
        username="yaxyo",
        email="yaxyo@gmail.com",
        first_name="Yaxyo",
        last_name="Bek",
        hashed_password=bcrypt_context.hash("qwerty1234"),
        role="admin",
        phone_number="+998942140551"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()


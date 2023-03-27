from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import Item, User, UserCreate, UserRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


def get_db():
    with Session(engine) as db:
        yield db


DataBase = Annotated[Session, Depends(get_db)]


@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: DataBase):
    users = db.exec(select(User).where(User.email == user.email)).all()
    if users:
        raise HTTPException(400, "Email already registered")
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[UserRead])
def read_users(db: DataBase, skip: int = 0, limit: int = 100):
    return db.exec(select(User).offset(skip).limit(limit)).all()


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(db: DataBase, user_id: int):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    return db_user


@app.get("/items/", response_model=list[Item])
def read_items(db: DataBase, skip: int = 0, limit: int = 100):
    return db.exec(select(Item).offset(skip).limit(limit)).all()

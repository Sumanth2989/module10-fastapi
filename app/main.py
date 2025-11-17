# app/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from . import schemas, crud, models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Secure User FastAPI App")


@app.post("/users/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_by_email = crud.get_user_by_email(db, email=user_in.email)
    if existing_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_by_username = crud.get_user_by_username(db, username=user_in.username)
    if existing_by_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    user = crud.create_user(db, user_in)
    return user


@app.get("/health")
def healthcheck():
    return {"status": "ok"}

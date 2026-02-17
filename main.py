
# custom
from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session

# project
from database import engine, SessionLocal, Base
from models import User as UserModel, Categories as CategoriesModel, Goals as GoalsModel
from schemas import UserResponse as UserResponseSchema, UserCreate, Goal as GoalSchema, GoalResponse

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users", response_model=List[UserResponseSchema])
def get_users(db: Session = Depends(get_db)) -> List[UserResponseSchema]:
    users = db.query(UserModel).all()
    return users


@app.post("/users", response_model=UserResponseSchema)
def create_users(user: UserCreate, db: Session = Depends(get_db)) -> UserResponseSchema:
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponseSchema:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/goal", response_model=GoalResponse)
def post_goal(goal: GoalResponse, db: Session = Depends(get_db)):
    db_goal = GoalSchema(**goal.dict())
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal





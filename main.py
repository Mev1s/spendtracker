
# custom
from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from typing import Optional, List, Dict, Union
from sqlalchemy.orm import Session

# project
from database import engine, SessionLocal, Base
from models import User as UserModel, Categories as CategoriesModel, Goals as GoalsModel

from schemas import (

    # User
    UserCreate as UserCreateSchema,
    UserResponse as UserResponseSchema,

    # Category
    CategoryCreate as CategoryCreateSchema,
    CategoryResponse as CategoryResponseSchema,

    # Goal
    GoalCreate as GoalCreateSchema,
    GoalResponse as GoalResponseSchema
)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# get requests

@app.get("/users", response_model=List[UserResponseSchema])
def get_users(db: Session = Depends(get_db)) -> List[UserResponseSchema]:
    users = db.query(UserModel).all()
    return users


@app.get("/users/{user_id}", response_model=UserResponseSchema)
def read_user(user_id: int, db: Session = Depends(get_db)) -> UserResponseSchema:
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/categories", response_model=List[CategoryResponseSchema])
def get_categories(db: Session = Depends(get_db)) -> List[CategoryResponseSchema]:
    categories_db = db.query(CategoriesModel).all()
    return categories_db


# post requests

@app.post("/users", response_model=UserResponseSchema)
def create_users(user: UserCreateSchema, db: Session = Depends(get_db)) -> UserResponseSchema:
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/goal", response_model=GoalResponseSchema)
def post_goal(goal: GoalCreateSchema, db: Session = Depends(get_db)):
    db_goal = GoalsModel(**goal.dict())
    user = db.query(UserModel).filter(UserModel.id == db_goal.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


# delete requests

@app.delete("/user/delete/{id}", response_model=UserResponseSchema)
def delete_user(id: int, db: Session = Depends(get_db)) -> UserResponseSchema:
    db_user = db.query(UserModel).filter(UserModel.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()

    return db_user

@app.delete("/goal/delete/{id}", response_model=GoalResponseSchema)
def delete_goal(id: int, db: Session = Depends(get_db)) -> GoalResponseSchema:
    db_goal = db.query(GoalsModel).filter(GoalsModel.id == id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    db.delete(db_goal)
    db.commit()

    return db_goal








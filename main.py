# custom
from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from typing import Optional, List, Dict, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# project
from database import get_db
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

# get requests

@app.get("/users", response_model=List[UserResponseSchema])
async def get_users(
        db: AsyncSession = Depends(get_db)
) -> List[UserResponseSchema]:

    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    return users


@app.get("/users/{user_id}", response_model=UserResponseSchema)
async def read_user(
        user_id: int,
        db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:

    result = await db.execute(
        select(UserModel).where(UserModel.id == user_id)
    )

    db_user = result.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/categories", response_model=List[CategoryResponseSchema])
async def get_categories(
        db: AsyncSession = Depends(get_db)
) -> List[CategoryResponseSchema]:

    result = await db.execute(select(CategoriesModel))
    db_categories = result.scalars().all()
    return db_categories


# post requests

@app.post("/users", response_model=UserResponseSchema)
async def create_users(
        user: UserCreateSchema, db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:
    db_user = UserModel(**user.dict())
    db.add(db_user)
    await db.commit()
    return db_user

@app.post("/goal", response_model=GoalResponseSchema)
async def post_goal(
        goal: GoalCreateSchema, db: AsyncSession = Depends(get_db)
) -> GoalResponseSchema:

    db_goal = GoalsModel(**goal.dict())

    req = await db.execute(
        select(UserModel)
        .where(UserModel.id == db_goal.user_id)
    )
    user = req.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.add(db_goal)
    await db.commit()
    return db_goal


# delete requests

@app.delete("/user/delete/{id}", response_model=UserResponseSchema)
async def delete_user(
        id: int,
        db: AsyncSession = Depends(get_db)
) -> UserResponseSchema:

    req = await db.execute(select(UserModel).where(UserModel.id == id))
    db_user = req.scalar_one_or_none()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(db_user)
    await db.commit()

    return db_user

@app.delete("/goal/delete/{id}", response_model=GoalResponseSchema)
async def delete_goal(
        id: int,
        db: AsyncSession = Depends(get_db)
) -> GoalResponseSchema:

    req = await db.execute(select(GoalsModel).where(GoalsModel.id == id))
    db_goal = req.scalar_one_or_none()

    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    await db.delete(db_goal)
    await db.commit()

    return db_goal
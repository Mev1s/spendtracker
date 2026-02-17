from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from sqlalchemy import func


class UserCreate(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=50)]
    telegram_id: Annotated[int, Field(ge=1)]
    money_per_month: Annotated[Optional[int], Field(default=None)]
    current_balance: Annotated[Optional[int], Field(default=None)]


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True


class Categories(BaseModel):
    hcs: Annotated[int, Field(default=None)]
    food: Annotated[int, Field(default=None)]
    transport: Annotated[int, Field(default=None)]
    pharmacy: Annotated[int, Field(default=None)]
    credits: Annotated[int, Field(default=None)]
    fun: Annotated[int, Field(default=None)]
    cloth: Annotated[int, Field(default=None)]
    financial_cushion: Annotated[int, Field(default=None)]
    target: Annotated[int, Field(default=None)]
    date: Annotated[int, Field(default=func.now())]

class Create_category(BaseModel):
    user_id: int

    class Config:
        from_attributes = True

class Goal(BaseModel):
    user_id: int
    target: Annotated[int, Field(default=None)]
    target_name: Annotated[str, Field(default=None)]
    currency_for_target: Annotated[int, Field(default=None)]
    deadline: Annotated[int, Field(default=None)]

class GoalResponse(Goal):
    id: int

    class Config:
        from_attributes = True



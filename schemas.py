from typing import Optional, Annotated
from pydantic import BaseModel, Field
from sqlalchemy import func
from datetime import date, datetime


class UserBase(BaseModel):
    username: Annotated[str, Field(min_length=1, max_length=50)]
    telegram_id: Annotated[int, Field(ge=1)]
    money_per_month: Annotated[Optional[int], Field(default=None)]
    current_balance: Annotated[Optional[int], Field(default=None)]

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True


class CategoryBase(BaseModel):
    hcs: Annotated[int, Field(default=None)]
    food: Annotated[int, Field(default=None)]
    transport: Annotated[int, Field(default=None)]
    pharmacy: Annotated[int, Field(default=None)]
    credits: Annotated[int, Field(default=None)]
    fun: Annotated[int, Field(default=None)]
    cloth: Annotated[int, Field(default=None)]
    financial_cushion: Annotated[int, Field(default=None)]
    target: Annotated[int, Field(default=None)]
    date: Annotated[datetime, Field(default=func.now())]

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class GoalBase(BaseModel):
    user_id: int
    target: Annotated[int, Field(default=None)]
    target_name: Annotated[str, Field(default=None)]
    currency_for_target: Annotated[int, Field(default=None)]
    deadline: Annotated[date, Field(default=None)]

class GoalCreate(GoalBase):
    pass

class GoalResponse(GoalBase):
    id: int

    class Config:
        from_attributes = True
from datetime import datetime
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Optional
from pydantic.types import conint


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# Pydantic models for requests
class PostBase(BaseModel):
    """Base Model for Post"""
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# Pydantic models for responses
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    class Config:
        from_attributes = True


class PostVotesResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        from_attributes = True


# Users Schemas
class UserCreate(BaseModel):
    email: EmailStr # validate email address
    password: str


# Auth Schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None # datatype str throws an error


class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)
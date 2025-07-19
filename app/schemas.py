from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    name: str = Field(..., max_length=24)
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_minimum_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


    


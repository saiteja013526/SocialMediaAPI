from datetime import datetime
from pydantic import BaseModel, EmailStr



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
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
    


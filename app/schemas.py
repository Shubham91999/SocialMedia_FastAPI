from datetime import datetime
from pydantic import BaseModel, EmailStr


# Defined Pydantic model to validate the input schema from frontend
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True

# Used to validate request body before User Creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# Used for sending reponse after User Creations
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
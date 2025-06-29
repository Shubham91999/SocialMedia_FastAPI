from datetime import datetime
from pydantic import BaseModel


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


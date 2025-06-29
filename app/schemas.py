from pydantic import BaseModel


# Defined Pydantic model to validate the input schema from frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
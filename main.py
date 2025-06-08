from fastapi import Body, FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Defined Pydantic model to validate the input schema from frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"Post1": "Data for Post1", "Post2": "Data for Post2"}

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"NewPost": f"Title: {payload['title']} Content: {payload['content']}"} 

@app.post("/createpost")
def create_post(post: Post):
    print(post)  # printing data in BaseModel format
    print(post.model_dump())  # dict() method is deprecated, so using model_dump() -> printing result in form of dictionary
    return {"data": post}



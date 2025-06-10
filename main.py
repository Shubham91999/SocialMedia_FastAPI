from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# Defined Pydantic model to validate the input schema from frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"id": 1, "title": "My favorite Car", "content": "I like BMW"}, {"id": 2, "title": "My favorite food", "content": "I like Pizza"}]

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"NewPost": f"Title: {payload['title']} Content: {payload['content']}"} 

# @app.post("/posts")
# def create_post(post: Post):
#     print(post)  # printing data in BaseModel format
#     print(post.model_dump())  # dict() method is deprecated, so using model_dump() -> printing result in form of dictionary
#     return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# {id} is a path parameter 
@app.get("/posts/{id}")
def get_post(id: int, respone: Response):
    # print(id)
    post = find_post(id)
    if not post:
        # respone.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with id {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    return {"post_detail": post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    my_posts.pop(index)
    return {"Message": f"Post {id} was deleted successfully."}




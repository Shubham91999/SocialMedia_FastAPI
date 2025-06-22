from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from dotenv import load_dotenv
import os
# Importing because psycopg2 alone doesn't return column names
from psycopg2.extras import RealDictCursor
import time


# Application instance used while starting dev server
app = FastAPI()

# Defined Pydantic model to validate the input schema from frontend
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='SocialMedia_FastAPI', user=DB_USER, password=DB_PASSWORD, cursor_factory=RealDictCursor)

        cursor = conn.cursor()
        print("Database Connection is successful")
        break
    except Exception as e:
        print("DB connection failed")
        print(e)
        print("Trying again in 2 seconds.")
        time.sleep(2)


my_posts = [{"id": 1, "title": "My favorite Car", "content": "I like BMW"}, {"id": 2, "title": "My favorite food", "content": "I like Pizza"}]

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

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
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)

    cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    post_dict = cursor.fetchone()
    conn.commit()
    return {"data": post_dict}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

# {id} is a path parameter 
@app.get("/posts/{id}")
def get_post(id: int):
    # print(id)
    cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # Adding , to make input as tuple, second argument in execute should be a tuple not string
    post = cursor.fetchone()
    # post = find_post(id)
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
    # index = find_index_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id,)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    # my_posts.pop(index)
    return {"Message": f"Post {id} was deleted successfully."}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    return {"data": updated_post}




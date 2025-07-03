from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from ..schemas import PostCreate, Post
from ..database import get_db
from .. import models
from fastapi import status, HTTPException

router = APIRouter(
    prefix="/users"
)


@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(posts)
    posts = db.query(models.Post).all()

    return posts

# Testing models.py
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}

# @app.post("/createpost")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"NewPost": f"Title: {payload['title']} Content: {payload['content']}"} 

# @app.post("/posts")
# def create_post(post: Post):
#     print(post)  # printing data in BaseModel format
#     print(post.model_dump())  # dict() method is deprecated, so using model_dump() -> printing result in form of dictionary
#     return {"data": post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10000000)
    # my_posts.append(post_dict)

    # cursor.execute("""INSERT INTO posts(title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # post_dict = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title,  # type: ignore
    #                        content=post.content,  # type: ignore
    #                        published=post.published) # type: ignore

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# {id} is a path parameter 
@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # print(id)
    # cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id),)) # Adding , to make input as tuple, second argument in execute should be a tuple not string
    # post = cursor.fetchone()
    # post = find_post(id)

    post = db.query(models.Post).filter(models.Post.id == id).first() # type: ignore # Instead of all(), first() is used for resource optimization
    print(post)

    if not post:
        # respone.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": f"Post with id {id} not found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id,)))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post = db.query(models.Post).filter(models.Post.id == id) # type: ignore

    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    return {"Message": f"Post {id} was deleted successfully."}


@router.put("/{id}", response_model=Post)
def update_post(id: int, post: PostCreate, db: Session = Depends(get_db)):
    # index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    updated_post = db.query(models.Post).filter(models.Post.id == id) # type: ignore

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()

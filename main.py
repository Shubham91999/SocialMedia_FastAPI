from fastapi import Body, FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    return {"Post1": "Data for Post1", "Post2": "Data for Post2"}

@app.post("/createpost")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"NewPost": f"Title: {payload['title']} Content: {payload['content']}"} 


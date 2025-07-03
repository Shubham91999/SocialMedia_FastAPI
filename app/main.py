from fastapi import Body, FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from dotenv import load_dotenv
import os
# Importing because psycopg2 alone doesn't return column names
from psycopg2.extras import RealDictCursor
import time
from .schemas import PostCreate, Post, UserCreate, UserOut
from . import models, schemas, utils

# Importing models and engine for db connectivity
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

from .routers import post, user, auth

# Importing models to create db tables
models.Base.metadata.create_all(bind=engine) # type: ignore

# Application instance used while starting dev server
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='SocialMedia_FastAPI', user=DB_USER, password=DB_PASSWORD, cursor_factory=RealDictCursor)

#         cursor = conn.cursor()
#         print("Database Connection is successful")
#         break
#     except Exception as e:
#         print("DB connection failed")
#         print(e)
#         print("Trying again in 2 seconds.")
#         time.sleep(2)













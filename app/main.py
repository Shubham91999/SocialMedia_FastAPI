from fastapi import FastAPI
from dotenv import load_dotenv
import os
from . import models
# Importing models and engine for db connectivity
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote

# Importing models to create db tables
models.Base.metadata.create_all(bind=engine) # type: ignore

# Application instance used while starting dev server
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)





# *********************************
"""
from pydantic import BaseModel
from typing import Optional, List
import psycopg2
from sqlalchemy.orm import Session
from fastapi import Depends
from random import randrange
from . import schemas, utils

# Importing because psycopg2 alone doesn't return column names
from psycopg2.extras import RealDictCursor
import time
from .schemas import PostCreate, Post, UserCreate, UserOut

from fastapi import Response, status, HTTPException, Body
"""
# *********************************

# load_dotenv()
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

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














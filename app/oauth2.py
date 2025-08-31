from jose import JWTError, jwt
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database
from sqlalchemy.orm import Session 
from . import models
from .config import settings

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


# Functon to create JWT Token upon User Authentication
def create_access_token(data: dict):
    to_encode = data.copy()
    # Setting the expiration timer
    expire = datetime.now(timezone.utc) + timedelta(minutes=float(ACCESS_TOKEN_EXPIRE_MINUTES or 30))
    # Adding expire to to_encode dictionary
    to_encode.update({"exp": expire})

    # Encode method takes payload, secret key and signature algorithm to create a encoded jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    # Returning the token
    return encoded_jwt

# Function to verify the access sent by user with every API request
def verify_access_token(token: str, credentials_exception):
    try:
        print(token)
        # In oauth2.py - add this debug
        # print(f"SECRET_KEY loaded: {SECRET_KEY}")
        if not SECRET_KEY:
            raise ValueError("SECRET_KEY environment variable not set")
        
        # Decode function takes token, secret key and algorithm to decode and give back the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        print(payload)
        
        # Accessing only User ID
        id = payload.get("user_id")
        # print(id)
        # If null return exception
        if id is None:
            raise credentials_exception
        # Validating token data with Tokendata Schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    return token_data
    
# This will be passed as dependency in every API route to authenticate user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"www-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token_data.id).first()  # type: ignore

    return user
        


    
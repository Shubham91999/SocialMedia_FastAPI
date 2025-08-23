from jose import JWTError, jwt
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

#SECRET_KEY
#Algorithm
#Expiration_Time
load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Functon to create JWT Token upon User Authentication
def create_access_token(data: dict):
    to_encode = data.copy()
    # Setting the expiration timer
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Adding expire to to_encode dictionary
    to_encode.update({"exp": expire})

    # Encode method takes payload, secret key and signature algorithm to create a encoded jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    # Returning the token
    return encoded_jwt

# Function to verify the access sent by user with every API request
def verify_access_token(token: str, credentials_exception):
    try:
        # Decode function takes token, secret key and algorithm to decode and give back the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) # type: ignore
        
        # Accessing only User ID
        id = payload.get("user_id")

        # If null return exception
        if id is None:
            raise credentials_exception
        # Validating token data with Tokendata Schema
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
# This will be passed as dependency in every API route to authenticate user
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"www-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
        


    
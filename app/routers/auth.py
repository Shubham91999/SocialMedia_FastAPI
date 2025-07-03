from fastapi import APIRouter, Depends, status, HTTPException, Response
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, utils



router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user_creds: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_creds.email).first() # type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    

    return {"token": "Login Successful"}

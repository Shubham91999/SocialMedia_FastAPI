from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2


router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    print(current_user.id)

    # Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() # type: ignore

    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id: {vote.post_id} does not exist")
    
    # Check if user already voted
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) # type: ignore

    found_vote = vote_query.first()

    if (vote.dir == 1):  # Add vote
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Vote added successfully"}

    else:  # Remove vote (dir = 0)
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Vote deleted successfully"}


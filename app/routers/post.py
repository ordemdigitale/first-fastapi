from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, aliased
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


#@router.get("/", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostVotesResponse])
#@router.get("/")
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 5,
              skip: int = 0,
              search: Optional[str] = ""):
#    cursor.execute("""SELECT * FROM posts""") # old way using sql query in the code
#    posts = cursor.fetchall()
    # 
#    posts = db.query(models.Posts).filter(
#        models.Posts.title.contains(search)
#    ).limit(limit).offset(skip).all()

    posts = db.query(
        models.Posts, func.count(models.Votes.post_id).label("votes")
    ).outerjoin(
        models.Votes, models.Posts.id == models.Votes.post_id
    ).group_by(models.Posts.id).filter(
        models.Posts.title.contains(search)
    ).limit(limit).offset(skip).all()

    # Modify the results to match the response model
    post_votes_response = [schemas.PostVotesResponse(Post=schemas.PostResponse(
        id=post.id, title=post.title, content=post.content, created_at=post.created_at, user_id=post.user.id, user=schemas.UserResponse(
            id=post.user.id, email=post.user.email, created_at=post.user.created_at
        )
    ), votes=votes) for post, votes in posts]
    return post_votes_response


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Posts(user_id=current_user.id, **post.model_dump()) # add current_user.id to new_post
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostVotesResponse)
def get_post(id: int, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    #post = db.query(models.Posts).filter(models.Posts.id == id).first()

    post = db.query(
        models.Posts, func.count(models.Votes.post_id).label("votes")
    ).outerjoin(
        models.Votes, models.Posts.id == models.Votes.post_id
    ).group_by(models.Posts.id).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    # Build the response using the post object directly
    post_votes_response = schemas.PostVotesResponse(Post=schemas.PostResponse(
        id=post.Posts.id,title=post.Posts.title,
        content=post.Posts.content,created_at=post.Posts.created_at,
        user_id=post.Posts.user.id,user=schemas.UserResponse(
            id=post.Posts.user.id,email=post.Posts.user.email,created_at=post.Posts.user.created_at
        )
    ), votes=post.votes)

    return post_votes_response


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform this action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


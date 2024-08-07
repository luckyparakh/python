from fastapi import HTTPException, Depends, status, APIRouter
from .. import models, schemas, outh2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    records = db.query(models.Posts).all()
    return records  # FastAPI will automatically convert this to JSON


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db), user: models.Users = Depends(outh2.get_current_user)):
    print(user.id)
    # new_post = models.Posts(title=payload.title, content=payload.content,published=payload.publish)
    new_post = models.Posts(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user: models.Users = Depends(outh2.get_current_user)):

    # cursor.execute(
    #     "DELETE FROM posts WHERE id = %s returning *", (str(post_id),))
    # del_post = cursor.fetchone()
    del_q = db.query(models.Posts).filter(models.Posts.id == post_id)
    if not del_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {post_id} not found")
    del_q.delete(synchronize_session=False)
    db.commit()
    return


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), user: models.Users = Depends(outh2.get_current_user)):
    # cursor.execute("Update posts SET title = %s, content = %s, published = %s WHERE id = %s returning *",
    #                (post.title, post.content, post.publish, id))
    # post_to_update = cursor.fetchone()
    up_q = db.query(models.Posts).filter(models.Posts.id == id)
    if not up_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    up_q.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return up_q.first()

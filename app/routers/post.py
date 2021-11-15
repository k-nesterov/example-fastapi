from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func  # give us access to functions like COUNT(*)
from ..database import engine, get_db
from typing import List, Optional

router = APIRouter(
    prefix='/posts',  # to do not put full path in each route
    tags=['Posts']
)

# return not a single Post, but List[schemas.Post]


# return not single, but List of Post
# @router.get('/', response_model=List[schemas.Post])
@router.get('/', response_model=List[schemas.PostOut])
# @router.get('/')
# connect to DB and check current user with 'get_current_user' function
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: Optional[str] = ""):  # this is query parameters http://www.ru/?limit=1&skip=2&search=word
    # if all checks is OK, so token is valid, and current_user is SQLAlchemy user with all of its fields
    # cursor.execute("""SELECT * FROM posts""") #commented
    # posts = cursor.fetchall() #commented
    #posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(
    #    models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(results)
    # return posts
    return results


# if created send 201 http code
# with response change model
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# here is some steps: 1 - validate POST data, 2 - connect to DB, 3 - check user JWT token is OK
# 1) validate POST request, that all required fields are exist (schemas.PostCreate)
# 2) create session with DB (db: Session = Depends(get_db)), because we do not put our session, so we use
# Session = Depends(get_db) which we put into DB variable
# 3) next we check current user. Can he post or not? We call current_user: int = Depends(oauth2.get_current_user))
# in variable CURRENT_USER we put result of running oauth2.get_current_user function in oauth2.py file.
# This function returning CURRENT_USER with all fields
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # #post_dict = post.dict()
    # #post_dict['id'] = randrange(0, 1000000)
    # # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(**post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # validate with SQLAlchemy is all required fields are exist
    # add owner_id from CURRENT_USER var
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)  # add new post to database
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  # auto convert to int
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),)) # add comma in str(id), ,because  it will fail
    #post = cursor.fetchone()

    #post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")


    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not enough rights")
    return post
# def create_post(payLoad: dict = Body(...)):
#    print(payLoad)
#    return {"new_post": f"title {payLoad['title']} content {payLoad['content']}"}
# new_post reference Post Pydantic Model. So this function calls by decorator and wait for Post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    #deleted_post = cursor.fetchone()
    # conn.commit()
    # find index in array for item by id
    #index = find_index_post(id)
    # if deleted_post == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f"post with id {id} does not exist")
    # if index == None:

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Not enough rights")
    post_query.delete(synchronize_session=False)
    db.commit()
    # remove from array
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *",
    #               (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #index = find_index_post(id)
    # if index == None:
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not enough rights")
    # post_query.update({'title': "updated_title",
    #                  "content": "updated_content"}, synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    #post_dict = post.dict()
    # because we are giving id in url then put it into dict
    #post_dict["id"] = id
    # my_posts[index] = post_dict  # find post by index in array and replace it
    return post_query.first()

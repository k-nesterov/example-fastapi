from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True  # if user dont give value ==> True
#     # rating: Optional[int] = None  # fully optional field with def.value None

class UserCreate(BaseModel):
    email: EmailStr  # validate email
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr  # validate email
    created_at: datetime
    # allow parse sqlalchemy object to dict

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

# class to show only specific fields, we can send only ID, or ID+content etc...


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    # allow parse sqlalchemy object to dict
    owner: UserOut
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post #this will expect all fields in class Post(PostBase):
    votes: int
    
    class Config:
        orm_mode = True
    # {
    #     "Post": {
    #         "title": "new_title3",
    #         "content": "new_title3",
    #         "published": true,
    #         "id": 6,
    #         "created_at": "2021-11-10T23:04:47.313834+03:00",
    #         "owner_id": 16,
    #         "owner": {
    #             "id": 16,
    #             "email": "abcdefg@gmail.com",
    #             "created_at": "2021-11-08T11:53:54.448650+03:00"
    #         }
    #     },
    #     "votes": 0
    # },
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)  # allow only <= 1


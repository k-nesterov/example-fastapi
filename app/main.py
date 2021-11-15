from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)  # we call models file to create all tables on startup
# but with alembec we do not need it anymore
# There is default Base class. We create tables



app = FastAPI()

origins = ["*"] # list of domains allowed to make request to API
# for example https://www.google.com , https://www.youtube.com

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
async def root():
    return {"message": "Hello world!"}

# my_posts = [
#     {"title": "title1", "content": "content1", "id": 1},
#     {"title": "title2", "content": "content2", "id": 2}
# ]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#     return None
# class Post which extend BaseModel


# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

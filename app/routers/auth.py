from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
#from ..database import get_db
from .. import database, schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token) # response with Pydantic validation schemas.Token
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # validate post data with OAuth2PasswordRequestForm. It has username= & password=
    # its not raw request, its form-data request
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first() # trying to find user
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ivalid credentials")

    # trying to compare hashed DB password with password from POST
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ivalid credentials")
    
    # if password is OK, so create access_token with 'user_id' value
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    # return JSON with access_token and token_type. This will be validated next by response_model=schemas.Token
    return {"access_token": access_token, "token_type": "bearer"}

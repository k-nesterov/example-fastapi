from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

# declares that the URL /login will be the
# one that the client should use to get the token.
# That information is used in OpenAPI, and then in the interactive API documentation systems.
# The oauth2_scheme variable is an instance of OAuth2PasswordBearer, but it is also a "callable".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# set options
SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

# create Oauth2 token


def create_access_token(data: dict):  # get {"user_id": "13"} dict
    to_encode = data.copy()  # copy original data to manipulate with it next

    # set expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # its linux time
    # add this key+value into our 'to_encode' dict, if value already exist - replace
    to_encode.update({"exp": expire})

    # encode with secret
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt  # return encoded token


def verify_access_token(token: str, credentials_exception): # we get token and custom exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM])  # decode JWT

        # get from payload user_id and store it in variable ID with type STR
        id: str = payload.get("user_id")  # extract ID

        if id is None:
            raise credentials_exception  # no ID = send error
        # validate id with schema (its just ID in it, can be skipped)
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data  # return token ID, example 'id=14'


# FastAPI know its Oauth2 and check it
# It will go and look in the request for that Authorization header, 
# check if the value is Bearer plus some token, and will return the token as a str.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    # we can call this func to check auth data in our selected paths
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Can not validate credentials", headers={"WWW-Authentication": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(
        models.User.id == token.id).first()  # get user
    return user  # return user information with all fields, like email
    # return verify_access_token(token, credentials_exception)

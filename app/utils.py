from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # set hashing algorithm to bcrypt for passlib

# convert normal password to hashed password
def hash(password: str):
    return pwd_context.hash(password)

# compare hashed and normal password
def verify (plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
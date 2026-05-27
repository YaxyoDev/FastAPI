from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from typing import Annotated
from starlette import status
from jose import jwt, JWTError
from datetime import timedelta, datetime

from database import SessionLocal
from models import User, Todos

###################################################################
#                           CONFIG  
###################################################################

SECRET_KEY = 'd8c1c23b7950f6211e890ba4e9bf5638300d2a7a2975e3c9b7d71b932d4595fc'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

###################################################################
#                           FUNCTIONS  
###################################################################

# 1) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2) 
def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
        
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    
    return user

# 3) 
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)    

# 4) 
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
        
        return {'username': username, 'user_id': user_id, 'role': role}
        
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

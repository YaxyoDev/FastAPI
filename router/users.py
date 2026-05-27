from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette import status

from models import User
from .forms import Password
from config import user_dependency, db_dependency
from functions import bcrypt_context


user_router = APIRouter(
    prefix='/users',
    tags=['users']
)

###################################################################
#                           USERS
###################################################################

# Get User
@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authencation Failed!")

    return db.query(User).filter(User.id == user.get('user_id')).first()

# Change Password
@user_router.put('/change_password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, request: Password):
    if user is None:
        raise HTTPException(status_code=401, detail="Authencation Failed!")
    
    db_user = db.query(User).filter(User.id == user.get('user_id')).first()
    
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found')
    
    if not bcrypt_context.verify(request.current_password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Password is incorrect!')
    
    db_user.hashed_password = bcrypt_context.hash(request.new_password)
    db.commit()

# Upgrade account

@user_router.put('/phonenumber/{phone_number}/', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    
    if user is None:
        raise HTTPException(status_code=401, detail="AUthencation failed")
    
    user_model = db.query(User).filter(User.id == user.get("user_id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()


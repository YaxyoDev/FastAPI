from fastapi import Depends, APIRouter, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi.templating import Jinja2Templates

from starlette import status

from datetime import timedelta
from models import User

from config import user_dependency, db_dependency
from functions import bcrypt_context, authenticate_user, create_access_token
from .forms import *

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

templates = Jinja2Templates(directory='templates')

####################################################################
#                           PAGES
####################################################################

@auth_router.get('/login-page')
def render_login_page(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

@auth_router.get('/register-page')
def render_register_page(request: Request):
    return templates.TemplateResponse(request=request, name='register.html')

####################################################################
#                           AUTHENCATION
####################################################################

# Create User
@auth_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, request: CreateUserRequest):
    new_user =  User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        role=request.role,
        hashed_password=bcrypt_context.hash(request.password),
        is_active=True,
        phone_number=request.phone_number
    )
    db.add(new_user)
    db.commit()
    
    return new_user

# Access Token
@auth_router.post('/token', response_model=Token)
async def login_for_acceess_token(form: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                  db: db_dependency):
    user = authenticate_user(form.username, form.password, db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {
        'access_token': token, 
        'token_type': 'bearer'
    }


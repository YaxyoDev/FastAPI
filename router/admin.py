from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated

from functions import get_current_user
from models import Todos, User

admin_router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@admin_router.get('/todos', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authencation failed!')
    
    return db.query(Todos).all()

@admin_router.delete('/delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def read_all(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authencation failed!')
    
    deleted = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if deleted is None:
        raise HTTPException(status_code=404, detail='Todo not found!')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return {deleted.title: 'deleted'}

@admin_router.get('/users', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authencation failed!')
    
    return db.query(User).all()

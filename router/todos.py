from fastapi import APIRouter, HTTPException, Path, Request
from starlette import status

from models import Todos

from config import user_dependency, db_dependency
from .forms import TodosRequest
from functions import get_current_user

todos_router = APIRouter(
    prefix='/todos',
    tags=['/todos']
)
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

def redirect_to_login():
    redirect_response = RedirectResponse('/auth/login-page', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

####################################################################
#                           PAGES   
####################################################################

@todos_router.get('/todo-page')
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        
        if user is None:
            return redirect_to_login()
        
        todos = db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
        
        return templates.TemplateResponse(request=request, name='todo.html', context={'todos': todos, 'user': user})

    except:
        return redirect_to_login()

@todos_router.get('/add-todo-page')
async def render_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))    
        
        if user is None:
            return redirect_to_login()
        
        return templates.TemplateResponse(request=request, name='add-todo.html', context={'user': user})
    
    except:
        return redirect_to_login()
    
@todos_router.get('/edit-todo-page/{todo_id}')
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))    
        
        if user is None:
            return redirect_to_login()
        
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        
        
        return templates.TemplateResponse(request=request, name='edit-todo.html', context={'user': user, 'todo': todo})
    
    except:
        return redirect_to_login()
         
####################################################################
#                           TODOS
####################################################################

# get
@todos_router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()

@todos_router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def read_one(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    selected = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if selected:
        return selected
    raise HTTPException(status_code=404, detail="Todo not found!")

#----------------------------------------------------------------------------

# create
@todos_router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, request: TodosRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    model = Todos(**request.model_dump(), owner_id=user.get('user_id'))
    
    db.add(model)
    db.commit()
  
#----------------------------------------------------------------------------

# update  
@todos_router.put('/update/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, request: TodosRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if not model:
        raise HTTPException(status_code=404, detail='Todo Not Found!')
    
    model.title = request.title
    model.description = request.description
    model.priority = request.priority
    model.complete = request.complete
    
    db.add(model)
    db.commit()

#----------------------------------------------------------------------------

# delete
@todos_router.delete('/delete/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if not model:
        raise HTTPException(status_code=404, detail='Todo Not Found!')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()



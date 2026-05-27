from fastapi import FastAPI, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from router import auth_router, todos_router, admin_router, user_router
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

@app.get('/')
def test(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)

@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}

app.include_router(auth_router)
app.include_router(todos_router)
app.include_router(admin_router)
app.include_router(user_router)
# app.include_router()
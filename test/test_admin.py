from .utils import *
from router.admin import get_db
from functions import get_current_user
from fastapi import status
from models import Todos

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "title": "Doing",
            "description": "Doing something",
            "priority": 3,
            'complete': True,
            "owner_id": 1
        }
    ]    

def test_admin_delete_todo(test_todo):
    response = client.delete('admin/delete/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    
def test_admin_delete_todo_not_found(test_todo):
    response = client.delete('admin/delete/1234') 
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found!"}  
    

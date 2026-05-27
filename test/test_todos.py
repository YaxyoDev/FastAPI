from main import app             
from functions import get_db, get_current_user 
from fastapi import status
from models import Todos

from .utils import *
     
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



###############################################################
#                   TEST READ
###############################################################
 

def test_read_all_authenticated(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1,
                                "title": "Doing",
                                "description": "Doing something",
                                "priority": 3,
                                'complete': True,
                                "owner_id": 1}]
    
def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1,
                                "title": "Doing",
                                "description": "Doing something",
                                "priority": 3,
                                'complete': True,
                                "owner_id": 1}
    
def test_read_one_not_found():
    response = client.get('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found!"}

###############################################################
#                   TEST CREATE
###############################################################
 

def test_create_todo(test_todo):
    request_data = {"title": "playing",
                                "description": "Playing cs 1.6",
                                "priority": 2,
                                'complete': False}
    response = client.post('/todos/create', json=request_data)
    assert response.status_code == 201
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data['title']
    assert model.description == request_data['description']
    assert model.priority == request_data['priority']
    assert model.complete == request_data['complete']

###############################################################
#                   TEST UPDATE
###############################################################

def test_update_todo(test_todo):
    request = {
        'title': 'Cooking',
        'description': 'Cooking Palov',
        'priority': 5,
        'complete': True
    }
    
    response = client.put('/todos/update/1', json=request)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'Cooking'
    
def test_update_todo_not_found(test_todo):
    request = {
        'title': 'Cooking',
        'description': 'Cooking Palov',
        'priority': 5,
        'complete': True
    }
    
    response = client.put('/todos/update/999', json=request)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo Not Found!'}
    
###############################################################
#                   TEST DELETE
###############################################################
    
def test_delete_todo(test_todo):
    response = client.delete('/todos/delete/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
    
def test_delete_todo_not_found(test_todo):
    response = client.delete('/todos/delete/1999')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo Not Found!'}


from .utils import *
from functions import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'yaxyo'
    assert response.json()['email'] == 'yaxyo@gmail.com'
    assert response.json()['first_name'] == 'Yaxyo'
    assert response.json()['last_name'] == 'Bek'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '+998942140551'


def test_change_password_success(test_user):
    response = client.put("/users/change_password", json={"current_password": "qwerty1234",
                                                  "new_password": "177oo817"})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_current_password(test_user):
    response = client.put("/users/change_password", json={"current_password": "hgyufrsgydrgd",
                                                  "new_password": "177oo817"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Password is incorrect!'}


def test_change_phone_number_success(test_user):
    response = client.put("/users/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT







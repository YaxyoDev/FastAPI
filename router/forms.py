from pydantic import BaseModel, Field

# 1)
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

# 2)
class Token(BaseModel):
    access_token: str
    token_type: str

# 3) 
class TodosRequest(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool 
    
# 4)

class Password(BaseModel):
    current_password: str
    new_password: str
from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session

from functions import get_current_user, get_db

# 1) 
db_dependency = Annotated[Session, Depends(get_db)]

# 2) 
user_dependency = Annotated[dict, Depends(get_current_user)]

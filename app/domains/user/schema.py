from pydantic import BaseModel
from typing import Optional, List

from app.core.config import settings

class UserBase(BaseModel):
    
    user_id: int
    user_project: List = []


"""
이거 보고 도입하기: https://wikidocs.net/295889
"""
from pydantic import BaseModel
from typing import Optional, List

from app.core.config import settings


class ProjectBase(BaseModel):

    user_id: int
    project_id: str

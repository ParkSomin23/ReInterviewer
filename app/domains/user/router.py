import os
import subprocess
import json

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

from sqlalchemy.orm import Session

import app.domains.user.service as user_service
from app.domains.user.schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    UserSearchRequest,
)

from app.core.config import settings
from app.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/add_user", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):

    return user_service.create_user(db, user_in)


@router.get("/find", response_model=UserResponse)
def find_user(email: str, db: Session = Depends(get_db)):
    return user_service.find_user(db, email)

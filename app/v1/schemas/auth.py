from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

class UserOut(BaseModel):
    uid: uuid.UUID
    email: EmailStr
    created_at: datetime

    model_config = {
        'from_attributes': True
    }

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

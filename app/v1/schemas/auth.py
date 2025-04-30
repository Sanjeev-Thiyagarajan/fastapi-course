from pydantic import BaseModel, EmailStr, Field
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
    email: EmailStr = Field(max_length=50)
    password: str = Field(max_length=50)


class UserLogin(BaseModel):
    email: EmailStr
    password: str

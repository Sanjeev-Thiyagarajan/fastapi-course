from pydantic import BaseModel
from datetime import datetime
import uuid



class PostBase(BaseModel):
    title: str
    content: str
    published_date: datetime 
    


class PostCreate(PostBase):
    pass


class PostOut(BaseModel):
    uid: uuid.UUID
    title: str
    content:str
    published_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

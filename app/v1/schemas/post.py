from pydantic import BaseModel
from datetime import datetime
import uuid
from app.v1.schemas.vote import VoteRead
from typing import Optional,List

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


class PostWithVote(BaseModel):
    post: PostOut
    vote: Optional[VoteRead]
    
class PostRead(BaseModel):
    uid: uuid.UUID
    title: str
    content: str
    votes: List[VoteRead] = []
    
    class Config:
        from_attributes = True
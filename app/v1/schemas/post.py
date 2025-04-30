from pydantic import BaseModel
from datetime import datetime
import uuid


class PostBase(BaseModel):
    title: str
    content: str
    published_date: bool = True
    


class PostCreate(PostBase):
    pass


class Post(PostBase):
    uid: uuid.UUID
    created_at: datetime
    owner_id: int

    model_config = {
        'from_attributes': True
    }
    
class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = {
        'from_attributes': True
    }

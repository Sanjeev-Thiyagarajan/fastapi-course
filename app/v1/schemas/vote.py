from pydantic import BaseModel
from pydantic.types import conint
import uuid
from typing import Optional

class VoteRead(BaseModel):
    uid: uuid.UUID
    user_uid: Optional[uuid.UUID]
    post_uid: Optional[uuid.UUID]
    
    class Config:
        from_attributes = True

class VoteModel(BaseModel):
    post_uid: uuid.UUID
    dir: conint(le=1)

class VoteCreate(BaseModel):
    # post_uid: uuid.UUID
    dir: conint(le=1)

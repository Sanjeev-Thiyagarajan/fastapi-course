from pydantic import BaseModel
from pydantic.types import conint
import uuid


class VoteModel(BaseModel):
    post_uid: uuid.UUID
    dir: conint(le=1)

class VoteCreate(BaseModel):
    # post_uid: uuid.UUID
    dir: conint(le=1)

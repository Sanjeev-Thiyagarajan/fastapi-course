from sqlmodel import SQLModel, Field,Column,Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional,List



class Post(SQLModel, table=True):
    __tablename__ = "posts"
    
    uid : uuid.UUID= Field(sa_column=Column(pg.UUID, primary_key=True, unique=True,nullable=False,default=uuid.uuid4))
    title: str
    content: str
    published_date: str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    user_uid: Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")
    
    
    owner : Optional["User"] = Relationship(back_populates="posts")
    
    def __repr__(self) -> str:
        return f"<Post {self.title}"



class User(SQLModel, table=True):
    __tablename__ = "users"
    
    uid:uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True,nullable=False,default=uuid.uuid4))
    email: str
    password_hash : str
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    
    posts: List["Post"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy":"selectin"})
    
    
    def __repr__(self) -> str:
        return f"<User {self.email}"


class Vote(SQLModel,table=True):
    __tablename__ = "votes"
    
    uid : uuid.UUID = Field(sa_column=Column(pg.UUID, primary_key=True, unique=True,nullable=False,default=uuid.uuid4))
    user_uid: Optional[uuid.UUID] = Field(default=None,foreign_key="users.uid")
    post_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="posts.uid")
    
    














# class Post(Base):
#     __tablename__ = "posts"

#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, server_default='TRUE', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text('now()'))
#     owner_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), nullable=False)

#     owner = relationship("User")


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True),
#                         nullable=False, server_default=text('now()'))


# class Vote(Base):
#     __tablename__ = "votes"
#     user_id = Column(Integer, ForeignKey(
#         "users.id", ondelete="CASCADE"), primary_key=True)
#     post_id = Column(Integer, ForeignKey(
#         "posts.id", ondelete="CASCADE"), primary_key=True)

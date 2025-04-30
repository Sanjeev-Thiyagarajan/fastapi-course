from sqlalchemy.ext.asyncio.session import AsyncSession
from app.v1.models.models import Post
from sqlmodel import select,desc
from app.v1.schemas.post import PostCreate


class PostService:
    async def get_all_posts(self,session:AsyncSession):
        statement = select(Post).order_by(desc(Post.created_at))
        
        result = await session.execute(statement)
        
        posts = result.all()
        
        return posts
    
    async def get_user_posts(self,user_uid:str,session:AsyncSession):
        
        statement = select(Post).where(Post.user_uid == user_uid)
        
        result = await session.execute(statement)
        
        user_posts = result.all()
        
        return user_posts
    
    
    async def create_new_posts(self,post_data:PostCreate,session:AsyncSession):
        
        pass
        
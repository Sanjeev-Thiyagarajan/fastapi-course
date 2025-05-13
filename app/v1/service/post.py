from sqlmodel.ext.asyncio.session import AsyncSession
from app.v1.models.models import Post,Vote
from fastapi import HTTPException,status
from sqlmodel import select,desc
from app.v1.schemas.post import PostCreate, PostOut,VoteRead
from datetime import datetime
from sqlalchemy.orm import selectinload
from app.utils.errors import PostNotFound

class PostService:
    async def get_all_posts(self,session:AsyncSession):
        statement = select(Post).order_by(desc(Post.created_at))
        
        result = await session.exec(statement)
        
        posts = result.all()
        
        return posts
    
    async def get_user_post(self,user_uid:str,session:AsyncSession):
        # statement = select(Post).where(Post.user_uid == user_uid).order_by(desc(Post.created_at))
        
        statement = select(Post,Vote).join(Vote, Post.uid == Vote.post_uid, isouter=True).where(Post.user_uid == user_uid).order_by(desc(Post.created_at))
        
        result = await session.exec(statement=statement)
        
        rows = result.all()
        print(f"Rows response is",rows)

        
        response = [
            {
                "post":PostOut.model_validate(post),
                "vote": VoteRead.model_validate(vote) if vote else None
            }
            
            for post,vote in rows
        ]
        
        print(f"Response is",response)
        return response
    
    
    async def get_posts_by_id(self,post_uid:str,session:AsyncSession):
        
        statement = select(Post).where(Post.uid == post_uid)
        
        result = await session.exec(statement)
        
        user_posts = result.first()
        
        
        return user_posts if user_posts is not None else None
    
    
    async def create_new_posts(self,user_uid: str, post_data:PostCreate,session:AsyncSession):
        
        new_post_data = post_data.model_dump()
        
        new_post = Post(**new_post_data)
        
        new_post.published_date = new_post_data["published_date"]
                
        new_post.user_uid = user_uid
        
        session.add(new_post)
        
        await session.commit()
        
        return new_post
    
    
    async def update_post(self,post_uid:str, post_update_data:PostCreate,session:AsyncSession):
        post = await self.get_posts_by_id(post_uid,session)
        
        if post:
            post_dict = post_update_data.model_dump()
            
            for k,v in post_dict.items():
                setattr(post,k,v)
                
            await session.commit()
            
            return post
        raise PostNotFound()
    
    
    async def delete_post(self,post_uid:str, session:AsyncSession):
        post = await self.get_posts_by_id(post_uid,session)
        
        if post:
            await session.delete(post)
            
            await session.commit()
            
            return {}
        
        else:
            return None
            
            

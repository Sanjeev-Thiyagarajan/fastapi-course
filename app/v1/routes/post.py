from fastapi import status, HTTPException, Depends, APIRouter
from typing import List
from app.db.database import get_session
from app.v1.schemas.post import PostCreate, PostOut
from app.v1.service.post import PostService
from app.db.database import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession

post_router = APIRouter()
post_service = PostService()



# Get all post
@post_router.get("/", status_code=status.HTTP_200_OK,response_model=List[PostOut])
async def get_all_posts(session: AsyncSession = Depends(get_session)):
    user_posts = await post_service.get_all_posts(session)
    
    return user_posts


@post_router.post("/", response_model=PostOut)
async def create_post(post_data:PostCreate, session: AsyncSession=Depends(get_session)):
    
    user_post = await post_service.create_new_posts(post_data,session)
    
    return user_post


@post_router.get("/{post_uid}", response_model=PostOut)
async def get_post_by_id(post_uid:str, session:AsyncSession=Depends(get_session)):
    
    post = await post_service.get_posts_by_id(post_uid=post_uid,session=session)
    
    return post

@post_router.put("/{post_uid}", response_model=PostOut)
async def update_post(post_uid:str, post_data:PostCreate, session:AsyncSession=Depends(get_session)):
    is_post = await post_service.get_posts_by_id(post_uid,session)
    
    if is_post:
        updated_post = await post_service.update_post(post_update_data=post_data,session=session)
        
        return updated_post
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Post not found")
    
    
@post_router.delete("/{post_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_uid:str,session:AsyncSession = Depends(get_session)):
    
    post = await post_service.delete_post(post_uid=post_uid,session=session)
    
    if post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

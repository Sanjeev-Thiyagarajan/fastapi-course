from app.v1.models.models import Vote,Post
from fastapi import status
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from sqlmodel import desc, select
from app.v1.service.post import PostService
from app.v1.schemas.vote import VoteModel, VoteCreate


post_service = PostService()

class VoteService:
    async def get_all_votes(self,user_uid:str,session:AsyncSession):
        statement = select(Vote).where(Vote.user_uid == user_uid)
        results = session.exec(statement)
        return results.all()
  
    async def add_vote_to_post(self,vote: VoteCreate,user_uid:str, post_uid:str,session:AsyncSession):
        statement = select(Vote).where(Vote.post_uid == post_uid, Vote.user_uid == user_uid)
        result = await session.exec(statement)
        vote_found = result.first()
        
        post = await post_service.get_posts_by_id(post_uid=post_uid, session=session)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Post with this {post} does not exits")
        
        # Check if post has been voted previously
        if vote.dir == 1:
            if vote_found:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f" user {user_uid} has already voted on post {post_uid}")
            
            new_vote = Vote(post_uid=post_uid, user_uid=user_uid)
            session.add(new_vote)
            await session.commit()
            await session.refresh(new_vote)
            
            return {"message":"Succesfully added vote"}
        
        
    async def delete_vote_from_post(self,user_uid:str, post_uid:str, session:AsyncSession):
        
        # Check if post has a vote on it
        vote_query = select(Vote).where(Vote.post_uid == post_uid, Vote.user_uid == user_uid)
                
        result = await session.exec(vote_query)
        
        
        user_vote = result.first()
    

        if not user_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You can't downvote someone's vote on your post")
            # get post to be sure user has access to this post
    
        await session.delete(user_vote)
        await session.commit()
            
        return {"message":"Successfully deleted vote."}
        
            
        
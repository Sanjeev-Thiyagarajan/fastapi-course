from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.database import get_session
from app.v1.service.vote import VoteService
from app.v1.schemas.vote import VoteModel, VoteCreate
from app.core.depedencies import AccessTokenBearer

vote_router = APIRouter()
vote_service = VoteService()


@vote_router.post("/", status_code=status.HTTP_201_CREATED)
async def vote_post(vote_data:VoteCreate,post_uid:str ,token_details:dict=Depends(AccessTokenBearer()), session:AsyncSession=Depends(get_session)):

        user_uid = token_details["user_data"]["user_uid"]
        
        vote = await vote_service.add_vote_to_post(vote=vote_data,user_uid=user_uid,post_uid=post_uid,session=session)
    
        return vote

@vote_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote(post_uid:str, token_details:dict=Depends(AccessTokenBearer()), session:AsyncSession=Depends(get_session)):
    user_uid = token_details["user_data"]["user_uid"]
    
    print(f"user id", user_uid)
    print(f"post id", post_uid)
    
    vote_delete = await vote_service.delete_vote_from_post(user_uid=user_uid, post_uid=post_uid,session=session)
    
    if vote_delete:
            return {"message": "Successfully deleted vote"}
    

    

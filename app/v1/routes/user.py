from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.database import get_session
from app.v1.schemas import schemas
from app.utils import utils
from app.core import oauth2
from app.v1.models import models
from app.v1.service.auth import AuthService
from app.v1.schemas.auth import UserCreate

user_router = APIRouter()

auth_service = AuthService()






@user_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    
    email = user_data.email
    
    user_exists = await auth_service.user_exists(email,session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email exists already")

    
    new_user = await auth_service.create_user(user_data,session)
    
    return new_user    
    


@user_router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: AsyncSession = Depends(get_session), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

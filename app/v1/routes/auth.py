from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.database import get_session
from app.v1.schemas.auth import UserOut
from app.utils.utils import generate_password_hash,verify_password,create_access_token,decode_access_token
from app.core import oauth2
from app.v1.models import models
from app.v1.service.auth import AuthService
from app.v1.schemas.auth import UserCreate
from fastapi.responses import JSONResponse

auth_router = APIRouter()

auth_service = AuthService()


@auth_router.post("/signup", response_model=UserOut , status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    
    email = user_data.email
    
    user_exists = await auth_service.user_exists(email,session)
    
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email exists already")

    
    new_user = await auth_service.create_user(user_data,session)
    
    return new_user    
    
@auth_router.post("/login")
async def login_user(user_data:UserCreate, session: AsyncSession=Depends(get_session)):
    
    user_email = user_data.email
    user_password = user_data.password

    user = await auth_service.get_user_by_email(user_email,session)
    
    if user is not None:
        password_valid = verify_password(user_password, user.password_hash)
        
        if password_valid:
            access_token = create_access_token(user_data={"email":user.email, "user_uid":user.uid})
            refresh_token = create_access_token(user_data={"email":user.email,"user_uid":user.uid}, refresh=True)
            
            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user": {"email": user.email,"user_uid":user.uid}
                }
            )

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email and Password")






@auth_router.get('/{id}')
def get_user(id: int, db: AsyncSession = Depends(get_session), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

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
from app.core.depedencies import RefreshTokenBearer,AccessTokenBearer, get_current_user
from datetime import datetime
from app.utils.utils import create_access_token
from app.utils.redis import add_jti_to_blocklist

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
            access_token = create_access_token(user_data={"email":user.email, "user_uid":str(user.uid)})
            refresh_token = create_access_token(user_data={"email":user.email,"user_uid":str(user.uid)}, refresh=True)
            
            return JSONResponse(
                content={
                    "message":"Login successful",
                    "access_token":access_token,
                    "refresh_token":refresh_token,
                    "user": {"email": user.email,"user_uid":str(user.uid)}
                }
            )

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email and Password")


@auth_router.get("/refresh_token")
async def generate_new_access_token(token_details:dict=RefreshTokenBearer()):
    
    expiry_time = token_details["exp"]
    
    if datetime.fromtimestamp(expiry_time) > datetime.now():
        access_token = create_access_token(user_data=token_details["user"])
        
        return JSONResponse(content={"access_token": access_token})
    
    raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or Expired Token")

@auth_router.get("/me")
async def get_current_user(user =Depends(get_current_user)):
    return user

@auth_router.get("/logout")
async def revoke_token(token_details: dict=Depends(AccessTokenBearer())):
    print(token_details)
    jti=token_details["jti"]
    
    await add_jti_to_blocklist(jti=jti)
    
    return JSONResponse(content={
        "message":"Logged Out Successfully"
    },
    status_code=status.HTTP_200_OK
                        
    )
    




from app.v1.models.models import User,Post,Vote
from app.v1.schemas.auth import UserCreate
from app.utils.utils import generate_password_hash
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import Depends 

class AuthService:
    async def get_user_by_email(self,email:str, session:AsyncSession):
        statement = select(User).where(User.email == email)
            
        result = await session.exec(statement)
        
        user = result.first()
        
        return user
    
    async def user_exists(self,email:str,session:AsyncSession):
        user = await self.get_user_by_email(email,session)
        
        return True if user is not None else None
    
    async def create_user(self,user_data:UserCreate, session:AsyncSession):
        user_data_dict = user_data.model_dump()
        
        new_user = User(**user_data_dict)
        
        new_user.password_hash = generate_password_hash(user_data_dict["password"])
        
        session.add(new_user)
        
        await session.commit()
                
        return new_user

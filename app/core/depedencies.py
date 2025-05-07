from fastapi import Request, HTTPException, status
from fastapi.security.http import HTTPAuthorizationCredentials
from typing_extensions import Annotated, Doc
from fastapi.security import HTTPBearer
from typing import Optional
from app.utils.utils import decode_access_token
from app.utils.redis import token_in_blocklist 


class TokenBearer(HTTPBearer):
    def __init__(self,auto_error=True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_access_token(token=token)
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
                "error":"This token is invalid or has been revoked",
                "resolution": "Please get a new token"
            })
        
        
        if not self.token_valid(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={
                "error":"Token has expired",
                "Solution":"Please get a new token"
            })
            
        self.verify_token(token_data)
        
        return token_data
    
    def token_valid(token: str) -> bool:
        token_data = decode_access_token(token=token)
        
        return token_data is not None
    
    def verify_token(token_data:dict):
        return NotImplementedError("Please Override this in Child Class")
    
class AccessTokenBearer(TokenBearer):
    def verify_token(token_data: dict):
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide an access token")
        
class RefreshTokenBearer(TokenBearer):
    def verify_token(token_data: dict):
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a refresh token")
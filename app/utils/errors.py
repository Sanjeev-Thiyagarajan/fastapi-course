from typing import Any,Callable
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import FastAPI, status

class OrdersEndpoint(Exception):
    """ This is the base class for all Orders-Endpoint Errors """
    pass

class InvalidToken(OrdersEndpoint):
    "User provides an invalid or expired token"
    pass

class RevokedToken(OrdersEndpoint):
    "Users has provided a token that has been revoked"
    pass

class AccessTokenRequired(OrdersEndpoint):
    "User has provided a refresh token when an access token is needed"
    pass

class RefreshTokenRequired(OrdersEndpoint):
    "User has provided an Access token when a refresh token is required"
    pass

class UserAlreadyExists(OrdersEndpoint):
    "User provides an email for a user who exists during sign up"
    pass
    
class InvalidCredentials(OrdersEndpoint):
    "User has provided wrong email or password during login"
    pass

class InsufficientPermission(OrdersEndpoint):
    "User does  not have the necessary permission to perform an action"
    pass

class PostNotFound(OrdersEndpoint):
    "User's post not found"
    pass

class VoteNotFound(OrdersEndpoint):
    "User's vote not found or not accessible"
    pass

class UserNotFound(OrdersEndpoint):
    "User not found"
    pass



def create_exception_handler(status_code:int, initial_detail:Any) -> Callable[[Request,Exception], JSONResponse]:
    async def exception_handler(request:Request, exc:OrdersEndpoint):
        return JSONResponse(content=initial_detail, status_code=status_code)
        
    return exception_handler


def register_error_handlers(app:FastAPI):
    app.add_exception_handler(UserAlreadyExists,create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, initial_detail={
        "message":"User with email already exits",
        "error_code":"user_exists"
    }))
    
    app.add_exception_handler(UserNotFound, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, initial_detail={
        "message":"User not found",
        "error_code":"user_not_found"
    }))
    
    app.add_exception_handler(PostNotFound, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, initial_detail={
        "message":"Post not found",
        "error_code":"post_not_found"
    }))
    
    app.add_exception_handler(VoteNotFound, create_exception_handler(status_code=status.HTTP_404_NOT_FOUND, initial_detail={
        "message":"Vote not found",
        "error_code":"vote_not_found"
    }))
    
    app.add_exception_handler(InsufficientPermission, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message":"Unauthorized",
        "error_code":"unauthorized"
    }))
    
    app.add_exception_handler(InvalidCredentials, create_exception_handler(status_code=status.HTTP_400_BAD_REQUEST, initial_detail={
        "message":"Invalid Email or Password",
        "error_code":"invalid_email_or_password"
    }))
    
    app.add_exception_handler(InvalidToken, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message":"Token is invalid or expired",
        "resolution":"please get a new token",
        "error_code":"invalid_token"
    }))
    
    app.add_exception_handler(RevokedToken, create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message":"Token is invalid or has been revoked",
        "resolution":"Please get new token",
        "error_code":"token_revoked"
    }))
    
    app.add_exception_handler(AccessTokenRequired,create_exception_handler(status_code=status.HTTP_401_UNAUTHORIZED, initial_detail={
        "message":"Please provide a valid access token",
        "error_code":"access_token_required",
        "resolution":"Please get an access token"    
    }))
    
    app.add_exception_handler(RefreshTokenRequired, create_exception_handler(status_code=status.HTTP_403_FORBIDDEN, initial_detail={
        "message":"Please provide a valid refresh token",
        "resolution":"Please get a refresh token",
        "error_code":"refresh_token_required"
    }))
    
    
    @app.exception_handler(500)
    async def internal_server_error(request,exc):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message":"Oops! Somthing went wrong",
                "error_code":"server_error"
            }, 
        )
    
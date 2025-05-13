from fastapi import FastAPI
from contextlib import asynccontextmanager


from .db.database import engine
from app.v1.routes.auth import auth_router
from app.v1.routes.post import post_router
from app.v1.routes.vote import vote_router
from app.db.database import initdb
from app.utils.errors import register_error_handlers



# models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app:FastAPI):
    print("Server is starting up....")
    
    await initdb()
    
    yield 
    
    
    print("Server is shutting down....")
    
version = "v1"
version_prefix = f"/api/{version}"


app = FastAPI(
    title="Blog Project",
    description="A sample API to manage user's blogs",
    version=version,
    # lifespan=lifespan
)

register_error_handlers(app)


app.include_router(auth_router,prefix=f"/api/{version}/auth", tags=["Auth"])
app.include_router(post_router, prefix=f"/api/{version}/posts", tags=["Posts"])
app.include_router(vote_router, prefix=f"/api/{version}/vote", tags=["Tags"])



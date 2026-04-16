from fastapi import APIRouter
from app.api.v1.endpoints import consumers, sources 

api_router = APIRouter()

api_router.include_router(consumers.router, prefix="/consumers", tags=["consumers"])
api_router.include_router(sources.router, prefix="/sources", tags=["sources"])


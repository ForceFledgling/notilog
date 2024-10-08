from fastapi import APIRouter

from .endpoints import router

events_router = APIRouter()
events_router.include_router(router, tags=["Модуль событий"])

__all__ = ["events_router"]

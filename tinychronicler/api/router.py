from fastapi import APIRouter, Request

router = APIRouter(prefix="/api")


@router.get("/")
async def index(request: Request):
    return {}

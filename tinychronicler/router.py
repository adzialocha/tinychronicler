from fastapi import APIRouter, HTTPException, Request, status, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page
from fastapi_pagination.ext.databases import paginate
from sqlalchemy import select
from pydantic import BaseModel

from . import crud, models, schemas
from .constants import TEMPLATES_DIR
from .database import database

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


class NotFoundResponse(BaseModel):
    detail: str


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post(
    "/api/chronicles",
    response_model=schemas.Chronicle,
    status_code=status.HTTP_201_CREATED,
)
async def create_chronicle(chronicle: schemas.ChronicleCreate):
    last_record_id = await crud.create_chronicle(chronicle)
    return {**chronicle.dict(), "id": last_record_id}


@router.get("/api/chronicles", response_model=Page[schemas.Chronicle])
async def read_chronicles(request: Request):
    return await paginate(database, select([models.Chronicle]))


@router.get(
    "/api/chronicles/{chronicle_id}",
    response_model=schemas.Chronicle,
    responses={404: {"model": NotFoundResponse}},
)
async def read_chronicle(chronicle_id: int):
    result = await crud.get_chronicle(chronicle_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    return result


@router.put(
    "/api/chronicles/{chronicle_id}",
    responses={
        404: {"model": NotFoundResponse},
    },
)
async def update_chronicle(
    chronicle_id: int, chronicle: schemas.ChronicleCreate
):
    result = await crud.update_chronicle(chronicle_id, chronicle)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/api/chronicles/{chronicle_id}",
    responses={404: {"model": NotFoundResponse}},
)
async def delete_chronicle(chronicle_id: int):
    result = await crud.delete_chronicle(chronicle_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    return Response(status_code=status.HTTP_200_OK)

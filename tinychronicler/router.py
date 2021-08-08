from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Page
from fastapi_pagination.ext.databases import paginate
from pydantic import BaseModel
from sqlalchemy import select

from . import crud, models, schemas
from .constants import TEMPLATES_DIR
from .database import database
from .files import ALLOWED_MIME_TYPES, store_file

router = APIRouter()

templates = Jinja2Templates(directory=TEMPLATES_DIR)


class CustomResponse(BaseModel):
    detail: str


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post(
    "/api/chronicles",
    response_model=schemas.Chronicle,
    status_code=status.HTTP_201_CREATED,
)
async def create_chronicle(chronicle: schemas.ChronicleIn):
    last_record_id = await crud.create_chronicle(chronicle)
    return {**chronicle.dict(), "id": last_record_id}


@router.get("/api/chronicles", response_model=Page[schemas.Chronicle])
async def read_chronicles(request: Request):
    return await paginate(database, select([models.Chronicle]))


@router.get(
    "/api/chronicles/{chronicle_id}",
    response_model=schemas.Chronicle,
    responses={404: {"model": CustomResponse}},
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
        404: {"model": CustomResponse},
    },
)
async def update_chronicle(
    chronicle_id: int, chronicle: schemas.ChronicleIn
):
    result = await crud.update_chronicle(chronicle_id, chronicle)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    return Response(status_code=status.HTTP_200_OK)


@router.delete(
    "/api/chronicles/{chronicle_id}",
    responses={404: {"model": CustomResponse}},
)
async def delete_chronicle(chronicle_id: int):
    result = await crud.delete_chronicle(chronicle_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/api/chronicles/{chronicle_id}/files",
    responses={415: {"model": CustomResponse}, 404: {"model": CustomResponse}},
)
async def create_file(chronicle_id: int, file: UploadFile = File(...)):
    chronicle = await crud.get_chronicle(chronicle_id)
    if chronicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="File format {} is not supported".format(file.content_type),
        )
    upload = await store_file(file)
    return {
        "fileName": upload["file_name"],
        "fileType": upload["file_type"],
        "fileUrl": upload["file_url"],
        "thumbName": upload["thumb_name"],
        "thumbUrl": upload["thumb_url"],
    }

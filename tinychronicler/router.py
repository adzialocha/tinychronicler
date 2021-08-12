from fastapi import (
    APIRouter,
    BackgroundTasks,
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

from . import crud, models, schemas, tasks
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


@router.get("/api/chronicles", response_model=Page[schemas.ChronicleOut])
async def read_chronicles():
    return await paginate(database, select([models.Chronicle]))


@router.get(
    "/api/chronicles/{chronicle_id}",
    response_model=schemas.ChronicleOut,
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
async def update_chronicle(chronicle_id: int, chronicle: schemas.ChronicleIn):
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
    # Store and process file first ..
    upload = await store_file(file)
    # ..then make an entry in the database
    file_id = await crud.create_file(
        schemas.FileIn(
            name=upload["file_name"],
            path=upload["file_path"],
            url=upload["file_url"],
            mime=upload["file_mime"],
            thumb_name=upload["thumb_name"],
            thumb_path=upload["thumb_path"],
            thumb_url=upload["thumb_url"],
        ),
        chronicle_id,
    )
    return {
        "id": file_id,
        "fileName": upload["file_name"],
        "fileMime": upload["file_mime"],
        "fileUrl": upload["file_url"],
        "thumbName": upload["thumb_name"],
        "thumbUrl": upload["thumb_url"],
    }


@router.get(
    "/api/chronicles/{chronicle_id}/files",
    response_model=Page[schemas.FileOut],
)
async def read_files(chronicle_id: int):
    return await paginate(
        database,
        select([models.File]).where(models.File.chronicle_id == chronicle_id),
    )


@router.get(
    "/api/chronicles/{chronicle_id}/files/{file_id}",
    response_model=schemas.FileOut,
    responses={404: {"model": CustomResponse}},
)
async def read_file(chronicle_id: int, file_id: int):
    result = await crud.get_file(file_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    if result.chronicle_id is not chronicle_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File does not belong to chronicle",
        )
    return result


@router.delete(
    "/api/chronicles/{chronicle_id}/files/{file_id}",
    responses={404: {"model": CustomResponse}, 403: {"model": CustomResponse}},
)
async def delete_file(chronicle_id: int, file_id: int):
    file = await crud.get_file(file_id)
    if file is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="File not found"
        )
    if file.chronicle_id is not chronicle_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="File does not belong to chronicle",
        )
    await crud.delete_file(file_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/api/chronicles/{chronicle_id}/compositions",
    responses={404: {"model": CustomResponse}},
)
async def create_composition(
    chronicle_id: int, background_tasks: BackgroundTasks
):
    chronicle = await crud.get_chronicle(chronicle_id)
    if chronicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chronicle not found"
        )
    background_tasks.add_task(tasks.generate_composition, chronicle_id)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.get(
    "/api/chronicles/{chronicle_id}/compositions",
    response_model=Page[schemas.CompositionOut],
)
async def read_compositions(chronicle_id: int):
    return await paginate(
        database,
        select([models.Composition]).where(
            models.Composition.chronicle_id == chronicle_id
        ),
    )


@router.get(
    "/api/chronicles/{chronicle_id}/compositions/{composition_id}",
    response_model=schemas.CompositionOut,
    responses={404: {"model": CustomResponse}},
)
async def read_composition(chronicle_id: int, composition_id: int):
    result = await crud.get_composition(composition_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Composition not found",
        )
    if result.chronicle_id is not chronicle_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Composition does not belong to chronicle",
        )
    return result


@router.delete(
    "/api/chronicles/{chronicle_id}/compositions/{composition_id}",
    responses={404: {"model": CustomResponse}, 403: {"model": CustomResponse}},
)
async def delete_composition(chronicle_id: int, composition_id: int):
    composition = await crud.get_composition(composition_id)
    if composition is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Composition not found",
        )
    if composition.chronicle_id is not chronicle_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Composition does not belong to chronicle",
        )
    if not composition.is_ready:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't delete composition which is not ready yet",
        )
    await crud.delete_composition(composition_id)
    return Response(status_code=status.HTTP_200_OK)

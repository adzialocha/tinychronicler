from sqlalchemy import select, insert, update, delete

from . import models, schemas
from .database import database


async def create_chronicle(chronicle: schemas.Chronicle):
    query = insert(models.Chronicle).values(
        title=chronicle.title, description=chronicle.description
    )
    return await database.execute(query)


async def get_chronicle(chronicle_id: int):
    query = select([models.Chronicle]).where(
        models.Chronicle.id == chronicle_id
    )
    return await database.fetch_one(query)


async def get_chronicles():
    query = select([models.Chronicle])
    return await database.fetch_all(query)


async def update_chronicle(
    chronicle_id: int, chronicle: schemas.ChronicleCreate
):
    print(chronicle_id, chronicle)
    query = (
        update(models.Chronicle)
        .where(models.Chronicle.id == chronicle_id)
        .values(title=chronicle.title, description=chronicle.description)
    )
    return await database.execute(query)


async def delete_chronicle(chronicle_id: int):
    query = delete(models.Chronicle).where(models.Chronicle.id == chronicle_id)
    return await database.execute(query)

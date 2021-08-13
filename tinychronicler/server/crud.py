from sqlalchemy import delete, insert, select, update

from tinychronicler.database import database, models, schemas


async def create_chronicle(chronicle: schemas.ChronicleIn):
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


async def update_chronicle(chronicle_id: int, chronicle: schemas.ChronicleIn):
    query = (
        update(models.Chronicle)
        .where(models.Chronicle.id == chronicle_id)
        .values(title=chronicle.title, description=chronicle.description)
    )
    return await database.execute(query)


async def delete_chronicle(chronicle_id: int):
    query = delete(models.Chronicle).where(models.Chronicle.id == chronicle_id)
    return await database.execute(query)


async def create_file(file: schemas.FileIn, chronicle_id: int):
    query = insert(models.File).values(
        name=file.name,
        path=file.path,
        url=file.url,
        mime=file.mime,
        thumb_name=file.thumb_name,
        thumb_path=file.thumb_path,
        thumb_url=file.thumb_url,
        chronicle_id=chronicle_id,
    )
    return await database.execute(query)


async def get_file(file_id: int):
    query = select([models.File]).where(models.File.id == file_id)
    return await database.fetch_one(query)


async def get_files(chronicle_id: int):
    query = select([models.File]).where(
        models.File.chronicle_id == chronicle_id
    )
    return await database.fetch_all(query)


async def delete_file(file_id: int):
    query = delete(models.File).where(models.File.id == file_id)
    return await database.execute(query)


async def create_composition(
    composition: schemas.CompositionIn, chronicle_id: int
):
    query = insert(models.Composition).values(
        chronicle_id=chronicle_id,
        is_ready=composition.is_ready,
        data=composition.data,
        title=composition.title,
    )
    return await database.execute(query)


async def get_composition(composition_id: int):
    query = select([models.Composition]).where(
        models.Composition.id == composition_id
    )
    return await database.fetch_one(query)


async def get_compositions(chronicle_id):
    query = select([models.Composition]).where(
        models.Composition.chronicle_id == chronicle_id
    )
    return await database.fetch_all(query)


async def update_composition(
    composition_id: int, composition: schemas.CompositionIn
):
    query = (
        update(models.Composition)
        .where(models.Composition.id == composition_id)
        .values(
            is_ready=composition.is_ready,
            data=composition.data,
            title=composition.title,
        )
    )
    return await database.execute(query)


async def delete_composition(composition_id: int):
    query = delete(models.Composition).where(
        models.Composition.id == composition_id
    )
    return await database.execute(query)

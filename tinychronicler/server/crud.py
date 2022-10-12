from sqlalchemy import delete, insert, select, update

from tinychronicler.database import database, models, schemas

from .files import remove_file


async def create_chronicle(chronicle: schemas.ChronicleIn):
    query = insert(models.Chronicle).values(
        title=chronicle.title,
        description=chronicle.description,
        language=chronicle.language
    )
    return await database.execute(query)


async def get_chronicle(chronicle_id: int):
    query = select([models.Chronicle]).where(
        models.Chronicle.id == chronicle_id
    )
    return await database.fetch_one(query)


async def get_chronicles():
    query = select([models.Chronicle]).order_by(
        models.Chronicle.created_at.desc())
    return await database.fetch_all(query)


async def update_chronicle(chronicle_id: int, chronicle: schemas.ChronicleIn):
    query = (
        update(models.Chronicle)
        .where(models.Chronicle.id == chronicle_id)
        .values(title=chronicle.title, description=chronicle.description)
    )
    return await database.execute(query)


async def delete_chronicle(chronicle_id: int):
    # Delete related compositions
    compositions = await get_compositions(chronicle_id)
    # Check first if compositions are still being generated
    for composition in compositions:
        if not composition.is_ready:
            raise Exception(
                "Can not delete chronicle while composition is generated")
    for composition in compositions:
        await delete_composition(composition.id)
    # Delete related files
    files = await get_files(chronicle_id)
    for file in files:
        remove_file(file)
    # Finally delete chronicle entry
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
    # Get file and delete it
    file = await get_file(file_id)
    remove_file(file)
    # Delete entry in database
    query = delete(models.File).where(models.File.id == file_id)
    return await database.execute(query)


async def create_composition(
    composition: schemas.CompositionIn, chronicle_id: int
):
    query = insert(models.Composition).values(
        chronicle_id=chronicle_id,
        data=composition.data,
        is_ready=composition.is_ready,
        title=composition.title,
        version=composition.version,
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

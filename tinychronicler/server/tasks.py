import asyncio
import pickle
from threading import Thread

from loguru import logger

from tinychronicler.database import schemas
from tinychronicler.generator import generator

from . import crud


async def generate_composition(chronicle_id: int):
    async def generate_composition_thread(chronicle_id: int):
        logger.info(
            "Generate new composition based on chronicle {}".format(
                chronicle_id)
        )

        # Insert pending composition in database
        chronicle = await crud.get_chronicle(chronicle_id)
        title = chronicle.title
        composition = schemas.CompositionIn(title=title,
                                            data=None,
                                            is_ready=False,
                                            version=1)
        last_record_id = await crud.create_composition(composition,
                                                       chronicle_id)

        # Generate composition, this might take some time ..
        files = await crud.get_files(chronicle_id)
        data = generator.generate_composition(files, chronicle.language)

        # Update composition with new data and set it ready
        composition.data = pickle.dumps(data)
        composition.is_ready = True
        await crud.update_composition(last_record_id, composition)
        logger.info(
            "Finished generation of new composition based on chronicle {}"
            .format(chronicle_id))

    def thread_handler(chronicle_id: int):
        asyncio.run(generate_composition_thread(chronicle_id))

    # Move it all into a separate thread as loading an large audio file blocks
    # the main thread
    new_thread = Thread(target=thread_handler, args=(chronicle_id,))
    new_thread.start()

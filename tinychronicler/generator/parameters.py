from typing import Any, List, Tuple

import numpy as np
from loguru import logger


def check_movements(config):
    movement_total_percentage = 0

    for movement in config:
        movement_total_percentage += movement['percentage']
        sections_total_percentage = 0
        for section in movement['sections']:
            sections_total_percentage += section['percentage']
            scenes_total_percentage = 0
            for scene in section['scenes']:
                scenes_total_percentage += scene['percentage']
            if scenes_total_percentage != 1:
                raise Exception("Invalid scene total percentage (not 100%)")
        if sections_total_percentage != 1:
            raise Exception("Invalid sections total percentage (not 100%)")

    if movement_total_percentage != 1:
        raise Exception("Invalid movement total percentage (not 100%)")


def generate_parameters(modules: List[Tuple[int, int]], movements: List[Any]):
    check_movements(movements)

    # Prepare values for generation
    movement = 0
    section = 0

    movement_start = 0
    movement_end = movements[movement]['percentage']

    section_start = 0
    section_end = movements[movement]['sections'][section]['percentage']

    # Go through all modules and find parameters for each of them
    result = []
    for (index, module) in enumerate(modules):
        current_position = index / len(modules)

        # Determine movement
        if movement_end < current_position:
            movement += 1
            section = 0
            sections = movements[movement]['sections']
            section_start = 0
            section_end = sections[section]['percentage']
            movement_start = movement_end
            movement_end = movement_start + \
                movements[movement]['percentage']

        # Determine section
        current_section_position = (
            current_position - movement_start
        ) / (movement_end - movement_start)
        if section_end < current_section_position:
            section += 1
            section_start = section_end
            section_end = section_start + \
                movements[movement]['sections'][section]['percentage']

        scenes = movements[movement]['sections'][section]['scenes']
        scenes_probabilities = [s['percentage'] for s in scenes]

        # Randomly find scene with parameters
        scene = np.random.choice(scenes, None, True, scenes_probabilities)
        logger.debug("Pick scene {} for module #{}".format(
            scene['name'], index))

        result.append({
            "parameters": scene['parameters'],
            "module": module,
        })

    return result

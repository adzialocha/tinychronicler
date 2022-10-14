from tinychronicler.database import schemas


def create_text_score(title: str,
                      composition_data: schemas.CompositionData):
    score = ''

    # Composition data
    current_module_index = 0
    modules = composition_data["parameters"]
    notes = composition_data["notes"]
    notes_human = notes[0]
    notes_robot = notes[1]
    total_modules = len(modules)

    while current_module_index < total_modules:
        # Get composition data for next module
        module = modules[current_module_index]
        parameters = module["parameters"]
        (module_id, start_time, end_time) = module["module"]

        # Performance state
        video = "VIDEO" in parameters
        photo = "PHOTO" in parameters
        audio = "NARRATOR" in parameters
        human = "VOICE_1" in parameters
        robot = "VOICE_2" in parameters

        # @TODO

    return score

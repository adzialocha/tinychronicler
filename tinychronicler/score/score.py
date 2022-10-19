from tinychronicler.constants import MIDI_MODULES_1, MIDI_MODULES_2
from tinychronicler.database import schemas

SILENCE_MODULE = 0
MODULE_BREAK = 8  # Make a visual break every x modules

# Character Table:
#   0 0 2 3 4 5 6 7 8 9 A B C D E F
# 8 Ç ü é â ä à å ç ê ë è ï î ì Ä Å
# 9 É æ Æ ô ö ò û ù ÿ Ö Ü ¢ £ ¥ ₧ ƒ
# A á í ó ú ñ Ñ ª º ¿ ⌐ ¬ ½ ¼ ¡ « »
# B ░ ▒ ▓ │ ┤ ╡ ╢ ╖ ╕ ╣ ║ ╗ ╝ ╜ ╛ ┐
# C └ ┴ ┬ ├ ─ ┼ ╞ ╟ ╚ ╔ ╩ ╦ ╠ ═ ╬ ╧
# D ╨ ╤ ╥ ╙ ╘ ╒ ╓ ╫ ╪ ┘ ┌ █ ▄ ▌ ▐ ▀
# E α ß Γ π Σ σ μ τ Φ Θ Ω δ ∞ φ ε ∩
# F ≡ ± ≥ ≤ ⌠ ⌡ ÷ ≈ ° · · √ ⁿ ²
PHOTO_CHAR = "▓"
VIDEO_CHAR = "█"
AUDIO_CHAR = "≈"
TACET_CHAR = "·"

HUMAN_PARAMETERS = ["HUMAN_1", "HUMAN_2", "HUMAN_3", "HUMAN_4"]
ROBOT_PARAMETERS = ["ROBOT_1", "ROBOT_2", "ROBOT_BASS"]

HUMAN_1_CHAR = "─"
HUMAN_2_CHAR = "═"
HUMAN_3_CHAR = "≡"
HUMAN_4_CHAR = "╪"

ROBOT_1_CHAR = "─"
ROBOT_2_CHAR = "═"
ROBOT_BASS_CHAR = "φ"


def contains(a, b):
    for item in a:
        if item in b:
            return True
    return False


def create_text_score(composition_data: schemas.CompositionData):
    lines = []
    current_module_index = 0

    # Composition data
    modules = composition_data["parameters"]
    total_modules = len(modules)

    temp_lines = []
    offset = int(MODULE_BREAK / 2)

    # Helper method to bring voices underneath each other
    def bring_voices_together():
        if len(temp_lines) > 0:
            for index in range(0, offset):
                if len(temp_lines) - 1 >= index + offset:
                    lines.append("{}{}".format(temp_lines[index + offset],
                                               temp_lines[index]))
                elif len(temp_lines) - 1 >= index:
                    lines.append("{}{}".format("        ",
                                               temp_lines[index]))
            temp_lines.clear()
            lines.append("")

    while current_module_index < total_modules:
        if current_module_index % MODULE_BREAK == 0:
            bring_voices_together()

        # Get composition data for next module
        module = modules[current_module_index]
        parameters = module["parameters"]
        (id_1, id_2, _, _) = module["module"]

        # Performance state
        video = "VIDEO" in parameters
        photo = "PHOTO" in parameters
        audio = "NARRATOR" in parameters
        legato = "LEGATO" in parameters
        human = contains(HUMAN_PARAMETERS, parameters)
        robot = contains(ROBOT_PARAMETERS, parameters)

        visual_char = " "
        if photo:
            visual_char = PHOTO_CHAR
        elif video:
            visual_char = VIDEO_CHAR

        audio_char = " "
        if audio:
            audio_char = AUDIO_CHAR

        robot_char = TACET_CHAR
        robot_oct_char = " "
        if id_2 != SILENCE_MODULE and robot:
            robot_char = MIDI_MODULES_2[id_2 - 1]["character"]
            if "ROBOT_1" in parameters:
                robot_oct_char = ROBOT_1_CHAR
            elif "ROBOT_2" in parameters:
                robot_oct_char = ROBOT_2_CHAR
            elif "ROBOT_BASS" in parameters:
                robot_oct_char = ROBOT_BASS_CHAR
            if legato:
                robot_char = robot_char.lower()

        human_char = TACET_CHAR
        human_oct_char = " "
        if id_1 != SILENCE_MODULE and human:
            human_char = MIDI_MODULES_1[id_1 - 1]["character"]
            if "HUMAN_1" in parameters:
                human_oct_char = HUMAN_1_CHAR
            elif "HUMAN_2" in parameters:
                human_oct_char = HUMAN_2_CHAR
            elif "HUMAN_3" in parameters:
                human_oct_char = HUMAN_3_CHAR
            elif "HUMAN_4" in parameters:
                human_oct_char = HUMAN_4_CHAR
            if legato:
                human_char = human_char.lower()

        temp_lines.append("{}{}{}{} {}{} ".format(robot_char,
                                                  robot_oct_char,
                                                  human_char,
                                                  human_oct_char,
                                                  visual_char,
                                                  audio_char,
                                                  ))

        current_module_index += 1

    bring_voices_together()

    return '\n'.join(lines)

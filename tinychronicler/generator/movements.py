def to_dict(namespace, arr):
    vals = {}
    for index, key in enumerate(arr):
        vals[key] = key
    return vals


PARAMETERS = to_dict("parameters", [
    "PHOTO",
    "VIDEO_ONLY",
    "VIDEO_W_SOUND",
    "BLACK",
    "NARRATOR",
    "VOCODER",
    "VOCODER_RELEASE_0.34",
    "VOCODER_RELEASE_0.65",
    "VOCODER_REVERB_0",
    "VOCODER_REVERB_-11",
    "TINY_CHRONICLER",
    "CHOIR",
    "BASS",
    "KAJSA_M",
    "KAJSA_L",
    "MALTE",
    "VOICES_SHORT",
    "VOICES_LONG",
    "VOICES_HP_0.6",
    "VOICES_HP_1.0",
    "VOICES_REVERB_-23",
    "VOICES_REVERB_-6",
])

SCENES = {
    "ONLY_NARRATOR": [
        PARAMETERS["NARRATOR"],
    ],
    "NARRATOR_W_2VOICES_HP": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["KAJSA_M"],
        PARAMETERS["MALTE"],
        PARAMETERS["VOICES_HP_0.6"],
        PARAMETERS["VOICES_SHORT"],
    ],
    "2VOICES": [
        PARAMETERS["KAJSA_M"],
        PARAMETERS["MALTE"],
        PARAMETERS["VOICES_HP_1.0"],
        PARAMETERS["VOICES_SHORT"],
    ],
}

MOVEMENTS = [
    {
        "name": "MOVEMENT_1",
        "percentage": 0.2,
        "sections": [
            {
                "name": "MOVEMENT_1_SECTION_1",
                "percentage": 0.15,
                "scenes": [
                    {
                        "name": "MOVEMENT_1_SECTION_1_SCENE_1",
                        "percentage": 1,
                        "parameters": SCENES["ONLY_NARRATOR"],
                    },
                ]
            },
            {
                "name": "MOVEMENT_1_SECTION_2",
                "percentage": 0.8,
                "scenes": [
                    {
                        "name": "MOVEMENT_1_SECTION_2_SCENE_1",
                        "percentage": 0.2,
                        "parameters": SCENES["ONLY_NARRATOR"],
                    },
                    {
                        "name": "MOVEMENT_1_SECTION_2_SCENE_2",
                        "percentage": 0.5,
                        "parameters": SCENES["NARRATOR_W_2VOICES_HP"],
                    },
                    {
                        "name": "MOVEMENT_1_SECTION_2_SCENE_3",
                        "percentage": 0.3,
                        "parameters": SCENES["2VOICES"],
                    }
                ]
            },
            {
                "name": "MOVEMENT_1_SECTION_3",
                "percentage": 0.05,
                "scenes": [
                    {
                        "name": "MOVEMENT_1_SECTION_3_SCENE_1",
                        "percentage": 1,
                        "parameters": SCENES["ONLY_NARRATOR"],
                    },
                ]
            },
        ],
    },
    {
        "name": "MOVEMENT_2",
        "percentage": 0.8,
        "sections": [
            {
                "name": "MOVEMENT_2_SECTION_1",
                "percentage": 1,
                "scenes": [
                    {
                        "name": "MOVEMENT_2_SECTION_1_SCENE_1",
                        "percentage": 1,
                        "parameters": SCENES["ONLY_NARRATOR"],
                    },
                ]
            },
        ],
    },
]

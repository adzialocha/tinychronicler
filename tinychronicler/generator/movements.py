def to_dict(namespace, arr):
    vals = {}
    for index, key in enumerate(arr):
        vals[key] = key
    return vals


PARAMETERS = to_dict("parameters", [
    "NARRATOR",
    "PHOTO",
    "VIDEO",
    # "VIDEO_W_SOUND", # Currently not supported
    "VOICE_1",
    "VOICE_2",
])

SCENES = {
    # ==================================
    "ONLY_NARRATOR": [
        PARAMETERS["NARRATOR"],
    ],
    # ==================================
    "TUTTI": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
        PARAMETERS["VOICE_2"],
    ],
    "TUTTI_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
        PARAMETERS["VOICE_2"],
        PARAMETERS["VIDEO"],
    ],
    "TUTTI_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
        PARAMETERS["VOICE_2"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "N_VOICE_1": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
    ],
    "N_VOICE_1_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
        PARAMETERS["VIDEO"],
    ],
    "N_VOICE_1_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_1"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "N_VOICE_2": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_2"],
    ],
    "N_VOICE_2_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_2"],
        PARAMETERS["VIDEO"],
    ],
    "N_VOICE_2_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["VOICE_2"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "VOICE_1_SOLO": [
        PARAMETERS["VOICE_1"],
    ],
    "VOICE_1_SOLO_W_VIDEO": [
        PARAMETERS["VOICE_1"],
        PARAMETERS["VIDEO"],
    ],
    "VOICE_1_SOLO_W_PHOTO": [
        PARAMETERS["VOICE_1"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "VOICE_2_SOLO": [
        PARAMETERS["VOICE_2"],
    ],
    "VOICE_2_SOLO_W_VIDEO": [
        PARAMETERS["VOICE_2"],
        PARAMETERS["VIDEO"],
    ],
    "VOICE_2_SOLO_W_PHOTO": [
        PARAMETERS["VOICE_2"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "BLACK": [],
    "TACET_W_VIDEO": [
        PARAMETERS["VIDEO"],
    ],
    "TACET_W_PHOTO": [
        PARAMETERS["PHOTO"],
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
                        "parameters": SCENES["TUTTI"],
                    },
                    {
                        "name": "MOVEMENT_1_SECTION_2_SCENE_3",
                        "percentage": 0.3,
                        "parameters": SCENES["TUTTI_W_PHOTO"],
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
                        "parameters": SCENES["TUTTI_W_VIDEO"],
                    },
                ]
            },
        ],
    },
]


MOVEMENTS_WITHOUT_PHOTO = MOVEMENTS

MOVEMENTS_WITHOUT_VIDEO = MOVEMENTS

MOVEMENTS_WITHOUT_VIDEO_AND_PHOTO = MOVEMENTS

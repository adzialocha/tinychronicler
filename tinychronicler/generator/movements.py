def to_dict(namespace, arr):
    vals = {}
    for index, key in enumerate(arr):
        vals[key] = key
    return vals


PARAMETERS = to_dict("parameters", [
    "NARRATOR",
    "PHOTO",
    "VIDEO",
    "HUMAN",
    "ROBOT",
])

SCENES = {
    # ==================================
    "ONLY_NARRATOR": [
        PARAMETERS["NARRATOR"],
    ],
    # ==================================
    "TUTTI": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
        PARAMETERS["ROBOT"],
    ],
    "TUTTI_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
        PARAMETERS["ROBOT"],
        PARAMETERS["VIDEO"],
    ],
    "TUTTI_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
        PARAMETERS["ROBOT"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "N_HUMAN": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
    ],
    "N_HUMAN_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
        PARAMETERS["VIDEO"],
    ],
    "N_HUMAN_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["HUMAN"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "N_ROBOT": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["ROBOT"],
    ],
    "N_ROBOT_W_VIDEO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["ROBOT"],
        PARAMETERS["VIDEO"],
    ],
    "N_ROBOT_W_PHOTO": [
        PARAMETERS["NARRATOR"],
        PARAMETERS["ROBOT"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "HUMAN_SOLO": [
        PARAMETERS["HUMAN"],
    ],
    "HUMAN_SOLO_W_VIDEO": [
        PARAMETERS["HUMAN"],
        PARAMETERS["VIDEO"],
    ],
    "HUMAN_SOLO_W_PHOTO": [
        PARAMETERS["HUMAN"],
        PARAMETERS["PHOTO"],
    ],
    # ==================================
    "ROBOT_SOLO": [
        PARAMETERS["ROBOT"],
    ],
    "ROBOT_SOLO_W_VIDEO": [
        PARAMETERS["ROBOT"],
        PARAMETERS["VIDEO"],
    ],
    "ROBOT_SOLO_W_PHOTO": [
        PARAMETERS["ROBOT"],
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
                        "percentage": 0.2,
                        "parameters": SCENES["TUTTI_W_VIDEO"],
                    },
                    {
                        "name": "MOVEMENT_2_SECTION_1_SCENE_1",
                        "percentage": 0.3,
                        "parameters": SCENES["HUMAN_SOLO_W_VIDEO"],
                    },
                    {
                        "name": "MOVEMENT_2_SECTION_1_SCENE_1",
                        "percentage": 0.5,
                        "parameters": SCENES["TUTTI"],
                    },
                ]
            },
        ],
    },
]


MOVEMENTS_WITHOUT_PHOTO = MOVEMENTS

MOVEMENTS_WITHOUT_VIDEO = MOVEMENTS

MOVEMENTS_WITHOUT_VIDEO_AND_PHOTO = MOVEMENTS

from lib.config import Configuration, RotorConfiguration, RotorInUseConfiguration, Pairings


test_configuration = Configuration(
    available_rotors=[
        RotorConfiguration(
            permutation=[14, 25, 16, 24, 7, 6, 2, 12, 4, 21, 10, 23, 3, 0, 5, 1, 13, 19, 11, 20, 22, 15, 9, 18, 17, 8]
        ),
        RotorConfiguration(
            permutation=[1, 21, 8, 5, 7, 24, 15, 4, 9, 0, 11, 18, 6, 25, 17, 2, 23, 12, 10, 3, 22, 19, 20, 16, 13, 14]
        ),
        RotorConfiguration(
            permutation=[13, 15, 5, 10, 8, 7, 24, 2, 0, 25, 6, 22, 12, 11, 20, 21, 16, 17, 3, 9, 18, 14, 4, 23, 19, 1]
        ),
        RotorConfiguration(
            permutation=[25, 6, 9, 23, 11, 22, 3, 14, 19, 0, 4, 10, 8, 21, 18, 20, 5, 16, 7, 24, 15, 17, 12, 13, 1, 2]
        ),
        RotorConfiguration(
            permutation=[4, 24, 10, 23, 21, 7, 2, 18, 11, 19, 15, 14, 16, 3, 20, 6, 8, 1, 12, 0, 13, 25, 17, 9, 22, 5]
        ),
    ],
    rotors_in_use=[
        RotorInUseConfiguration(
            type=3,
            starting_position=10,
            turnover_notch=2,
        ),
        RotorInUseConfiguration(
            type=1,
            starting_position=23,
            turnover_notch=0,
        ),
        RotorInUseConfiguration(
            type=4,
            starting_position=1,
            turnover_notch=13,
        ),
    ],
    plug_board=Pairings(
        pairings=[14, 25, 7, 15, 21, 9, 3, 18, 17, 11, 23, 1, 8, 10, 6, 12, 0, 20, 24, 2]
    ),
    reflector=Pairings(
        pairings=[10, 25, 14, 0, 5, 6, 1, 9, 16, 15, 4, 17, 19, 8, 18, 2, 23, 22, 24, 13, 12, 21, 20, 11, 7, 3]
    )
)

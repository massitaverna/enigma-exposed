import pydantic

from . import utils


class RotorConfiguration(pydantic.BaseModel):
    permutation: list[int]


class RotorInUseConfiguration(pydantic.BaseModel):
    type: int = pydantic.Field(
        description="Which of the available rotors this one is. Uses 0-indexing. Historically marked as I, II, ..., V."
    )
    starting_position: int = pydantic.Field(
        description="The rotor setting, i.e., from which starting position the rotor is inserted into the slot. "
        "Uses 0-indexing. Historically marked as 1 - 26.",
        min=0,
    )
    turnover_notch: int = pydantic.Field(
        description="Position that - when reached - causes the next rotor in use to turn over. Uses 0-indexing.",
        min=0,
    )


class Configuration(pydantic.BaseModel):
    available_rotors: list[RotorConfiguration]
    rotors_in_use: list[RotorInUseConfiguration]

    @pydantic.model_validator
    def unique_rotor_size(self) -> "Configuration":
        rotor_sizes = set([len(rotor.permutation) for rotor in self.available_rotors])
        if len(rotor_sizes) > 1:
            raise ValueError(
                f"available rotors have different sizes {rotor_sizes}: all rotors must have the same size"
            )
        return self

    @pydantic.model_validator
    def use_available_rotors(self) -> "Configuration":
        for rotor_in_use in self.rotors_in_use:
            if rotor_in_use.type < 0 or rotor_in_use.type >= len(self.available_rotors):
                raise ValueError(
                    f"want to use rotor type {rotor_in_use.type}, "
                    f"but only types 0 - {len(self.available_rotors)-1} are available"
                )
        return self
    
    @pydantic.model_validator
    def use_each_available_rotor_at_most_once(self) -> "Configuration":
        rotor_types = [rotor.type for rotor in self.rotors_in_use]
        if len(rotor_types) > len(set(rotor_types)):
            raise ValueError("can't use an available rotor more than once")
        return self

    @pydantic.model_validator
    def check_starting_position(self) -> "Configuration":
        for rotor in self.rotors_in_use:
            alphabet_length = len(self.available_rotors[rotor.type].permutation)
            if not utils.is_a_valid_position(rotor.starting_position, alphabet_length):
                raise utils.InvalidPosition(rotor.starting_position, alphabet_length)
        return self
            
    @pydantic.model_validator
    def check_turnover_notch(self) -> "Configuration":
        for rotor in self.rotors_in_use:
            alphabet_length = len(self.available_rotors[rotor.type].permutation)
            if not utils.is_a_valid_position(rotor.turnover_notch, alphabet_length):
                raise utils.InvalidPosition(rotor.turnover_notch, alphabet_length)
        return self

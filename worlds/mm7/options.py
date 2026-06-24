from dataclasses import dataclass
from Options import Range, Toggle, PerGameCommonOptions


class StartingLives(Range):
    """Number of lives Mega Man starts with."""
    display_name = "Starting Lives"
    range_start = 1
    range_end = 9
    default = 2


class StartingBolts(Range):
    """Number of bolts Mega Man starts with.
    Bolts are used to purchase items from Auto's shop."""
    display_name = "Starting Bolts"
    range_start = 0
    range_end = 999
    default = 0


class LogicBossWeakness(Toggle):
    """When enabled, each boss logically requires the player to have
    at least one of its weakness weapons before that boss location
    is considered accessible. This promotes weakness weapons from
    'useful' to 'progression' in the item pool."""
    display_name = "Boss Weakness Logic"
    default = 0


@dataclass
class MegaMan7Options(PerGameCommonOptions):
    starting_lives: StartingLives
    starting_bolts: StartingBolts
    logic_boss_weakness: LogicBossWeakness
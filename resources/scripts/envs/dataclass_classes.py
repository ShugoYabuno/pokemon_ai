from dataclasses import dataclass
from .enum_classes import Field


@dataclass
class Move:
    index: int
    name: str
    power: int
    accuracy: int
    pp: int
    category: int
    type: int
    effectivities: list[tuple[int, float]]


@dataclass
class Ability:
    index: int
    name: str
    name_en: str


@dataclass
class Stats:
    hp: int
    atk: int
    df: int
    sp_atk: int
    sp_df: int
    spd: int


@dataclass
class StatsRank:
    rank = -6 | -5 | -4 | -3 | -2 | -1 | 0 | 1 | 2 | 3 | 4 | 5 | 6
    three_times_rank = 0 | 1 | 2 | 3

    atk: rank
    df: rank
    sp_atk: rank
    sp_df: rank
    spd: rank
    evasion: rank
    critical: three_times_rank
    # stockpile: three_times_rank

    def __init__(self) -> None:
        self.atk = 0
        self.df = 0
        self.sp_atk = 0
        self.sp_df = 0
        self.sp_df = 0
        self.spd = 0
        self.critical = 0
        self.evasion = 0
        # self.stockpile = 0


@dataclass
class Information:
    moves: list[Move]


@dataclass
class FieldState:
    field: Field
    remaining_turn: int

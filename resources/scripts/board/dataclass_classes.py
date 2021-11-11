from dataclasses import dataclass


@dataclass
class Move:
    index: int
    name: str
    power: int
    accuracy: int
    pp: int
    category: int
    type: int
    compatibilities: list[tuple[int, float]]


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

    atk: rank
    df: rank
    sp_atk: rank
    sp_df: rank
    spd: rank

    def __init__(self) -> None:
        self.atk = 0
        self.df = 0
        self.sp_atk = 0
        self.sp_df = 0
        self.sp_df = 0
        self.spd = 0

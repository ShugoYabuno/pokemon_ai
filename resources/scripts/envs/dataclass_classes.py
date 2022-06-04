from dataclasses import dataclass
from .enum_classes import Field, Weather


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
    atk: int
    df: int
    sp_atk: int
    sp_df: int
    spd: int
    evasion: int
    critical: int
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

    def _truncate_over_6(self, rank: int):
        if rank > 6:
            return 6
        elif rank < -6:
            return -6
        else:
            return rank

    def add_atk(self, diff=0):
        atk = self.atk + diff
        self.atk = self._truncate_over_6(atk)

    def add_df(self, diff=0):
        df = self.df + diff
        self.df = self._truncate_over_6(df)

    def add_sp_atk(self, diff=0):
        sp_atk = self.sp_atk + diff
        self.sp_atk = self._truncate_over_6(sp_atk)

    def add_sp_df(self, diff=0):
        sp_df = self.sp_df + diff
        self.sp_df = self._truncate_over_6(sp_df)

    def add_spd(self, diff=0):
        spd = self.spd + diff
        self.spd = self._truncate_over_6(spd)


@dataclass
class Information:
    moves: list[Move]


@dataclass
class FieldState:
    field: Field
    remaining_turn: int

@dataclass
class WeatherState:
    weather: Weather
    remaining_turn: int

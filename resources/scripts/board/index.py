import json
from math import floor
from typing import Final
from dataclasses import dataclass
from .dataclass_classes import Stats, Move, StatsRank
from .enum_classes import StatusAilment

pokemons: Final = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))
moves: Final = json.load(
    open("./resources/data/original/poketetsu/moves.json", "r"))


def move_index_to_name(_index: int):
    return next(
        (_move["name"] for _move in moves if _move["index"] == _index), None)


def half_down(_number):
    if _number % 1 <= 0.5:
        return floor(_number)
    else:
        return int(_number + 0.5)


def json2move(_move: dict):
    return Move(_move["index"], _move["name"], _move["power"], _move["accuracy"],
                _move["pp"], _move["category"], _move["type"], _move["compatibilities"])


@dataclass
class Pokemon:
    name: str
    stats: Stats
    types: list[int]
    ragal_moves: list[int]
    usable_moves: list[Move]

    def __init__(self, _name, _effort={
        "h": 0,
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
        "s": 0
    }, _correction="", _level=50):
        self.name = _name
        pokemon = next(
            (_pokemon for _pokemon in pokemons if _pokemon["name"] == _name), None)

        correction_atk = 1.0
        correction_df = 1.0
        correction_sp_atk = 1.0
        correction_sp_df = 1.0
        correction_spd = 1.0
        if _correction == "A":
            correction_atk = 1.1
        elif _correction == "B":
            correction_df = 1.1
        elif _correction == "C":
            correction_sp_atk = 1.1
        elif _correction == "D":
            correction_sp_df = 1.1
        elif _correction == "S":
            correction_spd = 1.1

        base_stats = pokemon["base_stats"]
        effort_h = _effort["h"] if _effort.get("h", None) else 0
        effort_a = _effort["a"] if _effort.get("a", None) else 0
        effort_b = _effort["b"] if _effort.get("b", None) else 0
        effort_c = _effort["c"] if _effort.get("c", None) else 0
        effort_d = _effort["d"] if _effort.get("d", None) else 0
        effort_s = _effort["s"] if _effort.get("s", None) else 0
        hp = self._calculate_hp(base_stats["hp"], effort_h)
        atk = self._calculate_stats(
            base_stats["atk"], effort_a, correction_atk)
        df = self._calculate_stats(
            base_stats["df"], effort_b, correction_df)
        sp_atk = self._calculate_stats(
            base_stats["sp_atk"], effort_c, correction_sp_atk)
        sp_df = self._calculate_stats(
            base_stats["sp_df"], effort_d, correction_sp_df)
        spd = self._calculate_stats(
            base_stats["spd"], effort_s, correction_spd)
        self.stats = Stats(hp, atk, df, sp_atk, sp_df, spd)
        self.ragal_moves = pokemon["moves"]
        self.usable_moves = []
        self.types = pokemon["types"]

    def _calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
        return floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

    def _calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
        return floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)

    # def _inject_moves(self, _move_indices: list[int]):
    #     move_classes = []

    #     for _move_index in _move_indices:
    #         move = next(
    #             (_move for _move in moves if _move["index"] == _move_index), None)

    #         if move:
    #             move = json2move(move)
    #             move_classes.append(move)

    #     return move_classes

    def set_move(self, _name: str):
        move = next(
            (_move for _move in moves if _move["name"] == _name), None)
        if move is None:
            return

        self.usable_moves.append(json2move(move))


class PokemonState:
    pokemon: Pokemon
    max_hp: int
    remaining_hp: int
    stats: Stats
    types: list[int]
    stats_rank: StatsRank
    status_ailments: list[StatusAilment]

    def __init__(self, _pokemon: Pokemon) -> None:
        self.pokemon = _pokemon
        self.max_hp = _pokemon.stats.hp
        self.remaining_hp = _pokemon.stats.hp
        self.stats = _pokemon.stats
        self.types = _pokemon.types
        self.stats_rank = StatsRank()
        self.status_ailments = []


class PokemonList:
    def __init__(self, _name, _level=50):
        self.name = _name

        pokemon_patterns = [
            ["ASh", "A"],
            ["ASh", "S"],
            ["CSh", "C"],
            ["CSh", "S"],
            ["HAs", "A"],
            ["HBs", "B"],
            ["HCs", "C"],
            ["HDs", "D"],
            ["HDs", "D"],
            ["HS", "S"]
        ]

        pokemons = []

        for _pattern in pokemon_patterns:
            effort_hp = 0
            effort_atk = 0
            effort_df = 0
            effort_sp_atk = 0
            effort_sp_df = 0
            effort_spd = 0
            for _stats in _pattern[0]:
                if _stats == "h":
                    effort_hp = 4
                elif _stats == "a":
                    effort_atk = 4
                elif _stats == "b":
                    effort_df = 4
                elif _stats == "c":
                    effort_sp_atk = 4
                elif _stats == "d":
                    effort_sp_df = 4
                elif _stats == "s":
                    effort_spd = 4
                elif _stats == "H":
                    effort_hp = 252
                elif _stats == "A":
                    effort_atk = 252
                elif _stats == "B":
                    effort_df = 252
                elif _stats == "C":
                    effort_sp_atk = 252
                elif _stats == "D":
                    effort_sp_df = 252
                elif _stats == "S":
                    effort_spd = 252

            pokemons.append(Pokemon(_name, {
                "h": effort_hp,
                "a": effort_atk,
                "b": effort_df,
                "c": effort_sp_atk,
                "d": effort_sp_df,
                "s": effort_spd,
            }, _pattern[1]))
        self.pokemon_list = pokemons


@dataclass
class SingleMatchBoard:
    ally: PokemonState
    enemy: PokemonState
    ally_moves: list[Move]
    enemy_moves: list[Move]
    ally_confirmed_moves: list[Move]
    enemy_confirmed_moves: list[Move]

    def __init__(self, _ally: Pokemon, _enemy: Pokemon) -> None:
        self.ally = PokemonState(_ally)
        self.enemy = PokemonState(_enemy)
        self.ally_moves = []
        self.enemy_moves = []
        self.ally_confirmed_moves = []
        self.enemy_confirmed_moves = []

    def calc_ally_moves(self):
        self.ally_moves = self._calc_moves(self.ally, self.enemy)

        for _move in self.ally_moves:
            print(f'{move_index_to_name(_move["index"])}: {_move["damage"]}')

    def calc_enemy_moves(self):
        self.enemy_moves = self._calc_moves(self.enemy, self.ally)

        for _move in self.enemy_moves:
            print(f'{move_index_to_name(_move["index"])}: {_move["damage"]}')

    def set_move(self, _name: str, _player=0):
        move = next(
            (_move for _move in moves if _move["name"] == _name), None)
        if move is None:
            return

        if _player == 0 and len(self.ally_confirmed_moves) <= 3:
            self.ally_confirmed_moves.append(json2move(move))
        elif _player == 1 and len(self.ally_confirmed_moves) <= 3:
            self.enemy_confirmed_moves.append(json2move(move))

    def _calc_moves(self, _self: PokemonState, _target: PokemonState):
        calculated_moves = []
        for _move in _self.pokemon.moves:
            damage = self._calc_damage(_self, _target, _move)

            calculated_moves.append({
                "index": _move.index,
                "damage": damage
            })

        return sorted(
            calculated_moves, key=lambda x: x["damage"], reverse=True)

    def _calc_compatibility_ratio(self, _compatibilities: list[tuple[int, float]], _enemy_types: list[int]) -> float:
        compatibility_ratio = 1.00
        for _compatibility in _compatibilities:
            if _compatibility[0] in _enemy_types:
                compatibility_ratio = compatibility_ratio * \
                    _compatibility[1]

        return compatibility_ratio

    def _calc_damage(self, _self: PokemonState, _target: PokemonState, _move: Move):
        if _move.category == 0:
            return 0

        level = 50
        range_ratio = 1
        parental_bond_ratio = 1
        whether_ratio = 1
        critical_ratio = 1
        random_ratio = 1
        type_match_ratio = 1.5 if _move.type in _self.pokemon.types else 1
        compatibility_ratio = self._calc_compatibility_ratio(
            _move.compatibilities, _target.pokemon.types)
        burn_ratio = 1
        m = 1
        m_protect = 1
        atk = _self.pokemon.stats.atk if _move.category == 1 else _self.pokemon.stats.sp_atk
        df = _target.pokemon.stats.df if _move.category == 1 else _target.pokemon.stats.sp_df

        step1 = floor(floor(level * 2 / 5 + 2) * _move.power * atk / df)
        step2 = floor(step1 / 50 + 2)
        step3 = half_down(step2 * range_ratio)
        step4 = half_down(step3 * parental_bond_ratio)
        step5 = half_down(step4 * whether_ratio)
        step6 = half_down(step5 * critical_ratio)
        step7 = floor(step6 * random_ratio)
        step8 = half_down(step7 * type_match_ratio)
        step9 = floor(step8 * compatibility_ratio)
        step10 = half_down(step9 * burn_ratio)
        step11 = half_down(step10 * m)
        damage = half_down(step11 * m_protect)

        return damage

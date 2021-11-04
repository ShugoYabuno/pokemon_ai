import json
import math
# import re

pokemons = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))
moves = json.load(
    open("./resources/data/original/poketetsu/moves.json", "r"))


class Pokemon:
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
        hp = self._calculate_hp(base_stats["hp"], _effort["h"])
        atk = self._calculate_stats(
            base_stats["atk"], _effort["a"], correction_atk)
        df = self._calculate_stats(
            base_stats["df"], _effort["b"], correction_df)
        sp_atk = self._calculate_stats(
            base_stats["sp_atk"], _effort["c"], correction_sp_atk)
        sp_df = self._calculate_stats(
            base_stats["sp_df"], _effort["d"], correction_sp_df)
        spd = self._calculate_stats(
            base_stats["spd"], _effort["s"], correction_spd)
        self.stats = [hp, atk, df, sp_atk, sp_df, spd]
        self.moves = [self._get_move(_index) for _index in pokemon["moves"]]
        self.types = pokemon["types"]

    def _calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
        return math.floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

    def _calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
        return math.floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)

    def get_stats(self):
        return self.stats

    def get_moves(self):
        return self.moves

    def get_types(self):
        return self.types

    def _get_move(self, _index):
        return next(
            (_move for _move in moves if _move["index"] == _index), None)


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

    def info(self):
        for _pokemon in self.pokemon_list:
            print(_pokemon.get_moves())


effort = {
    "h": 4,
    "a": 252,
    "b": 0,
    "c": 0,
    "d": 0,
    "s": 252,
}
garchomp = Pokemon("ガブリアス", effort, "S")
tyranitar = Pokemon("バンギラス", effort, "S")


class Match:
    ally: Pokemon
    enemy: Pokemon

    def __init__(self, _ally: Pokemon, _enemy: Pokemon) -> None:
        self.ally = _ally
        self.enemy = _enemy

    def categorize_moves(self):
        moves = self.ally.get_moves()
        enemy_types = self.enemy.get_types()

        # move_powers = []
        status_moves = []
        atk_moves = []
        sp_atk_moves = []
        for _move in moves:
            compatibilities = _move["compatibilities"]
            compatibility_ratio = None
            if _move["category"] != 0:
                compatibility_ratio = 1
                for _compatibility in compatibilities:
                    if _compatibility[0] in enemy_types:
                        compatibility_ratio = compatibility_ratio * \
                            _compatibility[1]

            print(f"{_move['name']}: {compatibility_ratio}倍")


match = Match(garchomp, tyranitar)
match.categorize_moves()

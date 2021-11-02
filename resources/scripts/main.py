import json
import math
import re

pokemons = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))


class Pokemon:
    def __init__(self, _name, _pattern=["", ""], _level=50):
        self.name = _name
        pokemon = next(
            (_pokemon for _pokemon in pokemons if _pokemon["name"] == _name), None)

        effort_hp = 0
        effort_atk = 0
        effort_df = 0
        effort_sp_atk = 0
        effort_sp_df = 0
        effort_spd = 0
        for e in _pattern[0]:
            if e == "h":
                effort_hp = 4
            elif e == "a":
                effort_atk = 4
            elif e == "b":
                effort_df = 4
            elif e == "c":
                effort_sp_atk = 4
            elif e == "d":
                effort_sp_df = 4
            elif e == "s":
                effort_spd = 4
            elif e == "H":
                effort_hp = 252
            elif e == "A":
                effort_atk = 252
            elif e == "B":
                effort_df = 252
            elif e == "C":
                effort_sp_atk = 252
            elif e == "D":
                effort_sp_df = 252
            elif e == "S":
                effort_spd = 252

        correction_atk = 1.0
        correction_df = 1.0
        correction_sp_atk = 1.0
        correction_sp_df = 1.0
        correction_spd = 1.0
        if _pattern[1] == "A":
            correction_atk = 1.1
        elif _pattern[1] == "B":
            correction_df = 1.1
        elif _pattern[1] == "C":
            correction_sp_atk = 1.1
        elif _pattern[1] == "D":
            correction_sp_df = 1.1
        elif _pattern[1] == "S":
            correction_spd = 1.1

        def calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
            return math.floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

        def calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
            return math.floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)

        base_stats = pokemon["base_stats"]
        hp = calculate_hp(base_stats["hp"], effort_hp)
        atk = calculate_stats(base_stats["atk"], effort_atk, correction_atk)
        df = calculate_stats(base_stats["df"], effort_df, correction_df)
        sp_atk = calculate_stats(
            base_stats["sp_atk"], effort_sp_atk, correction_sp_atk)
        sp_df = calculate_stats(
            base_stats["sp_df"], effort_sp_df, correction_sp_df)
        spd = calculate_stats(base_stats["spd"], effort_spd, correction_spd)
        self.base_stats = [hp, atk, df, sp_atk, sp_df, spd]
        self.moves = pokemon["moves"]


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
            pokemons.append(Pokemon(_name, _pattern))
        self.pokemon_list = pokemons

    def info(self):
        print(self.pokemon_list)


garchomp = PokemonList("ガブリアス")
garchomp.info()

import json
import math

pokemons = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))


class Pokemon:
    def __calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
        return math.floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

    def __calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
        return math.floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)

    def __init__(self, _name, _level=50):
        self.name = _name
        pokemon = next(
            (_pokemon for _pokemon in pokemons if _pokemon["name"] == _name), None)

        # ASh

        effort_hp = 4
        effort_atk = 252
        effort_spd = 252

        base_stats = pokemon["base_stats"]
        hp = self.__calculate_hp(base_stats["hp"], effort_hp)
        atk = self.__calculate_stats(base_stats["atk"], effort_atk)
        df = self.__calculate_stats(base_stats["df"])
        sp_atk = self.__calculate_stats(base_stats["sp_atk"], 0.9)
        sp_df = self.__calculate_stats(base_stats["sp_df"])
        spd = self.__calculate_stats(base_stats["spd"], effort_spd, 1.1)
        self.base_stats = [hp, atk, df, sp_atk, sp_df, spd]
        self.moves = pokemon["moves"]

    def info(self):
        print(self.name)
        print(self.base_stats)
        # print(self.moves)


garchomp = Pokemon("ガブリアス")
garchomp.info()
tyranitar = Pokemon("バンギラス")
tyranitar.info()

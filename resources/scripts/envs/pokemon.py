import json
from math import floor
from typing import Final
from dataclasses import dataclass
from .dataclass_classes import Stats, Move, StatsRank
from .enum_classes import StatusAilment, SingleBattleActions, switch_pokemon_actions, move_actions
# from random import shuffle

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


@dataclass
class PokemonState:
    pokemon: Pokemon
    max_hp: int
    remaining_hp: int
    stats: Stats
    types: list[int]
    stats_rank: StatsRank
    eternal_status_ailments: list[StatusAilment]
    temporary_status_ailments: list[StatusAilment]

    def __init__(self, _pokemon: Pokemon) -> None:
        self.pokemon = _pokemon
        self.max_hp = _pokemon.stats.hp
        self.remaining_hp = _pokemon.stats.hp
        self.eternal_status_ailments = []
        self.initialize()

    def initialize(self):
        self.stats = self.pokemon.stats
        self.types = self.pokemon.types
        self.temporary_status_ailments = []
        self.stats_rank = StatsRank()

    def get_speed(self):
        return self.pokemon.stats.spd

    def receive_damage(self, _damage: int):
        calced = self.remaining_hp - _damage
        self.remaining_hp = calced if calced > 0 else 0

    def is_fainted(self):
        return self.remaining_hp == 0


@dataclass
class Information:
    moves: list[Move]


action = 0 | 1 | 2 | 3 | 4 | 5


@dataclass
class SingleBattle:
    parties: list[tuple[PokemonState, PokemonState, PokemonState]]
    playing_pokemons: list[int, int]
    information: tuple[Information, Information]
    actions: list[SingleBattleActions, SingleBattleActions]

    def __init__(self, _party0: list[tuple[Pokemon, Pokemon, Pokemon]], _party1: tuple[Pokemon, Pokemon, Pokemon]) -> None:
        self.parties = [self._pokemons_to_states(_party0),
                        self._pokemons_to_states(_party1)]
        self.playing_pokemons = [0, 0]
        self.information = ((), ())
        self._initialize_actions()

    def set_action(self, _player: 0 | 1, _action: SingleBattleActions):
        self.actions[_player] = _action

    def advance_turn(self):
        if None in self.actions:
            raise ValueError("actions includes None")

        if self.actions[0] in switch_pokemon_actions or self.actions[1] in switch_pokemon_actions:
            # if self.playing_pokemons[0].get_speed() == self.playing_pokemons[1].get_speed():
            #     sorted_players = shuffle([0, 1])

            for _player in self._sorted_players():
                if self.actions[_player] in switch_pokemon_actions:
                    self._playing_pokemon_state(_player).initialize()
                    self._switch_pokemon(_player, self.actions[_player])

        if self.actions[0] in move_actions or self.actions[1] in move_actions:
            for _player in self._sorted_players():
                if self.actions[_player] in move_actions:
                    player_pokemon_state = self._playing_pokemon_state(_player)
                    # プレイヤーのポケモンが瀕死の場合処理しない
                    if player_pokemon_state.is_fainted():
                        continue

                    target_pokemon_state = self._playing_pokemon_state(
                        self._target_player(_player))
                    move = player_pokemon_state.pokemon.usable_moves[self.actions[_player]]
                    damage = self._calc_damage(
                        player_pokemon_state, target_pokemon_state, move)
                    target_pokemon_state.receive_damage(damage)
                    print(
                        f"{player_pokemon_state.pokemon.name} -> {target_pokemon_state.pokemon.name}")
                    print(f"{move.name} {damage}ダメージ")

        self._initialize_actions()

    def info(self):
        print("player0")
        print(f"{self._playing_pokemon_state(0).pokemon.name}")
        print(
            f"{self._playing_pokemon_state(0).remaining_hp} / {self._playing_pokemon_state(0).max_hp}")
        print("player1")
        print(f"{self._playing_pokemon_state(1).pokemon.name}")
        print(
            f"{self._playing_pokemon_state(1).remaining_hp} / {self._playing_pokemon_state(1).max_hp}")

    def _pokemons_to_states(self, _list: tuple[Pokemon, Pokemon, Pokemon]):
        return [PokemonState(_pokemon) for _pokemon in _list]

    def _switch_pokemon(self, _player: 0 | 1, _action: 5 | 6 | 7):
        parties_index = _action - 5

        self.playing_pokemons[_player] = parties_index

    def _target_player(self, _player: 0 | 1):
        if _player == 0:
            return 1
        else:
            return 0

    def _sorted_players(self):
        return sorted(
            [0, 1], key=lambda x: self._playing_pokemon_state(x).get_speed(), reverse=True)

    def _initialize_actions(self):
        self.actions = [None, None]

    def _playing_pokemon_state(self, _player: 0 | 1):
        return self.parties[_player][self.playing_pokemons[_player]]

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

        # for _player in self._sorted_players():
        #     if self.actions[_player] in [5, 6]:
        # if playler_0_speed > playler_1_speed:
        #     self._calc_damage(self.playing_pokemons[0], self.playing_pokemons[1])

        # def calc_ally_moves(self):
        #     self.ally_moves = self._calc_moves(self.ally, self.enemy)

        #     for _move in self.ally_moves:
        #         print(f'{move_index_to_name(_move["index"])}: {_move["damage"]}')

        # def calc_enemy_moves(self):
        #     self.enemy_moves = self._calc_moves(self.enemy, self.ally)

        #     for _move in self.enemy_moves:
        #         print(f'{move_index_to_name(_move["index"])}: {_move["damage"]}')

        # def set_move(self, _name: str, _player=0):
        #     move = next(
        #         (_move for _move in moves if _move["name"] == _name), None)
        #     if move is None:
        #         return

        #     if _player == 0 and len(self.ally_confirmed_moves) <= 3:
        #         self.ally_confirmed_moves.append(json2move(move))
        #     elif _player == 1 and len(self.ally_confirmed_moves) <= 3:
        #         self.enemy_confirmed_moves.append(json2move(move))

        # def _calc_moves(self, _self: PokemonState, _target: PokemonState):
        #     calculated_moves = []
        #     for _move in _self.pokemon.moves:
        #         damage = self._calc_damage(_self, _target, _move)

        #         calculated_moves.append({
        #             "index": _move.index,
        #             "damage": damage
        #         })

        #     return sorted(
        #         calculated_moves, key=lambda x: x["damage"], reverse=True)

    def _calc_compatibility_ratio(self, _compatibilities: list[tuple[int, float]], _enemy_types: list[int]) -> float:
        compatibility_ratio = 1.00
        for _compatibility in _compatibilities:
            if _compatibility[0] in _enemy_types:
                compatibility_ratio = compatibility_ratio * \
                    _compatibility[1]

        return compatibility_ratio

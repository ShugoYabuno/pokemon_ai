import json
from math import floor
from typing import Final
from dataclasses import dataclass, field
from .dataclass_classes import Stats, Move, StatsRank
from .enum_classes import StatusAilment, Field
# from random import shuffle

pokemons: Final = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))
moves: Final = json.load(
    open("./resources/data/original/poketetsu/moves.json", "r"))
abilities: Final = json.load(
    open("./resources/data/original/poketetsu/abilities.json", "r"))


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
class Ability:
    index: int
    name: str
    name_en: str


@dataclass
class BaseInfo:
    stats: Stats
    types: list[int]
    regal_abilities: list[Ability]
    regal_moves: list[Move]

    def __init__(self, _name: str, _effort: dict, _correction: str, _level=50):
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

        self.regal_moves = []
        for i in pokemon["moves"]:
            move = next(
                (_move for _move in moves if _move["index"] == i), None)
            if move is not None:
                self.regal_moves.append(json2move(move))

        self.types = pokemon["types"]

        self.regal_abilities = []
        for i in pokemon["abilities"]:
            ability = next(
                (_ability for _ability in abilities if _ability["index"] == i), None)
            if ability is None:
                continue

            self.regal_abilities.append(Ability(
                ability["index"], ability["name"], ability["name_en"]))

    def _calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
        return floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

    def _calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
        return floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)


@dataclass
class PokemonState:
    name: str
    base_info: BaseInfo
    max_hp: int
    remaining_hp: int
    stats: Stats
    types: list[int]
    stats_rank: StatsRank
    usable_move_indices: list[int]
    usable_ability_index: int
    eternal_status_ailments: list[StatusAilment]
    temporary_status_ailments: list[StatusAilment]

    def __init__(self, _name: str, _effort: dict, _correction: str) -> None:
        self.name = _name
        base_info = BaseInfo(_name, _effort, _correction)
        self.base_info = base_info
        self.max_hp = base_info.stats.hp
        self.remaining_hp = base_info.stats.hp
        self.eternal_status_ailments = []
        self.usable_move_indices = []
        self.usable_ability_index = None
        self.initialize()

    def initialize(self):
        self.stats = self.base_info.stats
        self.types = self.base_info.types
        self.temporary_status_ailments = []
        self.stats_rank = StatsRank()

    def get_speed(self):
        return self.base_info.stats.spd

    def receive_damage(self, _damage: int):
        calced = self.remaining_hp - _damage
        self.remaining_hp = calced if calced > 0 else 0

    def is_fainted(self):
        return self.remaining_hp == 0

    def set_ability(self, _ability_name):
        self.usable_ability_index = next(
            (i for i, a in enumerate(self.base_info.regal_abilities) if a.name == _ability_name), None)

    def set_move(self, _move_name):
        index = next(
            (i for i, m in enumerate(self.base_info.regal_moves) if m.name == _move_name), None)
        if index is not None:
            self.usable_move_indices.append(index)

    def get_ability_name_en(self):
        if self.usable_ability_index is None:
            return "unknown"
        else:
            return self.base_info.regal_abilities[self.usable_ability_index].name_en

    def get_usable_move(self, _index: 0 | 1 | 2 | 3):
        return self.base_info.regal_moves[self.usable_move_indices[_index]]


@dataclass
class Information:
    moves: list[Move]


action = 0 | 1 | 2 | 3 | 4 | 5


@dataclass
class FieldState:
    field: Field
    remaining_turn: int


@dataclass
class SingleBattle:
    parties: list[tuple[PokemonState, PokemonState, PokemonState]]
    playing_pokemons: list[int, int]
    information: tuple[Information, Information]
    actions: list[int, int]
    field_state: FieldState

    move_actions = range(3)
    switch_pokemon_actions = range(4, 6)

    def __init__(self, _party0: list[tuple[PokemonState, PokemonState, PokemonState]], _party1: tuple[PokemonState, PokemonState, PokemonState]) -> None:
        self.parties = [_party0,
                        _party1]
        self.playing_pokemons = [0, 0]
        self.information = ((), ())
        self.field_state = None
        self._initialize_actions()

        # 登場時に発動する特性の処理
        players_spd_desc = self._get_players_spd_desc()

        for _player in players_spd_desc:
            s = self._playing_pokemon_state(_player)
            self._fanfare(s)

    def set_action(self, _player: 0 | 1, _action: int):
        self.actions[_player] = _action

    def advance_turn(self):
        if None in self.actions:
            raise ValueError("actions includes None")

        # S順に並び替え
        players_spd_desc = self._get_players_spd_desc()

        # ポケモンの交代処理
        if self.actions[0] in self.switch_pokemon_actions or self.actions[1] in self.switch_pokemon_actions:
            # if self.playing_pokemons[0].get_speed() == self.playing_pokemons[1].get_speed():
            #     sorted_players = shuffle([0, 1])

            for _player in players_spd_desc:
                if self.actions[_player] in self.switch_pokemon_actions:
                    self._playing_pokemon_state(_player).initialize()
                    self._switch_pokemon(_player, self.actions[_player])

        # ポケモンの攻撃処理
        if self.actions[0] in self.move_actions or self.actions[1] in self.move_actions:
            for _player in players_spd_desc:
                if self.actions[_player] in self.move_actions:
                    player_pokemon_state = self._playing_pokemon_state(_player)
                    # 攻撃プレイヤーのポケモンが瀕死の場合処理しない
                    if player_pokemon_state.is_fainted():
                        continue

                    # ダメージ処理
                    target_plaer = 1 if _player == 0 else 0
                    target_pokemon_state = self._playing_pokemon_state(
                        target_plaer)
                    move = player_pokemon_state.get_usable_move(
                        self.actions[_player])
                    damage = self._calc_damage(
                        player_pokemon_state, target_pokemon_state, move)
                    target_pokemon_state.receive_damage(damage)
                    print(
                        f"{player_pokemon_state.name} -> {target_pokemon_state.name}")
                    print(f"{move.name} {damage}ダメージ")

        # アクションの初期化
        self._initialize_actions()

    def info(self):
        print("player0")
        print(f"{self._playing_pokemon_state(0).name}")
        print(
            f"{self._playing_pokemon_state(0).remaining_hp} / {self._playing_pokemon_state(0).max_hp}")
        print("player1")
        print(f"{self._playing_pokemon_state(1).name}")
        print(
            f"{self._playing_pokemon_state(1).remaining_hp} / {self._playing_pokemon_state(1).max_hp}")
        if self.field_state:
            print(f"フィールド: {self.field_state.field}")

    def _fanfare(self, _pokemon_state: PokemonState):
        ability = _pokemon_state.get_ability_name_en()
        if ability == "electric_surge":
            self.field_state = FieldState(Field.electric, 5)
        elif ability == "psychic_surge":
            self.field_state = FieldState(Field.psychic, 5)
        elif ability == "grassy_surge":
            self.field_state = FieldState(Field.grass, 5)
        elif ability == "misty_surge":
            self.field_state = FieldState(Field.mist, 5)

    def _get_players_spd_desc(self):
        return sorted(
            [0, 1], key=lambda x: self._playing_pokemon_state(x).get_speed(), reverse=True)

    def _switch_pokemon(self, _player: 0 | 1, _action: 4 | 5 | 6):
        parties_index = _action - 5

        self.playing_pokemons[_player] = parties_index

    def _playing_pokemon_state(self, _player: 0 | 1):
        return self.parties[_player][self.playing_pokemons[_player]]

    def _initialize_actions(self):
        self.actions = [None, None]

    def _calc_damage(self, _self: PokemonState, _target: PokemonState, _move: Move):
        def calc_compatibility_ratio(_compatibilities: list[tuple[int, float]], _enemy_types: list[int]) -> float:
            compatibility_ratio = 1.00
            for _compatibility in _compatibilities:
                if _compatibility[0] in _enemy_types:
                    compatibility_ratio = compatibility_ratio * \
                        _compatibility[1]

            return compatibility_ratio

        if _move.category == 0:
            return 0

        level = 50
        range_ratio = 1
        parental_bond_ratio = 1
        whether_ratio = 1
        critical_ratio = 1
        random_ratio = 1
        type_match_ratio = 1.5 if _move.type in _self.base_info.types else 1
        compatibility_ratio = calc_compatibility_ratio(
            _move.compatibilities, _target.base_info.types)
        burn_ratio = 1
        m = 1
        m_protect = 1
        atk = _self.base_info.stats.atk if _move.category == 1 else _self.base_info.stats.sp_atk
        df = _target.base_info.stats.df if _move.category == 1 else _target.base_info.stats.sp_df

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

import json
from math import floor
from typing import Final, Literal
from dataclasses import dataclass
from .dataclass_classes import Stats, Move, StatsRank, Ability, Information, FieldState, WeatherState
from .enum_classes import StatusAilment, Field, Type, Weather
from decimal import Decimal, ROUND_HALF_UP
from os import path


def relative_path(file_path: str):
    return path.join(path.dirname(__file__), file_path)


pokemons: Final = json.load(
    open(relative_path("../../data/original/poketetsu/pokemons.json"), "r"))
moves: Final = json.load(
    open(relative_path("../../data/original/poketetsu/moves.json"), "r"))
abilities: Final = json.load(
    open(relative_path("../../data/original/poketetsu/abilities.json"), "r"))


def move_index_to_name(_index: int):
    return next(
        (_move["name"] for _move in moves if _move["index"] == _index), None)


def half_down(_number: float):
    if _number % 1 <= 0.5:
        return floor(_number)
    else:
        return int(_number + 0.5)


def half_up(_number: float):
    return Decimal(_number).quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def json2move(_move: dict):
    return Move(_move["index"], _move["name"], _move["power"], _move["accuracy"],
                _move["pp"], _move["category"], _move["type"], _move["effectivities"])


def some(l1: list, l2: list):
    for i in l1:
        if i in l2:
            return True

    return False


@dataclass
class PokemonBaseInfo:
    stats: Stats
    types: list[int]
    regal_abilities: list[Ability]
    regal_moves: list[Move]
    usable_ability_index: int

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
        if len(self.regal_abilities) == 1:
            self.usable_ability_index = 0
        else:
            self.usable_ability_index = None

    def _calculate_hp(self, _base_stats, _effort=0, _individual=31, _level=50):
        return floor((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + _level + 10)

    def _calculate_stats(self, _base_stats, _effort=0, _correction=1.0, _individual=31, _level=50):
        return floor(((_base_stats * 2 + _individual + _effort / 4) * _level / 100 + 5) * _correction)

    def set_ability(self, _ability_name):
        self.usable_ability_index = next(
            (i for i, a in enumerate(self.regal_abilities) if a.name == _ability_name), None)

    def get_ability(self):
        if self.usable_ability_index is None:
            return None
        else:
            return self.regal_abilities[self.usable_ability_index]

    def get_stats(self):
        return self.stats


@dataclass
class PokemonState:
    name: str
    base_info: PokemonBaseInfo
    max_hp: int
    remaining_hp: int
    stats: Stats
    types: list[int]
    stats_rank: StatsRank
    usable_move_indices: list[int]
    ability: Ability
    eternal_status_ailments: list[StatusAilment]
    temporary_status_ailments: list[StatusAilment]

    def __init__(self, name: str, effort={}, correction="") -> None:
        self.name = name
        base_info = PokemonBaseInfo(name, effort, correction)
        self.base_info = base_info
        self.max_hp = base_info.stats.hp
        self.remaining_hp = base_info.stats.hp
        self.eternal_status_ailments = []
        self.usable_move_indices = []
        self._initialize_ability()
        self.initialize()

    def initialize(self):
        self.stats = self.base_info.stats
        self.types = self.base_info.types
        self.temporary_status_ailments = []
        self.stats_rank = StatsRank()

    def _calc_rank(self, base_stats: int, rank: int):
        return floor(((max(rank, 0) + 2) / (-min(rank, 0) + 2)) * base_stats)

    def get_atk(self):
        return self._calc_rank(self.stats.atk, self.stats_rank.atk)

    def get_df(self):
        return self._calc_rank(self.stats.df, self.stats_rank.df)

    def get_sp_atk(self):
        return self._calc_rank(self.stats.sp_atk, self.stats_rank.sp_atk)

    def get_sp_df(self):
        return self._calc_rank(self.stats.sp_df, self.stats_rank.sp_df)

    def get_spd(self):
        return self._calc_rank(self.stats.spd, self.stats_rank.spd)

    def receive_damage(self, _damage: int):
        calced = self.remaining_hp - _damage
        self.remaining_hp = calced if calced > 0 else 0

    def is_fainted(self):
        return self.remaining_hp == 0

    def _initialize_ability(self):
        self.ability = self.base_info.get_ability()

    def set_ability(self, _ability_name):
        self.base_info.set_ability(_ability_name)
        self.ability = self.base_info.get_ability()

    def set_move(self, _move_name):
        index = next(
            (i for i, m in enumerate(self.base_info.regal_moves) if m.name == _move_name), None)
        if index is not None:
            self.usable_move_indices.append(index)

    def get_ability_name_en(self):
        ability = self.base_info.get_ability()
        if ability is None:
            return "unknown"
        else:
            return ability.name_en

    def get_usable_move(self, _index: 0 | 1 | 2 | 3):
        return self.base_info.regal_moves[self.usable_move_indices[_index]]

    def get_regal_moves(self):
        return self.base_info.regal_moves

    def update_stats_rank(self, atk=0, df=0, sp_atk=0, sp_df=0, spd=0):
        if atk:
            self.stats_rank.add_atk(atk)
        if df:
            self.stats_rank.add_df(df)
        if sp_atk:
            self.stats_rank.add_sp_atk(sp_atk)
        if sp_df:
            self.stats_rank.add_sp_df(sp_df)
        if spd:
            self.stats_rank.add_spd(spd)

    def get_stats(self):
        print(self.stats_rank)
        return {
            "atk": self.get_atk(),
            "df": self.get_df(),
            "sp_atk": self.get_sp_atk(),
            "sp_df": self.get_sp_df(),
            "spd": self.get_spd()
        }

def equal_ability(pokemon_state: PokemonState, ability_name: str):
    return pokemon_state.get_ability_name_en() == ability_name

@dataclass
class SingleBattle:
    parties: list[list[PokemonState]]
    playing_pokemons: list[int, int]
    information: tuple[Information, Information]
    actions: list[int, int]
    weather_state: WeatherState
    field_state: FieldState

    move_actions = list(range(4))
    switch_pokemon_actions = list(range(4, 7))
    PlayerIndexes = [0, 1]
    Player = Literal[0, 1]
    MoveActions = Literal[0, 1, 2, 3]
    SwitchPokemonActions = Literal[0, 1, 2, 3]

    def __init__(self, _party0: list[PokemonState], _party1: list[PokemonState]) -> None:
        self.parties = [_party0,
                        _party1]
        self.playing_pokemons = [0, 0]
        self.information = ((), ())
        self.weather_state = None
        self.field_state = None
        self._initialize_actions()

        # 登場時に発動する特性の処理
        players_spd_desc = self._get_players_spd_desc()

        for _player in players_spd_desc:
            s = self._get_playing_pokemon_state(_player)
            self._fanfare(s)

    def set_action(self, _player: Player, _action: MoveActions):
        self.actions[_player] = _action

    def advance_turn(self):
        if None in self.actions:
            raise ValueError("actions includes None")

        # S順に並び替え
        players_spd_desc = self._get_players_spd_desc()

        # ポケモンの交代処理
        if some(self.actions, self.switch_pokemon_actions):
            for _player in players_spd_desc:
                if self.actions[_player] in self.switch_pokemon_actions:
                    self._get_playing_pokemon_state(_player).initialize()
                    self._switch_pokemon(_player, self.actions[_player])

        # ポケモンの攻撃処理
        if some(self.actions, self.move_actions):
            for _player in players_spd_desc:
                if self.actions[_player] in self.move_actions:
                    player_pokemon_state = self._get_playing_pokemon_state(
                        _player)
                    # 攻撃プレイヤーのポケモンが瀕死の場合処理しない
                    if player_pokemon_state.is_fainted():
                        continue

                    self._active_ability_when_move(
                        _player, player_pokemon_state)

                    # ダメージ処理
                    target_player = self._get_target_player(_player)
                    target_pokemon_state = self._get_playing_pokemon_state(
                        target_player)
                    move = self._get_this_turn_move(_player)
                    damage = self._calc_damage(_player, target_player)
                    target_pokemon_state.receive_damage(damage)
                    print(
                        f"{player_pokemon_state.name} -> {target_pokemon_state.name}")
                    print(f"{move.name} {damage}ダメージ")

        # ポケモンが瀕死になっていた場合の交代処理
        for player in [0, 1]:
            if self._get_playing_pokemon_state(player).is_fainted():
                print(f"player{player} 誰に交代しますか？")
                for (index, pokemon) in enumerate(self.parties[player]):
                    if pokemon.is_fainted() is False:
                        print(f"{pokemon.name}: {index}")
                parties_index = int(input("半角数字を入力: "))

                self._switch_pokemon(player, parties_index + 4)

        # アクションの初期化
        self._initialize_actions()

    def info(self, stats=False):
        print("player0")
        print(self._get_playing_pokemon_state(0).name)
        print(
            f"{self._get_playing_pokemon_state(0).remaining_hp} / {self._get_playing_pokemon_state(0).max_hp}")
        print("player1")
        print(self._get_playing_pokemon_state(1).name)

        print(
            f"{self._get_playing_pokemon_state(1).remaining_hp} / {self._get_playing_pokemon_state(1).max_hp}")
        if self.weather_state:
            print(f"天候: {self.weather_state.weather}")
        if self.field_state:
            print(f"フィールド: {self.field_state.field}")

        if stats:
            for i in [0, 1]:
                ps = self._get_playing_pokemon_state(i)
                print("--------------------")
                print(ps.name)
                print(ps.get_stats())

    def most_effective_move(self, attacker: Player):
        move_damages = self._get_moves_order_of_effectiveness(attacker)

        return move_damages[0]

    # region private methods
    def _fanfare(self, _pokemon_state: PokemonState):
        if equal_ability(_pokemon_state, "drizzle"):
            self.weather_state = WeatherState(Weather.heavy_rain, 5)
        if equal_ability(_pokemon_state, "drought"):
            self.weather_state = WeatherState(Weather.sunny_day, 5)
        if equal_ability(_pokemon_state, "snow_warning"):
            self.weather_state = WeatherState(Weather.hailstorm, 5)
        if equal_ability(_pokemon_state, "sand_stream"):
            self.weather_state = WeatherState(Weather.sandstorm, 5)
        if equal_ability(_pokemon_state, "electric_surge"):
            self.field_state = FieldState(Field.electric, 5)
        elif equal_ability(_pokemon_state, "psychic_surge"):
            self.field_state = FieldState(Field.psychic, 5)
        elif equal_ability(_pokemon_state, "grassy_surge"):
            self.field_state = FieldState(Field.grass, 5)
        elif equal_ability(_pokemon_state, "misty_surge"):
            self.field_state = FieldState(Field.mist, 5)
        elif equal_ability(_pokemon_state, "intrepid_sword"):
            _pokemon_state.update_stats_rank(atk=1)
        elif equal_ability(_pokemon_state, "dauntless_shield"):
            _pokemon_state.update_stats_rank(df=1)

    def _get_players_spd_desc(self):
        return sorted(
            [0, 1], key=lambda x: self._get_playing_pokemon_state(x).get_spd(), reverse=True)

    def _get_target_player(self, _player: Player):
        return 1 if _player == 0 else 0

    def _switch_pokemon(self, _player: Player, _action: SwitchPokemonActions):
        parties_index = _action - 4

        self.playing_pokemons[_player] = parties_index
        s = self._get_playing_pokemon_state(_player)
        self._fanfare(s)

    def _get_playing_pokemon_state(self, _player: Player):
        return self.parties[_player][self.playing_pokemons[_player]]

    def _get_playing_pokemon_states(self):
        return [self._get_playing_pokemon_state(i) for i in [0, 1]]

    def _includes_abilities(self, _pokemon_state: PokemonState, _ability_names: list[str]):
        return _pokemon_state.get_ability_name_en() in _ability_names

    def _initialize_actions(self):
        self.actions = [None, None]

    def _get_this_turn_move(self, _player: Player):
        return self._get_playing_pokemon_state(_player).get_usable_move(
            self.actions[_player])

    def _active_ability_when_move(self, _player: Player, _pokemon_state: PokemonState):
        if self._includes_abilities(_pokemon_state, ["libero", "protean"]):
            m = self._get_this_turn_move(_player)
            _pokemon_state.types = [m.type]

    def _calc_effective_ratio(self, effectivities: list[tuple[int, float]], df_pokemon_state: PokemonState) -> float:
        enemy_types = df_pokemon_state.types
        effective_ratio = 1.00
        for _effective in effectivities:
            if _effective[0] in enemy_types:
                effective_ratio = effective_ratio * _effective[1]

        if equal_ability(df_pokemon_state, "prism_armor"):
            effective_ratio = effective_ratio * 3 / 4

        return effective_ratio

    def _calc_move_power(self, player: Player, move: Move = None):
        move = move if move else self._get_this_turn_move(player)
        myself = self._get_playing_pokemon_state(player)
        target = self._get_playing_pokemon_state(self._get_target_player(player))

        correction = 4096

        if (myself.get_ability_name_en() == "fairy_aura" and Type(move.type) == Type.fairy) or\
                (myself.get_ability_name_en() == "dark_aura" and Type(move.type) == Type.dark):
            if target.get_ability_name_en() == "aura_break":
                correction = 3075
            else:
                correction = 5448

        return half_up(move.power * correction / 4096)

    def _calc_atk(self, _player: Player, move: Move = None):
        def under_one_third():
            ps = self._get_playing_pokemon_state(_player)

            return ps.remaining_hp * 3 <= ps.max_hp

        move = move if move else self._get_this_turn_move(_player)
        atk_pokemon_state = self._get_playing_pokemon_state(_player)
        atk = atk_pokemon_state.get_atk() if move.category == 1 else atk_pokemon_state.get_sp_atk()
        if equal_ability(atk_pokemon_state, "torrent") and under_one_third() and Type(move.type) == Type.water:
            return half_up(atk * 6144 / 4096)
        else:
            return atk

    def _calc_df(self, _player: Player, _target: Player, move: Move = None):
        move = move if move else self._get_this_turn_move(_player)
        df_pokemon_state = self._get_playing_pokemon_state(_target)
        df = df_pokemon_state.get_df() if move.category == 1 else df_pokemon_state.get_sp_df()

        return df

    def _calc_weather_ratio(self, move: Move):
        if self.weather_state is None:
            return 1
        elif (self.weather_state.weather == Weather.heavy_rain and Type(move.type) == Type.water) or\
                (self.weather_state.weather == Weather.sunny_day and Type(move.type) == Type.fire):
            return 1.5
        else:
            return 1

    def _calc_damage(self, player: Player, target: Player, move: Move = None):
        atk_pokemon_state = self._get_playing_pokemon_state(player)
        df_pokemon_state = self._get_playing_pokemon_state(target)
        move = move if move else self._get_this_turn_move(player)
        if move.category == 0:
            return 0

        level = 50
        range_ratio = 1
        parental_bond_ratio = 1
        whether_ratio = self._calc_weather_ratio(move)
        critical_ratio = 1
        random_ratio = 1
        type_match_ratio = 1.5 if move.type in atk_pokemon_state.types else 1
        effective_ratio = self._calc_effective_ratio(
            move.effectivities, df_pokemon_state)
        burn_ratio = 1
        m = 1
        m_protect = 1
        move_power = self._calc_move_power(player, move=move)
        atk = self._calc_atk(player, move=move)
        df = self._calc_df(player, target, move=move)

        i1 = floor(level * 2 / 5 + 2)
        i2 = floor(i1 * move_power * atk / df)
        i3 = floor(i2 / 50 + 2)
        i4 = half_down(i3 * range_ratio)
        i5 = half_down(i4 * parental_bond_ratio)
        i6 = half_down(i5 * whether_ratio)
        i7 = half_down(i6 * critical_ratio)
        i8 = floor(i7 * random_ratio)
        i9 = half_down(i8 * type_match_ratio)
        i10 = floor(i9 * effective_ratio)
        i11 = half_down(i10 * burn_ratio)
        i12 = half_down(i11 * m)
        damage = half_down(i12 * m_protect)

        return damage

    def _some_fainted_pokemon(self):
        for pokemon in self._get_playing_pokemon_states():
            if pokemon.is_fainted():
                return True

        return False

    def _get_remaining_pokemons(self, player: Player):
        remaining_pokemons: list[PokemonState] = list()
        for pokemon in self.parties[player]:
            if pokemon.is_fainted() is False:
                remaining_pokemons.append(pokemon)

        return remaining_pokemons

    def _get_moves_order_of_effectiveness(self, attacker: Player):
        atk_regal_moves = self._get_playing_pokemon_state(
            attacker).base_info.regal_moves
        defender = self._get_target_player(attacker)
        defender_pokemon_state = self._get_playing_pokemon_state(defender)

        move_damage = []
        for move in atk_regal_moves:
            damage = self._calc_damage(attacker, defender, move=move)
            accuracy = move.accuracy / 100 if move.accuracy else 1
            expectation = damage * accuracy
            defender_hp = defender_pokemon_state.max_hp
            move_damage.append([move, expectation / defender_hp])

        return sorted(move_damage, key=lambda x: x[1], reverse=True)
    # endregion

from enum import Enum, auto


class StatusAilment(Enum):
    burn = auto()  # やけど
    freeze = auto()  # こおり
    paralysis = auto()  # まひ
    poison = auto()  # どく
    sleep = auto()  # ねむり
    bad_poison = auto()  # もうどく
    confusion = auto()  # こんらん
    curse = auto()  # のろい
    encore = auto()  # アンコール
    protect = auto()  # まもる
    identify = auto()  # みきり
    infatuation = auto()  # メロメロ
    leech_seed = auto()  # やどりぎのタネ
    lock_on = auto()  # ロックオン
    nightmare = auto()  # あくむ
    bound = auto()  # バインド
    perish_song = auto()  # ほろびのうた
    taunt = auto()  # ちょうはつ
    torment = auto()  # いちゃもん
    yawn = auto()  # あくび
    aqua_ring = auto()  # アクアリング
    smack_down = auto()  # うちおとす
    grudge = auto()  # おんねん
    disable = auto()  # かなしばり
    kings_shield = auto()  # キングシールド
    endure = auto()  # こらえる
    uproar = auto()  # さわぐ
    throat_chop = auto()  # じごくづき
    charge = auto()  # じゅうでん
    tar_shot = auto()  # タールショット
    max_guard = auto()  # ダイウォール
    octolock = auto()  # たこがため
    minimize = auto()  # ちいさくなる
    rage_powder = auto()  # いかりのこな
    follow_me = auto()  # このゆびとまれ
    levitate = auto()  # ふゆう
    invalidate_ability = auto()  # とくせいなし
    can_not_escape = auto()  # にげられない
    ingrain = auto()  # ねをはる
    uutotomize = auto()  # ボディーパージ
    magic_coat = auto()  # マジックコート
    defense_curl = auto()  # まるくなる
    substitute = auto()  # みがわり
    destiny_bond = auto()  # みちづれ


class Field(Enum):
    grass = auto()
    electric = auto()
    psychic = auto()
    mist = auto()

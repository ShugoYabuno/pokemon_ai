from envs.pokemon import SingleBattle, PokemonState

rillaboom = PokemonState("ゼルネアス", {
    "c": 252,
    "s": 252,
}, "c")
rillaboom.set_move("ムーンフォース")
rillaboom.set_ability("フェアリーオーラ")

cinderace = PokemonState("クレセリア", {
    "h": 252,
    "b": 252,
}, "B")
cinderace.set_move("れいとうビーム")
cinderace.set_ability("ふゆう")

inteleon = PokemonState("インテレオン", {
    "h": 12,
    "c": 252,
    "s": 252
}, "A")
inteleon.set_move("なみのり")
inteleon.set_ability("げきりゅう")

party0 = (inteleon, cinderace, inteleon)
party1 = (cinderace, rillaboom, inteleon)

singleBattle = SingleBattle(party0, party1)
singleBattle.info()
singleBattle.set_action(0, 0)
singleBattle.set_action(1, 0)
singleBattle.advance_turn()
singleBattle.info()

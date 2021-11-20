from envs.pokemon import SingleBattle, PokemonState

a = PokemonState("ゼルネアス", {
    "c": 252,
    "s": 252,
}, "c")
a.set_move("ムーンフォース")
a.set_ability("フェアリーオーラ")

b = PokemonState("クレセリア", {
    "h": 252,
    "b": 252,
}, "B")
b.set_move("れいとうビーム")
b.set_ability("ふゆう")

c = PokemonState("インテレオン", {
    "h": 12,
    "c": 252,
    "s": 252
}, "A")
c.set_move("なみのり")
c.set_ability("げきりゅう")

party0 = (c, b, c)
party1 = (b, a, c)

singleBattle = SingleBattle(party0, party1)
singleBattle.info()
singleBattle.set_action(0, 0)
singleBattle.set_action(1, 0)
singleBattle.advance_turn()
singleBattle.info()

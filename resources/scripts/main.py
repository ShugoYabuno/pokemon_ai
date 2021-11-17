from envs.pokemon import SingleBattle, PokemonState

rillaboom = PokemonState("ゴリランダー", {
    "h": 252,
    "a": 252,
    "s": 4,
}, "A")
rillaboom.set_move("ドラムアタック")
rillaboom.set_move("じしん")
print(rillaboom)

cinderace = PokemonState("エースバーン", {
    "h": 252,
    "a": 252,
    "s": 4,
}, "A")
cinderace.set_move("かえんボール")
cinderace.set_move("とびひざげり")

inteleon = PokemonState("インテレオン", {
    "h": 252,
    "c": 252,
    "s": 4
}, "A")
inteleon.set_move("みずのはどう")
inteleon.set_move("シャドーボール")

party0 = (rillaboom, cinderace, inteleon)
party1 = (cinderace, rillaboom, inteleon)

singleBattle = SingleBattle(party0, party1)
singleBattle.info()
singleBattle.set_action(0, 0)
singleBattle.set_action(1, 0)
singleBattle.advance_turn()
singleBattle.info()

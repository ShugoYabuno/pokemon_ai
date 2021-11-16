from envs.pokemon import Pokemon, SingleBattle

rillaboom = Pokemon("ゴリランダー", {
    "h": 252,
    "a": 252,
    "s": 4,
}, "a")
rillaboom.set_move("ドラムアタック")
rillaboom.set_move("じしん")

cinderace = Pokemon("エースバーン", {
    "h": 252,
    "a": 252,
    "s": 4,
}, "A")
cinderace.set_move("かえんボール")
cinderace.set_move("とびひざげり")

inteleon = Pokemon("インテレオン", {
    "h": 252,
    "c": 252,
    "s": 4
}, "A")
inteleon.set_move("みずのはどう")
inteleon.set_move("シャドーボール")

party0 = (rillaboom, cinderace, inteleon)
party1 = (cinderace, rillaboom, inteleon)

singleBattle = SingleBattle(party0, party1)
singleBattle.set_action(0, 0)
singleBattle.set_action(1, 0)
singleBattle.advance_turn()
singleBattle.info()

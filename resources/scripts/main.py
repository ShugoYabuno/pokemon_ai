from envs.pokemon import SingleBattle, PokemonState

rillaboom = PokemonState("ゴリランダー", {
    "h": 252,
    "a": 252,
}, "A")
rillaboom.set_move("ドラムアタック")
rillaboom.set_move("じしん")
rillaboom.set_ability("グラスメイカー")

cinderace = PokemonState("エースバーン", {
    "a": 252,
    "s": 252,
}, "S")
cinderace.set_move("かえんボール")
cinderace.set_move("とびひざげり")
cinderace.set_ability("リベロ")

inteleon = PokemonState("インテレオン", {
    "c": 252,
    "s": 252
}, "A")
inteleon.set_move("みずのはどう")
inteleon.set_move("シャドーボール")
inteleon.set_ability("げきりゅう")

party0 = (rillaboom, cinderace, inteleon)
party1 = (cinderace, rillaboom, inteleon)

singleBattle = SingleBattle(party0, party1)
singleBattle.info()
singleBattle.set_action(0, 0)
singleBattle.set_action(1, 1)
singleBattle.advance_turn()
singleBattle.info()

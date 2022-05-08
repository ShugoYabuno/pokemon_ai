from envs.pokemon import SingleBattle, PokemonState

# a = PokemonState("サンダー", {
#     "c": 252,
#     "s": 252,
#     "h": 4
# }, "S")
# a.set_move("ぼうふう")
# a.set_move("はねやすめ")
# a.set_move("ねっぷう")
# a.set_move("ボルトチェンジ")
# a.set_ability("せいでんき")

# b = PokemonState("ランドロス", {
#     "h": 252,
#     "b": 252,
#     "s": 4
# }, "B")
# b.set_move("じしん")
# b.set_move("そらをとぶ")
# b.set_move("がんせきふうじ")
# b.set_move("つるぎのまい")
# b.set_ability("いかく")

zacian = PokemonState("ザシアンf", {}, "A")
zamazenta = PokemonState("ザマゼンタf", {}, "A")
# print(zacian)
# print(zamazenta)


party0 = (zacian, zacian, zacian)
party1 = (zamazenta, zamazenta, zamazenta)

singleBattle = SingleBattle(party0, party1)
print(singleBattle._most_effective_move(0))
print(singleBattle._most_effective_move(1))

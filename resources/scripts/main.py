from envs.pokemon import SingleBattle, PokemonState
import copy
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.subplot.left'] = 0.17

mewtwo = PokemonState("ミュウツー")
lugia = PokemonState("ルギア")
ho_oh = PokemonState("ホウオウ")
groudon = PokemonState("グラードン")
groudon.set_ability("ひでり")
kyogre = PokemonState("カイオーガ")
kyogre.set_ability("あめふらし")
rayquaza = PokemonState("レックウザ")
dialga = PokemonState("ディアルガ")
palkia = PokemonState("パルキア")
giratina = PokemonState("ギラティナ")
giratina_o = PokemonState("ギラティナo")
zekrom = PokemonState("ゼクロム")
reshiiam = PokemonState("レシラム")
kyurem = PokemonState("キュレム")
kyurem_w = PokemonState("キュレムw")
kyurem_b = PokemonState("キュレムb")
xerneas = PokemonState("ゼルネアス")
xerneas.set_ability("フェアリーオーラ")
yveltal = PokemonState("イベルタル")
yveltal.set_ability("ダークオーラ")
zygarde = PokemonState("ジガルデ")
solgaleo = PokemonState("ソルガレオ")
lunala = PokemonState("ルナアーラ")
necrozma = PokemonState("ネクロズマ")
necrozma_s = PokemonState("ネクロズマs")
necrozma_m = PokemonState("ネクロズマm")
zacian = PokemonState("ザシアンf")
zacian.set_ability("ふとうのけん")
zamazenta = PokemonState("ザマゼンタf")
zamazenta.set_ability("ふくつのたて")
calyrex_w = PokemonState("バドレックスw")
calyrex_b = PokemonState("バドレックスb")


pokemons = [mewtwo, lugia, ho_oh, groudon, kyogre, rayquaza,
            dialga, palkia, giratina, zekrom, reshiiam, kyurem, xerneas, yveltal, zygarde,
            solgaleo, lunala, necrozma_s, necrozma_m, zacian, zamazenta, calyrex_w, calyrex_b]

sum = []
table = []


def step(a):
    if a > 0:
        return 1
    else:
        return 0


for x in pokemons:
    sum_damage = 0

    for y in pokemons:
        if x.name == y.name:
            continue

        attacker = copy.deepcopy(x)
        defender = copy.deepcopy(y)

        party_x = [attacker]
        party_y = [defender]
        x_spd = attacker.stats.spd
        y_spd = defender.stats.spd

        singleBattle = SingleBattle(party_x, party_y)
        inflict_damage_ratio = singleBattle.most_effective_move(0)
        receive_damage_ratio = singleBattle.most_effective_move(1)
        speed_correction_value = 1.2

        sum_damage += (inflict_damage_ratio[1] * speed_correction_value**step(x_spd - y_spd)) / (receive_damage_ratio[1] * speed_correction_value**step(y_spd - x_spd))

    sum.append([x, sum_damage / (len(pokemons) - 1)])

sorted_pokemons = sorted(sum, key=lambda x: x[1])

heights = []
labels = []
for [pokemon, ratio] in sorted_pokemons:
    labels.append(pokemon.name)
    heights.append(ratio)

left = np.arange(len(heights))

height=0.3

plt.barh(left, heights, color='r', height=height, align='center')
plt.yticks(left + height/2, labels)
plt.show()

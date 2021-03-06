from envs.pokemon import SingleBattle, PokemonState
import copy
import matplotlib.pyplot as plt
import numpy as np
import math
import scipy.stats

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
# zacian = PokemonState("ザシアンf")
# zacian.set_ability("ふとうのけん")
# zamazenta = PokemonState("ザマゼンタf")
# zamazenta.set_ability("ふくつのたて")
eternatus = PokemonState("ムゲンダイナ")
calyrex_w = PokemonState("バドレックスw")
calyrex_b = PokemonState("バドレックスb")


pokemons = [mewtwo, lugia, ho_oh, groudon, kyogre, rayquaza,
            dialga, palkia, giratina, zekrom, reshiiam, kyurem, xerneas, yveltal, zygarde,
            solgaleo, lunala, necrozma_s, necrozma_m, eternatus, calyrex_w, calyrex_b]

def step(a):
    if a > 0:
        return 1
    else:
        return 0


def zscore(x, axis=None):
    xmean = x.mean(axis=axis, keepdims=True)
    xstd = np.std(x, axis=axis, keepdims=True)
    zscore = (x - xmean) / xstd
    return zscore


speed_correction_values = [1.3, 1.0]
labels = []
color = "rgby"
height=0.3

for index, speed_correction_value in enumerate(speed_correction_values):
    sum = []

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

            inflict = inflict_damage_ratio[1] * speed_correction_value**step(x_spd - y_spd)
            receive = receive_damage_ratio[1] * speed_correction_value**step(y_spd - x_spd)
            sum_damage += math.log2(inflict / receive)

        sum.append([x.name, sum_damage / (len(pokemons) - 1)])

    heights = []
    if index == 0:
        sorted_pokemons = sorted(sum, key=lambda x: x[1])
        labels = [pokemon[0] for pokemon in sorted_pokemons]
        heights = [pokemon[1] for pokemon in sorted_pokemons]
        normalized = scipy.stats.zscore(heights)
        left = np.arange(len(normalized))

        plt.barh(left, normalized, color=color[index], height=height, align='center', label=str(speed_correction_value))
    else:
        sorted_pokemons = sorted(sum, key=lambda x: labels.index(x[0]))
        heights = [pokemon[1] for pokemon in sorted_pokemons]
        normalized = scipy.stats.zscore(heights)
        plt.barh(left-height*index, normalized, color=color[index], height=height, align='center', label=str(speed_correction_value))


plt.yticks(left + height/2, labels)
plt.legend()
plt.show()

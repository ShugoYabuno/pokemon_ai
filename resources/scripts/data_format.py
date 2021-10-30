import json
import re

gen1 = json.load(open("./resources/data/original/pokemons/gen1-jp.json", "r"))
gen2 = json.load(open("./resources/data/original/pokemons/gen2-jp.json", "r"))
gen3 = json.load(open("./resources/data/original/pokemons/gen3-jp.json", "r"))
gen4 = json.load(open("./resources/data/original/pokemons/gen4-jp.json", "r"))
gen5 = json.load(open("./resources/data/original/pokemons/gen5-jp.json", "r"))
gen6 = json.load(open("./resources/data/original/pokemons/gen6-jp.json", "r"))
gen7 = json.load(open("./resources/data/original/pokemons/gen7-jp.json", "r"))
gen8 = json.load(open("./resources/data/original/pokemons/gen8-jp.json", "r"))

gens = [
    gen1,
    gen2,
    gen3,
    gen4,
    gen5,
    gen6,
    gen7,
    gen8
]

i = 0
pokemons = []
for _gen in gens:
    i += 1

    for _pokemon in _gen:
        name = _pokemon["name"]
        if re.search(r"-\d", name):
            continue

        level_up_moves = [_move[1] for _move in _pokemon["level_up_moves"]]

        pokemon = {
            "name": name,
            "base_stats": _pokemon["base_stats"],
            "moves": level_up_moves
        }
        pokemons.append(pokemon)

with open(f"./resources/data/formatted/pokemons.json", "w") as f:
    json.dump(pokemons, f, ensure_ascii=False)

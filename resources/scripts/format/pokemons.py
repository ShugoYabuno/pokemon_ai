from os import path
import json
from typing import Final
import re


def relative_path(file_path: str):
    return path.join(path.dirname(__file__), file_path)


poketetsu_pokemons: Final = json.load(
    open(relative_path("../../data/original/poketetsu/pokemons.json"), "r"))
pokemon_home_pokemons: Final = json.load(
    open(relative_path("../../data/original/pokemon_home/pokemons.json"), "r"))

pokemons_add_form = []
counter = []
for poketetsu_pokemon in poketetsu_pokemons:
    form = counter.count(poketetsu_pokemon["index"])
    mega = None
    if (re.search(r"\Sm$", poketetsu_pokemon["name"]) and (not (poketetsu_pokemon["name"] in ["オドリドリm", "ネクロズマm"]))) or\
            poketetsu_pokemon["name"] in ["リザードンx", "リザードンy"]:
        mega = poketetsu_pokemon["name"][-1]
        form = 0

    pokemons_add_form.append({
        **poketetsu_pokemon,
        "form": form,
        "mega": mega
    })
    counter.append(poketetsu_pokemon["index"])


def find_pokemon(id: int, form: int):
    for pokemon in pokemons_add_form:
        if pokemon["index"] == id and pokemon["form"] == form:
            return pokemon


formatted_pokemons = []

for pokemon_home_pokemon in pokemon_home_pokemons:
    for form in pokemon_home_pokemon["forms"].keys():
        pokemon_id = pokemon_home_pokemon["id"]
        data_by_form = pokemon_home_pokemon["forms"][form]
        form_int = int(form)
        pokemon = find_pokemon(pokemon_id, form_int)
        if pokemon is None:
            continue

        useful_moves = [{"id": waza["id"], "utilization_rate": float(waza["val"]) / 100} for waza in data_by_form["temoti"]["waza"]]

        formatted_pokemons.append({
            **pokemon,
            "useful_moves": useful_moves
        })

with open(relative_path("../../data/formatted/pokemons.json"), "w") as f:
    json.dump(formatted_pokemons, f, ensure_ascii=False)

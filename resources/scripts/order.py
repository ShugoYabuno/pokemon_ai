import json
from typing import Final

pokemons: Final = json.load(
    open("./resources/data/original/poketetsu/pokemons.json", "r"))

pokemon_names = []
for pokemon in pokemons:
    pokemon_names.append(f"{pokemon['name_en']} {pokemon['name']}")

pokemon_names.sort()

print(pokemon_names)

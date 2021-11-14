import requests
from bs4 import BeautifulSoup
import re
import json
import time


def checkLeftColumn(_tr, _text):
    return len(_tr.find_all("td")) >= 1 and _tr.find_all("td")[0].get_text() == _text


def getATagIndex(_a):
    pokemonId = re.search(
        r"\d+\w*$", _a["href"]).group()
    pokemonIndex = re.sub(r"[a-z]+", "", pokemonId)
    return int(pokemonIndex)


base_url = "https://yakkun.com/swsh/zukan/n"
i = 1
pokemons = []
max = 898

while i <= max:
    print(i)

    next_form = ""
    name = ""
    while True:
        time.sleep(0.3)
        form = next_form
        response = requests.get(base_url + str(i) + next_form)

        soup = BeautifulSoup(response.content, 'html.parser')

        if soup.select(".select_list") and len(soup.select(".select_list")) >= 2:
            form_table = soup.select(".select_list")[1]
            form_li_list = form_table.find_all("li")
            find_strong = False
            next_form = ""
            for _li in form_li_list:
                exist_strong = _li.find("strong")
                if exist_strong:
                    find_strong = True
                elif find_strong is False:
                    continue
                else:
                    href = _li.find("a")["href"]

                    path = re.search(r"\d[a-z]$", href).group()
                    next_form = path[1:]
                    break

        base_anchor = soup.select_one("div#base_anchor > table")
        base_anchor_trs = base_anchor.find_all("tr")
        name = base_anchor_trs[0].find("th").get_text() if form == "" else name

        print(name + form)

        evolutions = []
        for _tr in base_anchor_trs:
            # if _index == 0:
            #     name = _tr.find("th").get_text() + form
            # elif checkLeftColumn(_tr, "全国No."):
            #     number = int(_tr.find_all("td")[1].get_text())
            if checkLeftColumn(_tr, "重さ"):
                weight = float(
                    re.search(r"[\d.]+", _tr.find_all("td")[1].get_text()).group())
            elif checkLeftColumn(_tr, "タイプ"):
                typeAs = _tr.find_all("a")
                types = [getATagIndex(typeA) for typeA in typeAs]
            elif checkLeftColumn(_tr, "英語名"):
                name_en = _tr.find("li").get_text()
            elif _tr.select(".evo_list"):
                evolutionElList = _tr.find_all("li")
                findIndex = 0
                findSelf = False
                for _index, _item in enumerate(evolutionElList):
                    if _item.find("img") and _item.find("img")["alt"] == name:
                        findSelf = True
                        findIndex = _index
                    elif findSelf and _item.find("img"):
                        evolutionIndex = getATagIndex(_item.find("a"))
                        evolutions.append(evolutionIndex)
                    elif findSelf and findIndex + 1 == _index:
                        continue
                    elif findSelf and _item.find("img") is None:
                        break

        stats_anchor = soup.select_one("#stats_anchor > table")

        stats_anchor_trs = stats_anchor.find_all("tr")
        hp_test = stats_anchor_trs[1].find_all("td")[1].get_text()
        hp = int(re.search(r"\d+", hp_test).group())
        atk_text = stats_anchor_trs[2].find_all("td")[1].get_text()
        atk = int(re.search(r"\d+", atk_text).group())
        dfText = stats_anchor_trs[3].find_all("td")[1].get_text()
        df = int(re.search(r"\d+", dfText).group())
        sp_atk_text = stats_anchor_trs[4].find_all("td")[1].get_text()
        sp_atk = int(re.search(r"\d+", sp_atk_text).group())
        sp_df_text = stats_anchor_trs[5].find_all("td")[1].get_text()
        sp_df = int(re.search(r"\d+", sp_df_text).group())
        spd_text = stats_anchor_trs[6].find_all("td")[1].get_text()
        spd = int(re.search(r"\d+", spd_text).group())

        abilitiesStartIndex = next(_index for _index, _tr in enumerate(
            stats_anchor_trs) if _tr.select_one("#characteristic"))
        del stats_anchor_trs[:abilitiesStartIndex + 1]

        abilities = []
        for tr in stats_anchor_trs:
            a = tr.find("a")
            if a and a.get_text():
                abilities.append(a.get_text().replace("*", ""))

        move_anchor = soup.select_one("#move_list")
        move_anchor_trs = move_anchor.find_all("tr")
        moves = []
        for _tr in move_anchor_trs:
            if(_tr.get("id", None) == "past_move"):
                break
            elif _tr.select(".move_name_cell"):
                moves.append(getATagIndex(
                    _tr.select_one(".move_name_cell").find("a")))

        moves = list(set(moves))

        pokemon = {
            "index": i,
            "name": name + form,
            "name_en": name_en + f" {form}",
            "types": types,
            "weight": weight,
            "evolutions": evolutions,
            "moves": moves,
            "base_stats": {
                "hp": hp,
                "atk": atk,
                "df": df,
                "sp_atk": sp_atk,
                "sp_df": sp_df,
                "spd": spd,
            }
        }
        pokemons.append(pokemon)

        if next_form == "":
            break

    i += 1

with open("./resources/data/original/poketetsu/pokemons.json", "w") as f:
    json.dump(pokemons, f, ensure_ascii=False)

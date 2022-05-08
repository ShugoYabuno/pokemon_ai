import requests
from bs4 import BeautifulSoup
import re
import json
import time

base_url = "https://yakkun.com/swsh/zukan/search/?move="
i = 1
moves = []
max = 841

while i <= max:
    time.sleep(0.3)
    print(i)

    response = requests.get(base_url + str(i))

    soup = BeautifulSoup(response.content, 'html.parser')

    name = re.search(
        r"『.+』", soup.find("a", id="database").get_text()).group()
    name = re.search(r"[^『』]+", name).group()
    print(name)

    name_en = soup.select_one(".narrow.small.right").get_text()
    name_en = re.search(r"名：.+$", name_en).group()[2:]
    print(name_en)

    move_data = soup.find("table", attrs={"summary": "技データ"})
    move_data_trs = move_data.find_all("tr")

    for _index, _tr in enumerate(move_data_trs):
        if _index == 0:
            type = _tr.find_all("td")[0].find("a")["href"]
            type = int(re.search(r"\d+$", type).group())
            if _tr.find_all("td")[1].find("a"):
                category = _tr.find_all("td")[1].find("a")["href"]
                category = int(re.search(r"\d+$", category).group())
            else:
                category = None
        if _index == 1:
            if re.search(r"^\d+$", _tr.find_all("td")[0].get_text()):
                power = int(_tr.find_all("td")[0].get_text())
            else:
                power = 0
            if re.search(r"^\d+$", _tr.find_all("td")[1].get_text()):
                accuracy = int(_tr.find_all("td")[1].get_text())
            else:
                accuracy = None
        if _index == 2:
            if re.search(r"^\d+$", _tr.find_all("td")[0].get_text()):
                pp = int(_tr.find_all("td")[0].get_text())
            else:
                pp = None
            target = _tr.find_all("td")[1].find("a")["href"]
            target = int(re.search(r"\d+$", target).group())

    effect_text = soup.find(
        "table", class_="effect_table").find("td").get_text()
    effect = re.sub(r"<.+>", "", effect_text)
    priority_search = re.search(r"優先度:\+\d", effect)
    priority = int(priority_search.group()[-1:]) if priority_search else 0

    effectivities = []

    type_chart = soup.find("table", class_="type_chart")

    if type_chart:
        type_tds = type_chart.find_all("tr")[0].find_all("td")
        compatibility_tds = type_chart.find_all("tr")[1].find_all("td")

        for (_type, _effective) in zip(type_tds, compatibility_tds):
            if _effective.find("span") and _effective.find("span").get_text() == "●":
                effectivities.append(
                    [int(re.search(r"\d+", _type["class"][0]).group()), 2])
            if _effective.find("span") and _effective.find("span").get_text() == "▲":
                effectivities.append(
                    [int(re.search(r"\d+", _type["class"][0]).group()), 0.5])
            if _effective.find("span") and _effective.find("span").get_text() == "×":
                effectivities.append(
                    [int(re.search(r"\d+", _type["class"][0]).group()), 0])

    move = {
        "index": i,
        "name": name,
        "name_en": name_en,
        "type": type,
        "category": category,
        "power": power,
        "accuracy": accuracy,
        "pp": pp,
        "target": target,
        # "effect": effect,
        "priority": priority,
        "effectivities": effectivities
    }
    moves.append(move)
    i += 1

with open("./resources/data/original/poketetsu/moves.json", "w") as f:
    json.dump(moves, f, ensure_ascii=False)

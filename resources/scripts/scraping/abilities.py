import requests
from bs4 import BeautifulSoup
import re
import json
import time

base_url = "https://yakkun.com/swsh/zukan/search/?tokusei="
i = 1
abilities = []
max = 266

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
    name_en = name_en.replace(" ", "_").lower()
    print(name_en)

    move = {
        "index": i,
        "name": name,
        "name_en": name_en,
    }
    abilities.append(move)
    i += 1

with open("./resources/data/original/poketetsu/abilities.json", "w") as f:
    json.dump(abilities, f, ensure_ascii=False)

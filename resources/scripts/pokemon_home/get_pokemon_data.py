import urllib.request
import json
from os import path


def relative_path(file_path: str):
    return path.join(path.dirname(__file__), file_path)


def get_latest_season():
    try:
        url = 'https://api.battle.pokemon-home.com/cbd/competition/rankmatch/list'
        req_header = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'countrycode': '304',
            'authorization': 'Bearer',
            'langcode': '1',
            'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
            'content-type': 'application/json'
        }
        req_data = json.dumps({
            'soft': 'Sw'
        })

        req = urllib.request.Request(url, data=req_data.encode(), method='POST', headers=req_header)

        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read())
            latest_season = sorted([int(season) for season in list(body["list"].keys())], reverse=True)[0]
            latest_season_rules = body["list"][str(latest_season)]
            print(latest_season_rules)

            for rule_id in latest_season_rules.keys():
                rule = latest_season_rules[rule_id]["rule"]
                if rule == 0:
                    rst = latest_season_rules[rule_id]["rst"]
                    ts2 = latest_season_rules[rule_id]["ts2"]
                    break

            return rule_id, rst, ts2

    except urllib.error.URLError as e:
        print(e.reason)


def write_pokemon_home_data(data):
    with open(relative_path("../../data/original/pokemon_home/pokemons.json"), "w") as f:
        json.dump(data, f, ensure_ascii=False)


def get_pokemon_data():
    rule_id, rst, ts2 = get_latest_season()

    data = {}
    for page in list(range(1, 6)):
        try:
            req = urllib.request.Request(f"https://resource.pokemon-home.com/battledata/ranking/{rule_id}/{rst}/{ts2}/pdetail-{page}")
            req.add_header('user-agent', 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36')
            req.add_header('accept', 'application/json')

            url = f"https://resource.pokemon-home.com/battledata/ranking/{rule_id}/{rst}/{ts2}/pdetail-{page}"
            req_header = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Mobile Safari/537.36',
                'accept': 'application/json'
            }

            req = urllib.request.Request(url, headers=req_header)

            with urllib.request.urlopen(req) as response:
                body = json.loads(response.read())

                with open("./resources/data/original/poketetsu/pokemons.json", "w") as f:
                    json.dump(body, f, ensure_ascii=False)
                print(body)
                data = {
                    **data,
                    **body
                }

        except urllib.error.URLError as e:
            print(e.reason)

    write_pokemon_home_data(data)


get_pokemon_data()

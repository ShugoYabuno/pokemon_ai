from board.index import Pokemon


zacian = Pokemon("ザシアンf", {
    "h": 220,
    "a": 236,
    "b": 4,
    "d": 4,
    "s": 44
}, "A")
zacian.set_move("きゅじゅうざん")
zacian.set_move("じゃれつく")
zacian.set_move("インファイト")
zacian.set_move("つるぎのまい")

zapdos = Pokemon("サンダー", {
    "h": 252,
    "b": 252,
    "d": 4,
}, "B")
zapdos.set_move("ぼうふう")
zapdos.set_move("ボルトチェンジ")
zapdos.set_move("でんじは")
zapdos.set_move("はねやすめ")

garchomp = Pokemon("ガブリアス", {
    "a": 252,
    "s": 252,
    "b": 4,
}, "A")
garchomp.set_move("じしん")
garchomp.set_move("スケイルショット")
garchomp.set_move("みがわり")
garchomp.set_move("つるぎのまい")

marowak = Pokemon("ガラガラa", {
    "h": 252,
    "a": 252,
    "s": 4,
}, "A")
marowak.set_move("フレアドライブ")
marowak.set_move("ポルターガイスト")
marowak.set_move("ホネブーメラン")
marowak.set_move("つるぎのまい")

porygon2 = Pokemon("ポリゴン2", {
    "h": 244,
    "b": 252,
    "s": 12,
}, "B")
porygon2.set_move("トライアタック")
porygon2.set_move("イカサマ")
porygon2.set_move("でんじは")
porygon2.set_move("じこさいせい")

quagsire = Pokemon("ヌオー", {
    "h": 252,
    "b": 252,
    "a": 4,
}, "B")
quagsire.set_move("じしん")
quagsire.set_move("カウンター")
quagsire.set_move("どくどく")
quagsire.set_move("じこさいせい")

print(zacian)
print(zapdos)
print(garchomp)
print(marowak)
print(porygon2)
print(quagsire)

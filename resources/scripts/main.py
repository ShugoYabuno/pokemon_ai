from board.index import Pokemon, SingleMatchBoard

effort = {
    "h": 4,
    "a": 252,
    "b": 0,
    "c": 0,
    "d": 0,
    "s": 252,
}

garchomp = Pokemon("ガブリアス", effort, "S")
tyranitar = Pokemon("バンギラス", effort, "S")
garchomp_tyranitar = SingleMatchBoard(garchomp, tyranitar)
print("ガブリアス -> バンギラス")
garchomp_tyranitar.set_move("じしん")
garchomp_tyranitar.set_move("つるぎのまい")
garchomp_tyranitar.set_move("げきりん")
garchomp_tyranitar.set_move("ステルスロック")
print(garchomp_tyranitar)

import re

# デッキリストの前処理用


def create_deck_from_deck_list(deck_list: dict) -> list:
    """
    デッキリストから枚数分のカードをリストとして挿入することで擬似的な、概念としてのデッキを作成\n
    引数にカード名をkey, 枚数をvalueを想定した辞書型、概ねget_main_board関数で作成されたものを想定\n
    返り値にカード名が枚数分続く、実際のデッキを模したリスト型を返す\n
    """
    deck = []

    for card in deck_list.keys():
        for i in range(deck_list[card]):
            deck.append(card)

    return deck


def get_main_board(path: str) -> dict:
    """
    いわゆるメインボードを解釈。メインとサイドを改行で区別。またデッキリストを解釈 4 HogeをHoge4枚と解釈\n
    引数にデッキリストファイルのパス\n
    返り値にカード名をkey, 枚数をvalueにした辞書型を返す\n
    """
    f = open(path, "r", encoding="utf-8")
    s = f.read()
    f.close()
    sl = s.split("\n")
    deck_list = {}
    maindeck = sl[: sl.index("")]
    for card in maindeck:  # GoldfishがArena用に出力する際につく識別用のタグを外すための部分が大多数
        splited = re.split(" ", card, 1)
        if "(" in splited[1]:
            text = re.split(" \(", splited[1])[0]
        elif "[":
            text = re.split(" \[", splited[1])[0]
        else:
            text = splited[1]
        if " <" in text:
            text = re.split(" <", text)[0]
        if type(text) is list:
            deck_list[text[0]] = int(splited[0])
        if type(text) is str:
            deck_list[text] = int(splited[0])
    return deck_list

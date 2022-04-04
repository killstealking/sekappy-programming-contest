from statsmodels.sandbox.stats.runs import runstest_1samp


def create_float_deck_list(deck: list, deck_key_dict: dict) -> list:
    """
    デッキリストとカードに番号を振った辞書からカード名をfloatに変換したリストを作成
    """
    float_deck_list = []
    for i in deck:
        float_deck_list.append(deck_key_dict[i])
    return float_deck_list


def create_deck_key_dict(original_deck: list) -> dict:
    """
    デッキリストからユニークなカードを一覧にして固有の番号をふる
    """
    unique_deck = set(original_deck)  # ユニークなカードのリスト
    deck_key_dict = {}
    for index, item in enumerate(unique_deck):
        deck_key_dict[item] = index
    return deck_key_dict


# https://en.wikipedia.org/wiki/Wald%E2%80%93Wolfowitz_runs_test
def runstest(float_deck_list: list) -> tuple:
    """
    デッキのランダム度を評価する関数
    """
    return runstest_1samp(float_deck_list, cutoff="mean", correction=False)

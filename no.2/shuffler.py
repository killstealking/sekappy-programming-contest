import math
import random  # 乱数としてのrandomの信頼度についての判断は使用者に委ねる

# シャッフル方法はWikipediaを参照した
# https://ja.wikipedia.org/wiki/%E3%82%B7%E3%83%A3%E3%83%83%E3%83%95%E3%83%AB_(%E3%82%AB%E3%83%BC%E3%83%89)


def pile_shuffle(deck: list, number_of_shuffle: int) -> list:
    """
    パイルシャッフル(ディールシャッフル)を行う\n
    引数にデッキを模したリスト、シャッフルの回数\n
    返り値にシャッフルされたデッキを模したリスト\n
    """
    pile_shuffled_deck = deck
    for shuffle in range(number_of_shuffle):  # シャッフルの回数分ループ
        pile_num = random.randint(4, 8)  # パイルの数を4から8の値でランダムに決める
        list_of_pile = [[] for piles in range(pile_num)]  # パイルを作成
        pile = 0
        for card in pile_shuffled_deck:  # パイルにカードを配る
            list_of_pile[pile].append(card)
            if pile == pile_num - 1:
                pile = 0
            else:
                pile += 1
        pile_shuffled_deck = []
        random.shuffle(list_of_pile)  # パイルの並びをランダムにする≒パイルを重ねる順番をランダムにする
        for pile in list_of_pile:  # パイルを重ね、デッキにする
            pile_shuffled_deck += pile
    return pile_shuffled_deck


def hindu_shuffle(deck: list, number_of_shuffle: int) -> list:
    """
    ヒンドゥーシャッフルを行う\n
    引数にデッキを模したリスト、シャッフルの回数\n
    返り値にシャッフルされたデッキを模したリスト\n
    """
    hindu_shuffled_deck = deck
    for i in range(number_of_shuffle):
        # 最初に半分にするポイントの誤差　殆どないと思うが10枚未満のデッキが入力された場合の処理も記載
        tolerance = (
            random.randint(0, 5) * random.choice([1, -1])
            if math.floor(len(hindu_shuffled_deck) / 2) > 5
            else (
                random.randint(0, math.floor(len(hindu_shuffled_deck) / 2))
                * random.choice([1, -1])
            )
        )
        split_point = math.floor(len(hindu_shuffled_deck) / 2) + tolerance  # 何枚目で分けたか
        deck_in_pick = hindu_shuffled_deck[:split_point]  # 手にとって上に載せるカードの束
        hindu_shuffled_deck = hindu_shuffled_deck[split_point:]  # カードが載せられる側の束
        while True:  # 手にとったほうがなくなるまで繰り返す
            # 取ったカードから何枚目まで(誤差含めて)をデッキに載せるか
            new_tolerance = random.randint(
                0, math.ceil(len(deck_in_pick) / 2)
            ) * random.choice([1, -1])
            new_deck = deck_in_pick[
                : math.ceil(len(deck_in_pick) / 2) + new_tolerance
            ]  # デッキに載せられるカードの束
            deck_in_pick = deck_in_pick[
                math.ceil(len(deck_in_pick) / 2) + new_tolerance :
            ]  # 　まだ手に取られている束
            hindu_shuffled_deck = hindu_shuffled_deck + new_deck  # 新たに載った結果
            if len(deck_in_pick) == 0:  # 手に取られているカードがない場合に終了する
                break
    return hindu_shuffled_deck


def riffle_shuffle(deck: list, number_of_shuffle: int) -> list:
    """
    リフルシャッフルを行う\n
    引数にデッキを模したリスト、シャッフルの回数\n
    返り値にシャッフルされたデッキを模したリスト\n
    """
    riffle_shuffled_deck = deck
    for i in range(number_of_shuffle):
        # 最初に半分にするポイントの誤差　殆どないと思うが10枚未満のデッキが入力された場合の処理も記載
        tolerance = (
            random.randint(0, 5) * random.choice([1, -1])
            if math.floor(len(riffle_shuffled_deck) / 2) > 5
            else (
                random.randint(0, math.floor(len(riffle_shuffled_deck) / 2))
                * random.choice([1, -1])
            )
        )
        split_point = math.floor(len(riffle_shuffled_deck) / 2) + tolerance  # 何枚目で分けたか
        left_deck = deck[:split_point]  # 左手に取った束
        right_deck = deck[split_point:]  # 右手に取った束
        riffle_shuffled_deck = []
        # どちらかの束がなくなるまで繰り返す
        while len(left_deck) > 0 and len(right_deck) > 0:
            # 枚数が多い束に重みをもたせつつ、約1/2の確率でどちらかの束からデッキに置かれるように
            if random.random() > ((len(left_deck) / len(right_deck)) / 2):
                riffle_shuffled_deck.append(left_deck.pop(0))
            else:
                riffle_shuffled_deck.append(right_deck.pop(0))
        # どちらかの束がなくなった段階で、もう片方の束をデッキに置いてシャッフル1回が完了
        if len(left_deck) > 0:
            riffle_shuffled_deck += left_deck
        if len(right_deck) > 0:
            riffle_shuffled_deck += right_deck
    return riffle_shuffled_deck


def over_hand_shuffle(deck: list, number_of_shuffle: int) -> list:
    """
    オーバーハンドシャッフルを行う\n
    引数にデッキを模したリスト、シャッフルの回数\n
    返り値にシャッフルされたデッキを模したリスト\n
    """
    over_hand_shuffled_deck = deck
    for i in range(number_of_shuffle):
        droppped_card = []
        while len(over_hand_shuffled_deck) > 0:
            # 1度に手に落とすカードの枚数　最大2割ほどとしている
            drop_number = (
                random.randint(0, math.ceil(len(over_hand_shuffled_deck) / 5)) + 1
            )
            # これから手に落とすカードの一時的な置き場
            temp_card = []
            count = 0
            # 落とす枚数までか、落とせるカードが無くなるまで落とす
            while count < drop_number and len(over_hand_shuffled_deck) > 0:
                temp_card.append(over_hand_shuffled_deck.pop(0))
                count += 1
            # すでに手に落ちているものと手に落ちたものを合算
            droppped_card = temp_card + droppped_card
        # すべてのカードが手に落ちたので落ちたカードを初期値にする
        over_hand_shuffled_deck = droppped_card
    return over_hand_shuffled_deck

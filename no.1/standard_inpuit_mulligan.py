import decimal
import random
import sys
from collections import Counter

from . import deck_parser


def combo_caliculate(
    number_of_try : int,
    deck : list,
    openning_hand_drawn : int,
    combo_list : list
) -> float:
    '''
    入力された要素からコンボ確率を計算\n
    引数は試行回数、デッキを模したリスト、初期手札の枚数、引きたいカード名のリスト\n
    返り値は有効数字3桁に設定した確率をパーセントとして返す\n
    '''
    number_of_combo_OK = 0
    decimal.getcontext().prec = 3  # 有効数字を3桁に指定

    for i in range(number_of_try):
        open_hand = Counter(random.sample(deck, openning_hand_drawn))
        flag = 0
        for combo_card in combo_list:
            if open_hand[combo_card] >= combo_list.count(combo_card):
                flag += 1
        if flag == len(combo_list):
            number_of_combo_OK += 1
    possibility = (
        decimal.Decimal(number_of_combo_OK) / decimal.Decimal(number_of_try)
    ) * 100  # パーセンテージにしている
    return possibility


def standard_input_main(argv):  # CUIに置ける対話用
    print('モンテカルロ法を用いて初手にコンボが揃う確率を計算します')
    if len(argv) == 1:  # .pyファイル実行時に引数にデッキリストファイルが指定されていない場合
        print('実行時にデッキリストが指定されていません')
        print('引数に有効なデッキリストを指定してください')
        sys.exit()  # 終了する
    deck_list = deck_parser.get_mainboard(argv[1])  # 引数のパスをデッキリストファイルとして取り込む
    deck = deck_parser.create_deck_from_deck_list(deck_list=deck_list)
    num_of_deck = input('デッキ枚数を入力してください\n')
    print('デッキ枚数: {}'.format(int(num_of_deck)))
    openning_hand_drawn = input('初期手札の枚数を入力してください\n')
    print('初期手札: {}'.format(int(openning_hand_drawn)))
    combo_list = []
    print('コンボに必要なカードを枚数分入力してください\nコンボに必要なカードをすべて入力したら finish と入力してください')
    count = 1
    while (
        True
    ):  # コンボカードを1枚1枚入力してもらう(シングルクォートをエスケープするリストを受け取るのが困難だったため)
        combo_card = input('コンボカード{}枚目'.format(count))
        if combo_card == 'finish':
            break
        combo_list.append(combo_card)
        count += 1
    print(combo_list)
    num_of_try = input('試行回数を入力してください\n')
    print('{}回試行します'.format(int(num_of_try)))
    result = combo_caliculate(
        number_of_try=int(num_of_try),
        deck=deck,
        openning_hand_drawn=int(openning_hand_drawn),
        combo_list=combo_list,
    )  # プログレスバーを入れたいが標準ライブラリだけで解決したいためオミット
    print('初手に揃う確率：{}%'.format(result))


if __name__ == '__main__':  # importされることは想定されていないがお約束のため
    standard_input_main(argv=sys.argv)

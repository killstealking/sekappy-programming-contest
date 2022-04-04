import decimal
import random  # 乱数としてのrandomの信頼度についての判断は使用者に委ねる
from collections import Counter

import PySimpleGUI as sg

import deck_parser


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
        # プログレスを出すSimpleGUIの機能
        sg.OneLineProgressMeter('コンボ試行中', i + 1, number_of_try, 'key')
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


def main_gui():
    '''
    GUIを司る部分
    '''
    sg.theme('Reddit')  # 見た目、いわゆるテーマを設定する
    combo_list = []
    # GUI上に実際に表示される部分
    layout = [
        [sg.Text('デッキリストとデッキ枚数、コンボカードを指定してください')],
        [
            sg.Text('デッキリスト', size=(15, 1)),
            sg.Input(key='deck_list_path', enable_events=True),
            sg.FileBrowse(
                'ファイルを選択',
                key='input_deck_list',
                enable_events=True
            ),
        ],
        [
            sg.Text('デッキ枚数', size=(15, 1)),
            sg.InputText(default_text='', size=(10, 1), key='number_of_deck'),
        ],
        [
            sg.Text('コンボカード', size=(15, 1)),
            sg.Listbox(
                combo_list,
                size=(35, 7),
                select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                key='combo_list',
            ),
        ],
        [
            sg.Text('計算回数', size=(15, 1)),
            sg.InputText(default_text=1000, size=(10, 1), key='number_of_try'),
        ],
        [
            sg.Text('初手枚数', size=(15, 1)),
            sg.InputText(
                default_text=7,
                size=(10, 1),
                key='openning_hand_drawn'
            ),
        ],
        [sg.Button('計算', key='calculate'), sg.Button('終了', key='terminate')],
        [sg.Output(size=(80, 20))],
    ]

    # Windowを作成
    window = sg.Window('コンボ初手揃う君.exe', layout)

    # イベントを待つ
    while True:
        event, values = window.read()
        if (
            event == sg.WIN_CLOSED or event == 'terminate'
        ):  # GUIが閉じられたとき、または終了を押された際に終了する
            break
        elif event == 'deck_list_path':  # デッキリストファイルを選択された際
            if values['input_deck_list'] == '':  # デッキリスト選択をキャンセルされた際、ルーチンに戻る
                continue
            deck_list = deck_parser.get_main_board(values['input_deck_list'])
            deck = deck_parser.create_deck_from_deck_list(deck_list)
            num_of_deck = sum(deck_list.values())
            window['combo_list'].Update(
                values=deck
            )  # デッキリストファイルから、コンボカードを選択する用のデッキ一覧を表示する
            # デッキリストファイルからデッキ枚数を計算する
            window['number_of_deck'].Update(num_of_deck)
        elif event == 'calculate':
            path = values['input_deck_list']
            combo_list = values['combo_list']
            deck_list = deck_parser.get_main_board(path)
            deck = deck_parser.create_deck_from_deck_list(deck_list)
            result = combo_caliculate(
                number_of_try=int(values['number_of_try']),
                deck=deck,
                openning_hand_drawn=int(values['openning_hand_drawn']),
                combo_list=combo_list,
            )
            print('初手に揃う確率：{}%'.format(result))

    window.close()  # 終了


if __name__ == '__main__':
    ''''
    importされることは想定されていないがお約束のため
    '''
    main_gui()

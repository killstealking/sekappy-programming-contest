import PySimpleGUI as sg

import deck_parser
import shuffler
import runs_test


def main_gui():
    """
    GUIを司る部分
    """
    sg.theme("Reddit")  # 見た目、いわゆるテーマを設定する
    init_info = "デッキリストとシャッフル方法、シャッフル回数を指定してください"
    shuffle_dict = {
        "pile": "パイル",
        "hindu": "ヒンドゥー",
        "riffle": "リフル",
        "over_hand": "オーバーハンド",
    }
    deck = []  # シャッフル後のデッキを格納
    deck_runs_test = []  # シャッフル後のRUns Testの結果
    original_deck = []  # シャッフル前のデッキを格納
    original_deck_runs_test = []  # シャッフル前のRuns Testの結果
    original_deck_key_dict = {}  # シャッフル前のユニークカードに数字を割り振ったもの
    # シャッフル前デッキ用レイアウト
    original_deck_col = [
        [sg.Text("シャッフル前", size=(15, 1))],
        [
            sg.Listbox(
                original_deck,
                size=(40, 30),
                key="original_deck_viewer",
                select_mode=sg.LISTBOX_SELECT_MODE_BROWSE,
            )
        ],
    ]

    # シャッフル後デッキ用レイアウト
    shuffle_deck_col = [
        [sg.Text("シャッフル後", size=(15, 1))],
        [
            sg.Listbox(
                deck,
                size=(40, 30),
                key="shuffled_deck_viewer",
                select_mode=sg.LISTBOX_SELECT_MODE_BROWSE,
            )
        ],
    ]
    # GUI上に実際に表示される部分
    layout = [
        [sg.Text(init_info, key="info")],
        [
            sg.Text("デッキリスト", size=(15, 1)),
            sg.Input(key="deck_list_path", enable_events=True),
            sg.FileBrowse("ファイルを選択", key="input_deck_list", enable_events=True),
        ],
        [sg.Radio(item[1], key=item[0], group_id="0") for item in shuffle_dict.items()],
        [
            sg.Text("シャッフル回数", size=(15, 1)),
            sg.InputText(default_text=10, size=(10, 1), key="number_of_shuffle"),
            sg.Button("デッキ初期化", key="reset_deck"),
        ],
        [
            sg.Column(original_deck_col, element_justification="c"),
            sg.Column(shuffle_deck_col, element_justification="c"),
        ],
        [
            sg.Text("シャッフル前P-Value", size=(30, 1)),
            sg.Text(original_deck_runs_test, size=(30, 1), key="original_p_value"),
        ],
        [
            sg.Text("シャッフル後P-Value", size=(30, 1)),
            sg.Text(deck_runs_test, size=(30, 1), key="p_value"),
        ],
        [sg.Button("シャッフル", key="shuffle"), sg.Button("終了", key="terminate")],
    ]

    # Windowを作成
    window = sg.Window("Shuffler.exe", layout, resizable=True)

    # イベントを待つ
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "terminate":
            # GUIが閉じられたとき、または終了を押された際に終了する
            break
        elif event == "deck_list_path":  # デッキリストファイルを選択された際
            if values["input_deck_list"] == "":  # デッキリスト選択をキャンセルされた際、ルーチンに戻る
                continue
            deck_list = deck_parser.get_main_board(values["input_deck_list"])
            deck = deck_parser.create_deck_from_deck_list(deck_list)
            original_deck = deck
            original_deck_key_dict = runs_test.create_deck_key_dict(deck)
            original_deck_runs_test = runs_test.runstest(
                runs_test.create_float_deck_list(
                    deck=deck, deck_key_dict=original_deck_key_dict
                )
            )
            window["original_deck_viewer"].Update(original_deck)  # デッキの中身を表示する
            window["original_p_value"].Update(original_deck_runs_test[1])
        elif event == "reset_deck":  # デッキをリセットする
            deck = []
            original_deck = deck
            window["original_deck_viewer"].Update(original_deck)
            window["shuffled_deck_viewer"].Update(original_deck)
            window["deck_list_path"].Update("")
        elif event == "shuffle":
            if values["input_deck_list"] == "":  # デッキリスト選択をしていない場合
                window["info"].Update("デッキリストを選択してください", text_color="red")
                continue
            try:  # 数字のバリデーション
                number_of_shuffle = int(values["number_of_shuffle"])
            except ValueError:
                window["info"].Update("シャッフル回数を半角整数で入力してください", text_color="red")
                continue
            if deck == []:  # すでにシャッフルされているデッキがなければオリジナルをシャッフル
                deck_list = deck_parser.get_main_board(values["input_deck_list"])
                deck = deck_parser.create_deck_from_deck_list(deck_list)
            if values["pile"]:  # パイルであれば
                result = shuffler.pile_shuffle(
                    deck=deck, number_of_shuffle=number_of_shuffle
                )
                window["pile"].Update(True)
            elif values["hindu"]:  # ヒンドゥーであれば
                result = shuffler.hindu_shuffle(
                    deck=deck, number_of_shuffle=number_of_shuffle
                )
                window["hindu"].Update(True)
            elif values["riffle"]:  # リフルであれば
                result = shuffler.riffle_shuffle(
                    deck=deck, number_of_shuffle=number_of_shuffle
                )
                window["riffle"].Update(True)
            elif values["over_hand"]:  # オーバーハンドであれば
                result = shuffler.over_hand_shuffle(
                    deck=deck, number_of_shuffle=number_of_shuffle
                )
                window["over_hand"].Update(True)
            else:  # シャッフル方法が選ばれていない場合
                window["info"].Update("シャッフル方法を選択してください", text_color="red")
                continue
            window["info"].Update(init_info, text_color="black")  # エラー表示を正常表示に戻す
            deck = result
            deck_runs_test = runs_test.runstest(
                runs_test.create_float_deck_list(
                    deck=deck, deck_key_dict=original_deck_key_dict
                )
            )
            window["p_value"].Update(deck_runs_test[1])
            window["shuffled_deck_viewer"].Update(deck)
    window.close()  # 終了


if __name__ == "__main__":
    """
    importされることは想定されていないがお約束のため
    """
    main_gui()

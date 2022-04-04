# Sekappyプログラミングチャレンジ 部門(1) コンボが初手に揃う確率の計算ツール
モンテカルロ法を用いたコンボが初手に揃う確率を計算するツールです
# Features
GUIで完結する、試行回数を指定できる計算ツール
# Requirement
 [Pipenv](https://github.com/pypa/pipenv)
 [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)

同封のSample_deck_a.txtのような
4 YYYYYYYY
3 XXXXXXXX
数字 カード名の順で書かれている、かつメインボードとサイドボードが段落として別れているデッキリスト
サンプルとしてsample_deck_*.txtを3種添付
# Installing
```
pipenv sync
```
# Usage
```
pipenv run gui_combo
```
GUIを用いて必要な項目を入力後、計算ボタンをクリック
# Auther
Keiske Iwamura/岩村 圭祐
# License
[MIT license](https://en.wikipedia.org/wiki/MIT_License)
# Sekappyプログラミングチャレンジ 部門(2) デッキシャッフルツール
4種のシャッフル方法を選べて、シャッフルする前(デッキリストの状態)とシャッフル後を比較できるツールです
# Features
直感的GUIで完結するシャッフルツール, [Runs Test](https://en.wikipedia.org/wiki/Wald%E2%80%93Wolfowitz_runs_test)も同時に行います
# Requirement
 [Pipenv](https://github.com/pypa/pipenv)
 [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI)
 [statsmodels](https://www.statsmodels.org/stable/index.html)
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
pipenv run gui_shuffle
```
GUIを用いて必要な項目を入力後、シャッフルボタンをクリック
シャッフルボタンを押すたびにシャッフル回数分シャッフルします
# Auther
Keiske Iwamura/岩村 圭祐
# License
[MIT license](https://en.wikipedia.org/wiki/MIT_License)
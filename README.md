# 実験第２　前半で使用したコードとデータ
どのコードも整理中なので早いうちに実行できる形で修正します。
実験データもこのレポジトリで見れるようにします。
## data
XX_Y_Z.bag or XX_Y_Z.csv という名前のファイルはそれぞれ以下のような条件で撮ったデータです.
1. XX
   1. 01 : d = 0.1
   2. 02 : d = 0.2
   3. 04 : d = 0.4
2. Y
   1. 2 : 入力でinput1,2のみを使用
   2. 4 : 入力でinput1,2,3,4(全て)使用
3. Z
   1. A : 入力が[0,400]
   2. B : 入力が[100,300]

_2024-05-16-15-09-44.bagは予備実験のデータ
### bagファイルのデータについて
- 入力の参照値
  pressure/cal_and_ref_value/data.36 - 39

- 入力の計測値
  pressure/cal_and_ref_value/data.0 - 3

- 圧力センサの計測値(フィルタ前)
  pressure/value/data.8 - 11

- フィルタした計測値(出力)
  pressure/cal_and_ref_value/data.8 - 11

フィルタや制御のパラメータなどの詳細はrosのlaunchファイル(~~~_chada.launch)を見てください

## calculate_MC
XX_4_Z.csvに対してMC_kのグラフを作成するコード. 詳しくはコードのコメントを読んでください.

## estimate_CLE
コードの前半では入力と出力の値の範囲が異なるので, どちらも平均0, 分散1になるように正規化して状態空間での近傍k点を探して保存している.
後半はヤコビアンの推定値を求めて, QR分解でCLEを推定している.

## other
* plot_inputs.py
  入出力をplotするコード
* plot_from_bag.m
  bagファイルからplotするコード, matlabで実行



# README

## ファイル説明
- main.py

  発言モジュール

  ngramで解析した結果からランダムに発言を行う

  ```
  Usage: python main.py
  ```

- wolf\_ngram.sh

  zinrou.csvに書かれている内容から、ngram\_output/h0\_ngram<数値>.txtを生成する

  ngram.py、ngram\_output、zinrou.csvに依存

  ```
  Usage: cat zinrou.csv | wolf\_ngram.sh [ファイルの何行から始めるか]
  ```

- ngram.py

  ngramを行う

  ```
  Usage: cat ファイル | python ngram.py <数値>
  ```

- ngram\_output/

  ngramの結果

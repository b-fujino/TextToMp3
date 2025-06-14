# TextToMP3

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-completed-green)

## 概要

このプロジェクトはGoogle TTS APIを使って，テキストを音声でアウトプットするパイソンコードを作成しています．

## 使い方

### Google TTS APIの取得
予めGoogle TTS API Keyを取得してください．取得方法はこちらの記事を参考にしてください．

https://qiita.com/fujino-fpu/items/f5deca52e8f708867f79

### 環境変数の設定
取得したAPI Keyは環境変数にGOOGLE_TTS_API_KEYとして保存してください．
同じフォルダに.envファイルを作成して
```
GOOGLE_TTS_API_KEY=*****************
```
と記載してもらっても構いません．


### 使い方
```
python TexttoSpeech.py -f text.txt 
```

デフォルトの言語はGB英語です．

ファイルは中身がテキストなのであれば，拡張子はどのようなものでも構いません．例えば，マークダウンファイルも与えることができます．ただ，あくまでテキストとして読み込んで，それをそのままGoogle TTS に流すので，記号などはそのまま読み上げられる可能性があります（Google TTSの仕様による）．

また，複数ファイルに分けたい場合，ファイルの切れ目に`[eop]`と書き込んでください．その場所でファイルが切り分けられます．

引数は色々とあります．以下で引数のヘルプが表示されます

```
python TexttoSpeech.py -h
```


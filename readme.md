# 音素セグメンテーションAPI

## 実行環境

- Docker
- Docker Compose

### コンテナ内実行環境
- Python 3.9.0
- pip 20.2.4
- Perl 5.28.1
- Julius 4.6
#### 使用webフレームワーク
- FastAPI

<br>

## 起動方法

### 1. リポジトリのクローン

```
git clone --recursive {クローンしたいリポジトリ}
```
※ --recursive オプションでサブモジュールも一緒にクローン

### 2. ビルド
```
docker-compose build
```

### 3. コンテナ起動
```
docker-compose up -d
```
`docker-compose.yml`にてアプリケーションの起動コマンドが定義されているので、
コンテナを起動すると自動でAPIアプリケーションも起動
<br>

以上

<br>

## APIドキュメント

Swaggerによる表示
```
{ホストIP or ドメイン}:8000/docs
```

ReDocによる表示
```
{ホストIP or ドメイン}:8000/redoc
```

<br>

## API使い方 サンプルコード
https://github.com/KaijiS/phoneme_segmentation/blob/master/app/sample/sample.ipynb

<br>

## リクエストデータの条件とTips

### wavedata
wavファイルのバイナリをbase64形式でエンコードした文字列<br>
wavファイルの条件:
- サンプリングレート: 16kHz
- 量子化bit: 16bit
- 1ch(モノラル)
- PCM（無圧縮）形式

### textdata
書き起こしテキスト
「ひらがな」で１行で記述します。
```
きょーわいいてんきです
```
※ 「きょう」ではなく「きょー」、「は」ではなく「わ」 音のままをひらがなで記述します

文中にポーズを入れたいときは、その位置でスペースで区切って sp を入れて 下さい（自動挿入には対応していません）。
```
きょーわ sp いいてんきです
```

ひらがなは内部で音素列に変換されます。変換がうまくいかないときは音素列 で直接指定することも可能です。
```
ky o: w a i i t e N k i d e s u
```

### disableSilenceAtEnds
"0": 実行時に文頭・文末に自動的に無音(silB, silE)を挿入してアラインメントが行われます。(デフォルト)<br>
"1": 文頭・文末に無音(silB, silE)を挿入せずアラインメントが行われます.

<br>

## Appendix

### コンテナに入る
```
docker exec -it phoneme_segmentation_api bash
```

### コンテナから出る
```
exit
```

### コンテナ内でapp起動
```
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### ログの場所
障害があればここを確認
```
/var/log/{日付}.log
```
lessコマンドで閲覧するのがおすすめ<br>
lessコマンド使い方 → https://qiita.com/inokou/items/a73bac8c7e03951d07be
```
less {日付}.log
```
※ ログファイル内の時間はUTCなので日本時間への変換は9時間を加算してください

### コンテナ内でサンプルnotebookの起動
```
jupyter-lab --no-browser --ip 0.0.0.0 --port 4000
```
指示されたtoken付きのURLをブラウザで起動<br>
例 )<br>
```
http://ce00a76dca26:4000/?token=693784dde4cc376b5a5d1156b2356d3a6258d29cdab93b87
 or http://127.0.0.1:4000/?token=693784dde4cc376b5a5d1156b2356d3a6258d29cdab93b87
```

<br>

## Juliusについて
### Julius
https://github.com/julius-speech/julius

### Segmentation-Kit
https://github.com/julius-speech/segmentation-kit
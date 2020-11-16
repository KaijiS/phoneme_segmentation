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
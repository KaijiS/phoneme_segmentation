from fastapi import FastAPI
from controllers import phoneme_segmentation
from fastapi.responses import ORJSONResponse

import logging
import datetime

# ログ出力先設定
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
logging.basicConfig(
  format='%(levelname)s %(asctime)s: %(message)s',
  datefmt='%Y-%m-%d %H:%M:%S-%Z',
  filename=f'/var/log/{now.strftime("%Y%m%d")}.log',
  level=logging.DEBUG
)


app = FastAPI(
  title='音素セグメンテーションAPI',
  description='Juliusを用いた音素ラベリングセグメンテーションの実行',
  version='0.1',
  # デフォルトの応答クラスを指定: ORJSONResponseｰ>パフォーマンス高い
  default_response_class=ORJSONResponse
)

# ルーティングをinclude
app.include_router(phoneme_segmentation.router)

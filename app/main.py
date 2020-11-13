from fastapi import FastAPI
from controllers import phoneme_segmentation
from fastapi.responses import ORJSONResponse

app = FastAPI(
  title='音素セグメンテーションAPI',
  description='Juliusを用いた音素ラベリングセグメンテーションの実行',
  version='0.1',
  # デフォルトの応答クラスを指定: ORJSONResponseｰ>パフォーマンス高い
  default_response_class=ORJSONResponse
)

# ルーティングをinclude
app.include_router(phoneme_segmentation.router)

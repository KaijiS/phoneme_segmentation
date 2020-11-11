from fastapi import FastAPI
from controllers import phoneme_segmentation

app = FastAPI(
  title='音素セグメンテーションAPI',
  description='Juliusを用いた音素ラベリングセグメンテーションの実行',
  version='0.1'
)

# ルーティングをinclude
app.include_router(phoneme_segmentation.router)

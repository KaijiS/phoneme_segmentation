from pydantic import BaseModel
from pydantic import Field

class OriginalVoiceWaveform(BaseModel):

  filename: str = Field(..., description='ファイル名')
  wavedata_base64: str = Field(..., description='音声データ(base64形式)', alias='wavedata')
  textdata: str = Field(..., description='テキストデータ')

  class Config:
    '''
    swaggerのサンプル欄に表示する例
    '''
    schema_extra = {
        'example': {
            'filename': 'original_voice_filename.wav',
            'wavedata': 'data:audio/wav;base64,//uwYAAP9IRoP・・・・・・・・・・・・・・・・AAAAA=',
            'textdata': 'ここに sp よみかたのてきすとでーたお sp だいにゅうします'
        }
    }
from pydantic import BaseModel
from pydantic import Field

class Speech(BaseModel):

  filename: str = Field(..., description='ファイル名')
  wavedata_base64: str = Field(..., description='音声データ(base64形式)', alias='wavedata')
  textdata: str = Field(..., description='テキストデータ')
  disable_silence_at_ends: str = Field("0", description='segmentation-kitのreadme.mdを参照', alias='disableSilenceAtEnds')

  class Config:
    '''
    swaggerのサンプル欄に表示する例
    '''
    schema_extra = {
        'example': {
            'filename': 'original_voice_filename.wav',
            'wavedata': 'data:audio/wav;base64,//uwYAAP9IRoP・・・・・・・・・・・・・・・・AAAAA=',
            'textdata': 'ここに sp よみかたのてきすとでーたお sp だいにゅうします',
            'disableSilenceAtEnds': '0'
        }
    }
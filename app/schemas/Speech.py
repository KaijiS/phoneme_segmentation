from pydantic import BaseModel
from pydantic import Field

class Speech(BaseModel):

  filename                : str = Field(..., description='ファイル名'                                                      , example='original_voice_filename.wav')
  wavedata_base64         : str = Field(..., description='音声データ(base64形式)'             , alias='wavedata'            , example='UklGRnYeAABXQVZFZm10IBAAAAABAAEAgD4AAAB9A...')
  textdata                : str = Field(..., description='テキストデータ'                                                   , example='ここに sp よみかたのてきすとでーたお sp だいにゅーします')
  disable_silence_at_ends : str = Field("0", description='segmentation-kitのreadme.mdを参照' , alias='disableSilenceAtEnds', example='0')

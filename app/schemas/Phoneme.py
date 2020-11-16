from pydantic import BaseModel
from pydantic import Field

class Phoneme(BaseModel):

  phoneme     : str   = Field(..., description='音素'                       ,                    example='a')
  wavedata    : str   = Field(..., description='音素部分wavデータ(base64形式)',                    example='UklGRnYeAABXQVZFZm10IBAAAAABAAEAgD4AAAB9A...')
  filename    : str   = Field(..., description='ファイル名'                  ,                    example='phonemefilename_a_00112233.wav')
  start_time  : float = Field(..., description='対象音素開始時間'             , alias='startTime', example=0.0056)
  end_time    : float = Field(..., description='対象音素終了時間'             , alias='endTime'  , example=0.1234)

  class Config:
    allow_population_by_alias = True
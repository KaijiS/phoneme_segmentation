from pydantic import BaseModel
from pydantic import Field

class Phoneme(BaseModel):

  phoneme: str = Field(..., description='音素')
  wavedata: str = Field(..., description='音素部分wavデータ(base64形式)')
  filename: str = Field(..., description='ファイル名')
  array_index_from: int = Field(description='対象音素開始配列index', alias='arrayIndexFrom')
  array_index_to: int = Field(description='対象音素終了配列index', alias='arrayIndexTo')
  n_score: float = Field(description='尤度', alias='nScore')

  class Config:
    allow_population_by_alias = True
    '''
    swaggerのサンプル欄に表示する例
    '''
    schema_extra = {
        'example': {
            'phoneme': 'a',
            'wavedata': 'data:audio/wav;base64,//uwYAAP9IRoP・・・・・・・・・・・・・・・・AAAAA=',
            'filename': 'phonemefilename_a_00112233.wav',
            'arrayIndexFrom': 23,
            'arrayIndexTo': 48,
            'nScore': 0.8721
        }
    }


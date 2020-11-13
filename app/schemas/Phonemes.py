from pydantic import BaseModel
from pydantic import Field
from typing import List

from schemas.Phoneme import Phoneme

class Phonemes(BaseModel):
  phonemes    : List[Phoneme] = Field(...)
  julius_lab  : str           = Field(..., description='juliusのsegmentation-kiが出力したlabファイルの内容', alias='juliusLab', example='.labの内容')
  julius_log: str = Field(..., description='juliusのsegmentation-kiが出力したlogファイルの内容', alias='juliusLog', example='.logの内容')

  class Config:
    allow_population_by_alias = True

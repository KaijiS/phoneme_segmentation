from fastapi import APIRouter
from typing import List

from schemas.OriginalVoiceWaveform import OriginalVoiceWaveform
from schemas.Phoneme import Phoneme

from services import phoneme_segmentation_service

router = APIRouter()

@router.get('/')
async def connection_check() -> dict[str: str]:
  '''
  意思疎通確認用API
  '''
  return {'接続':'確認！'}


@router.post('/', response_model=List[Phoneme], status_code=201)
async def phoneme_segmentation(originalVoiceWaveform: OriginalVoiceWaveform) -> List[Phoneme]:
  '''
  音素セグメンテーションの実行API
  '''

  return phoneme_segmentation_service.phoneme_segmentation(originalVoiceWaveform)
from fastapi import APIRouter
from typing import List

from schemas.OriginalVoiceWaveform import OriginalVoiceWaveform
from schemas.Phoneme import Phoneme

from services.phoneme_segmentation_service import PhonemeSegmentationService

router = APIRouter()

@router.get('/')
def connection_check() -> dict[str: str]:
  '''
  意思疎通確認用API
  '''
  return {'接続':'確認！'}


@router.post('/', response_model=List[Phoneme])
def phoneme_segmentation(originalVoiceWaveform: OriginalVoiceWaveform) -> List[Phoneme]:
  '''
  音素セグメンテーションの実行API
  '''

  return PhonemeSegmentationService.phoneme_segmentation(originalVoiceWaveform)
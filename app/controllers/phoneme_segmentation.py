from fastapi import APIRouter

from schemas.Speech import Speech
from schemas.Phonemes import Phonemes

from services import phoneme_segmentation_service

router = APIRouter()

@router.get('/')
async def connection_check() -> dict[str: str]:
  '''
  意思疎通確認用API
  '''
  return {'接続':'確認！'}


@router.post('/', response_model=Phonemes, status_code=201)
async def phoneme_segmentation(speech: Speech) -> Phonemes:
  '''
  音素セグメンテーションの実行API
  '''

  return phoneme_segmentation_service.phoneme_segmentation(speech)
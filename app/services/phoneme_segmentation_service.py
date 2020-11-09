from schemas.OriginalVoiceWaveform import OriginalVoiceWaveform
from schemas.Phoneme import Phoneme
from typing import List

class PhonemeSegmentationService:

  @staticmethod
  def phoneme_segmentation(originalVoiceWaveform: OriginalVoiceWaveform) -> List[Phoneme]:
    ''' 音素セグメンテーションを実行

    Parameters
    --------------
    originalVoiceWaveform: OriginalVoiceWaveform

    Returns
    --------------
    List[Phoneme]
    '''

    phonemes: List[Phoneme] =  []
    for i in range(2):
      phoneme: Phoneme = Phoneme(
        phoneme = 'a',
        wavedata = 'wavedata_base64',
        filename = 'filename_a_00001111000.wav',
        array_index_from = 20,
        array_index_to = 39,
        n_score=0.987
      )
      phonemes.append(phoneme)

    return phonemes
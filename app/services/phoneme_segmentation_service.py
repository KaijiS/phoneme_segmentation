from schemas.OriginalVoiceWaveform import OriginalVoiceWaveform
from schemas.Phoneme import Phoneme
from typing import List

import base64

from components.WaveData import WaveData

def phoneme_segmentation(originalVoiceWaveform: OriginalVoiceWaveform) -> List[Phoneme]:
  ''' 音素セグメンテーションを実行

  Parameters
  --------------
  originalVoiceWaveform: OriginalVoiceWaveform

  Returns
  --------------
  List[Phoneme]
  '''

  # TODO 音声ファイルの中身確認
  check_wavefile(originalVoiceWaveform.wavedata_base64)

  # TODO 音声ファイルとテキストファイル保存

  # TODO perl実行(kitをgit cloneしてくる)

  # TODO 終了 or どこかで失敗した場合保存したファイルすべて削除(finally句を使用)

  # TODO 型にはめてレスポンス

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



def check_wavefile(wavedata_base64: str):

  # まずバイナリに変更
  binary: bytes = base64.b64decode(wavedata_base64.encode("UTF-8"))
  wavedata: WaveData = WaveData(binary)
  print(wavedata.riff)
  print(wavedata.format)
  wavedata.validate()
  return
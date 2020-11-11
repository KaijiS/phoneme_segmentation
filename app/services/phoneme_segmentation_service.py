from schemas.Speech import Speech
from schemas.Phoneme import Phoneme
from typing import List

import os
import sys
import datetime
import base64
import subprocess

from components.WaveData import WaveData
from utils import file_read_write

def phoneme_segmentation(speech: Speech) -> List[Phoneme]:
  ''' 音素セグメンテーションを実行

  Parameters
  --------------
  speech: Speech

  Returns
  --------------
  List[Phoneme]
  '''
  # 音声ファイルをバイナリに変換
  wave_binary: bytes = base64.b64decode(speech.wavedata_base64.encode("UTF-8"))

  # 音声ファイルの検証
  # TODO 検証
  # validate_wavefile(wave_binary)

  # ファイル名から拡張子を除いたものをベースとする
  base_filename = speech.filename.lower().replace('.wav', '')

  # 音声ファイルとテキストファイル保存し保存先のディレクトリpathを取得
  dir_path = write_wavefile_and_textfile(
    base_filename,
    wave_binary,
    speech.textdata
  )

  # perl実行
  run_segmentation_julius(dir_path, speech.disable_silence_at_ends)

  # TODO 分解された音素音声ファイルを保存するためのディレクトリを準備

  # TODO 音声波形を音素に分解してファイル出力

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



def validate_wavefile(wave_binary: bytes):
  ''' 音声ファイルの検証

  Parameters
  --------------
  wave_binary: 音声バイナリファイル
  '''

  wavedata: WaveData = WaveData(wave_binary)
  wavedata.validate()

  return


def write_wavefile_and_textfile(
  base_filename : str,
  wave_binary: bytes,
  textdata: str
) -> str:
  ''' 音声ファイルとテキストファイルの書き出し
  Parameters
  --------------
  base_filename:  音声ファイル名(拡張子なし)
  wave_binary:    音声バイナリファイル
  textdata:       textデータ内容

  Returns
  --------------
  保存先ディレクトリ
  '''

  # 現在のタイムスタンプを取得してそれを利用した名のディレクトリを作成
  now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
  dir_path = f'.tmp/{now.strftime("%Y%m%d%H%M%S")}_{base_filename}'
  os.makedirs(dir_path)

  text_filepath = f'{dir_path}/{base_filename}.txt'
  wave_filepath = f'{dir_path}/{base_filename}.wav'

  # テキストファイル書き出し
  file_read_write.write_text(
    text_filepath,
    textdata
  )

  # 音声バイナリファイル書き出し
  file_read_write.write_binary(
    wave_filepath,
    wave_binary
  )

  return dir_path


def run_segmentation_julius(dir_path: str, disable_silence_at_ends: str = '0'):
  ''' segmentation-kit(perl)の実行

  Parameters
  --------------
  dir_path: 解析対象音声ファイルとテキストファイルが格納されているディレクトリ
  disable_silence_at_ends:
        実行時には文頭・文末に自動的に無音(silB, silE)を挿入してアラインメント が行われます。
        この機能を止めたい場合は'1'をセットしてから以下を実行してください。
        (デフォルト: '0')
  '''
  try:
    subprocess.run(
      [
        "perl",
        "segment_julius.pl",
        "../../" + dir_path,
        disable_silence_at_ends
      ],
      cwd='components/segmentation-kit',
      check=True
    )

  except subprocess.CalledProcessError:
    # print('セグメンテーションのの実行に失敗しました', file=sys.stderr)
    HTTPException(status_code=500, detail=sys.stderr)

  finally:
    # TODO ファイル削除
    print('finally')

  return

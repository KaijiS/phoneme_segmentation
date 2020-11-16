from schemas.Speech import Speech
from schemas.Phoneme import Phoneme
from schemas.Phonemes import Phonemes
from fastapi import HTTPException
from typing import List

import os
import sys
import datetime
import base64
import subprocess
import logging

from components.WaveData import WaveData
from utils import fileutil
from models.dto.PhonemeDto import PhonemeDto

def phoneme_segmentation(speech: Speech) -> List[Phoneme]:
  ''' 音素セグメンテーションを実行

  Parameters
  --------------
  speech: Speech

  Returns
  --------------
  List[Phoneme]
  '''

  try:

    logging.info('--------Phoneme Segmentation Service Start-----------')
    logging.info(f'File Name: {speech.filename}')

    # 音声ファイルをバイナリに変換
    wave_binary: bytes = base64.b64decode(speech.wavedata_base64.encode("UTF-8"))

    # 音声ファイルの検証
    validate_wavefile(wave_binary)
    logging.info(f'Wave File Validation: OK')

    # ファイル名から拡張子を除いたものをベースとする
    base_filename = speech.filename.lower().replace('.wav', '')

    # 音声ファイルとテキストファイル保存し保存先のディレクトリpathを取得
    dir_path = write_wavefile_and_textfile(
      base_filename,
      wave_binary,
      speech.textdata
    )
    logging.info(f'writing Original File: OK')

    # 音素セグメンテーション perl実行
    run_segmentation_julius(dir_path, speech.disable_silence_at_ends)
    logging.info(f'Segmentation-kit: Complete')

    # 音声波形を音素に分解してファイル出力しその音素ファイル情報を受取る
    phoneme_dto_list: List[PhonemeDto] = divide_into_phoneme_and_write_wave_file(dir_path, base_filename)
    logging.info(f'Segmentation and Writing Phoneme Wave File : Complete')

    # レスポンス準備
    phoneme_list: List[Phoneme] =  []
    for phoneme_dto in phoneme_dto_list:

      # 先に音素ファイルを読み込みbase64形式に変換
      wavedate_base64 = base64.b64encode(fileutil.read_binary(phoneme_dto.filepath)).decode("UTF-8")
      # レスポンス用スキーマに詰め込み
      phoneme: Phoneme = Phoneme(
        phoneme = phoneme_dto.phoneme,
        wavedata = wavedate_base64,
        filename = phoneme_dto.filename,
        start_time = phoneme_dto.start_time,
        end_time = phoneme_dto.end_time
      )
      phoneme_list.append(phoneme)

    # juliusの出力labデータを準備
    lab_text: str = fileutil.read_text(f'{dir_path}/{base_filename}.lab')
    # juliusの出力logデータを準備
    log_text: str = fileutil.read_text(f'{dir_path}/{base_filename}.log')

    phonemes = Phonemes(
      phonemes    = phoneme_list,
      julius_lab  = lab_text,
      julius_log  = log_text
    )

    logging.info(f'Response Preperation : OK')

    logging.info('--------Phoneme Segmentation Service Finished-----------')

    return phonemes

  except:
    # エラーハンドリング
    raise HTTPException(status_code=500, detail='サーバエラー')

  finally:
    # 正常でもエラーがあってもファイル削除
    if 'dir_path' in locals():
      fileutil.removeDir(dir_path)



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
  fileutil.write_text(
    text_filepath,
    textdata
  )

  # 音声バイナリファイル書き出し
  fileutil.write_binary(
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
    HTTPException(status_code=500, detail=sys.stderr)

  return


def divide_into_phoneme_and_write_wave_file(dir_path: str, base_filename: str):
  ''' segmentation-kitの結果ファイルをもとに 原音声ファイルを分割して保存

  Parameters
  --------------
  dir_path      : 解析対象音声ファイルとテキストファイル、
                  及びsegmentation-kitの結果ファイル(log, lab)が格納されているディレクトリ
  base_filename : 解析対象音声ファイルとテキストファイル、
                  及びsegmentation-kitの結果ファイル(log, lab)の拡張子を除くファイル名

  Returns
  --------------
  List[PhonemeDto] 音素ファイル情報
  '''

  # 音声データを取得
  wave_filepath: str = f'{dir_path}/{base_filename}.wav'
  wave_array, fs, times_array = fileutil.read_wave_file(wave_filepath)

  # labファイル読み込み
  lab_filepath: str = f'{dir_path}/{base_filename}.lab'
  lab_text: str = fileutil.read_text(lab_filepath)

  # 音素データを保存するディレクトリ作成
  phoneme_output_dir: str = f'{dir_path}/phoneme'
  os.makedirs(phoneme_output_dir)

  # 戻り値用リスト
  phoneme_dto_list: List[PhonemeDto] = []

  # 改行で区切り、それぞれリストの要素とする
  lab_text_to_list = lab_text.split('\n')
  # 上記リストの要素を一つずつ(labファイルの内容を1行ずつ)読みながら処理
  for lab_text_oneline in lab_text_to_list:

    # スペース区切りで音素開始時間, 音素終了時間, 音素情報を抽出
    phoneme_start_time, phoneme_end_time, phoneme = lab_text_oneline.split(' ')
    # 対象の波形を切り出し
    phoneme_wav_array = wave_array[int(float(phoneme_start_time)*fs):int(float(phoneme_end_time)*fs)+1]
    # wavファイルに変換し保存
    phoneme_filename = f'{base_filename}_{phoneme}_{str(int(float(phoneme_start_time)*(10**6)))}us.wav'
    phoneme_filepath = f'{phoneme_output_dir}/{phoneme_filename}'
    fileutil.write_wave_file(
      phoneme_filepath,
      phoneme_wav_array,
      fs=fs
    )

    phonemeDto: PhonemeDto = PhonemeDto(
      phoneme     = phoneme,
      filepath    = phoneme_filepath,
      filename    = phoneme_filename,
      start_time  = phoneme_start_time,
      end_time    = phoneme_end_time
    )

    phoneme_dto_list.append(phonemeDto)

  return phoneme_dto_list
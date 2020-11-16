import struct
from fastapi import HTTPException
import logging

class WaveData:
  '''
  waveファイルに関する情報(waveファイルの規格を基に構成)

  フィールド変数
  bin:                    bytes   バイナリデータ
  riff:                   str     RIFF識別子 “RIFF”(0x52494646)で固定。
  format:                 str     フォーマット WAVファイルの場合は“WAVE”(0x57415645)で固定。AVIファイルの場合は“AVI”が入る
  fmt:                    str     fmt識別子 “fmt “(0x666D7420)で固定
  audioFormat:            int     音声フォーマット 非圧縮のリニアPCMフォーマットは1(0x0100) 他、例えばA-lawは6、μ-lawは7
  ch:                     int     チャンネル数 モノラルは1(0x0100)、ステレオは2(0x0200)
  fs:                     int     サンプリング周波数(Hz) 8kHzの場合は(0x401F0000)、44.1kHzの場合なら(0x44AC0000)
  quantization_bit:       int     量子化ビット数(ビット／サンプル) 1サンプルに必要なビット数 8ビットの場合は8(0x0800)、16ビットの場合は16(0x1000)など
  subchunk_identifier:    str     サブチャンク識別子 “data” (0x64617461)で固定
  subchunk_size_of_wave:  int     サブチャンクザイズ 波形データのバイト数(総ファイルサイズ – 126)
  '''

  def __init__(self, wavedata_binary: bytes):
    self.bin                  : bytes = wavedata_binary
    self.riff                 : str   = hex(struct.unpack('>I', wavedata_binary[0:4])[0]).lower()
    self.format               : str   = hex(struct.unpack('>I', wavedata_binary[8:12])[0]).lower()
    self.fmt                  : str   = hex(struct.unpack('>I', wavedata_binary[12:16])[0]).lower()
    self.audioFormat          : int   = int(struct.unpack('<H', wavedata_binary[20:22])[0])
    self.ch                   : int   = int(struct.unpack('<H', wavedata_binary[22:24])[0])
    self.fs                   : int   = int(struct.unpack('<I', wavedata_binary[24:28])[0])
    self.quantization_bit     : int   = int(struct.unpack('<H', wavedata_binary[34:36])[0])
    self.subchunk_identifier  : str   = hex(struct.unpack('>I', wavedata_binary[36:40])[0]).lower()
    self.subchunk_size_of_wave: int   = int(struct.unpack('<I', wavedata_binary[40:44])[0])


  def validate(self):
    '''
    受け取ったデータの検証
    '''
    error_massages: List[str] = []

    if not (
        self.riff.replace('0x', '')                    == 'RIFF'.encode('utf-8').hex() \
        and self.fmt.replace('0x', '')                 == 'fmt '.encode('utf-8').hex() \
        and self.subchunk_identifier.replace('0x', '') == 'data'.encode('utf-8').hex()
    ):
      error_massages.append('ファイル形式が違います')
      logging.error('ファイル形式が違います')
      if self.riff.replace('0x', '') != 'RIFF'.encode('utf-8').hex():
        logging.error(f'riff: {self.riff} ... except "0x52494646 (RIFF)"')
      if self.fmt.replace('0x', '') != 'fmt '.encode('utf-8').hex():
        logging.error(f'fmt: {self.fmt} ... except "0x666D7420 (fmt )"')
      if self.subchunk_identifier.replace('0x', '') != 'data'.encode('utf-8').hex():
        logging.error(f'subchunk_identifier: {self.subchunk_identifier} ... except "0x64617461 (data)"')

    if self.format.replace('0x', '')  != 'WAVE'.encode('utf-8').hex():
      error_massages.append('wavファイルにしてください')
      logging.error('wavファイルにしてください')
      logging.error(f'format: {self.format} ... except "WAVE"')

    # 非圧縮のリニアPCMフォーマットが対象
    if self.audioFormat != 1:
      error_massages.append('非圧縮のリニアPCMフォーマットにしてください')
      logging.error('非圧縮のリニアPCMフォーマットにしてください')
      logging.error(f'audioFormat: {self.audioFormat} ... except 1')

    # モノラルチャンネル(チャンネル数:1)だけが対象
    if self.ch != 1:
      error_massages.append('モノラルにしてください')
      logging.error('モノラルにしてください')
      logging.error(f'ch: {self.ch} ... except 1')

    # サンプリング周波数:16000[Hz]だけが対象
    if self.fs != 16000:
      error_massages.append('サンプリング周波数は16000[Hz]にしてください')
      logging.error('サンプリング周波数は16000[Hz]にしてください')
      logging.error(f'fs: {self.fs} ... except 16000')

    # 量子化bit:16bitだけが対象
    if self.quantization_bit != 16:
      error_massages.append('量子化ビット数は16[bit]にしてください')
      logging.error('量子化ビット数は16[bit]にしてください')
      logging.error(f'quantization_bit: {self.quantization_bit} ... except 16')

    # 一つでもバリデーションエラーがあるとエラーハンドリング
    if len(error_massages) > 0:
      logging.error('wavファイルバリデーションエラー')
      raise HTTPException(status_code=415, detail=error_massages)
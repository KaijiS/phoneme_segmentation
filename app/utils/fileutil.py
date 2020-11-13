import shutil
import wave
import numpy as np

# --------------------------------------
# テキストファイル
# --------------------------------------

def write_text(filepath: str, text: str):
  ''' テキストファイル書き出し

  Parameters
  --------------
  filepath: 書き出し先ファイルパス
  text    : 書き出すtextデータ内容
  '''

  with open(filepath, mode='w') as f:
    f.write(text)

  return

def read_text(filepath) -> str:
  ''' テキストファイル読み込み

  Parameters
  --------------
  filepath: 読み込みファイルパス

  Returns
  --------------
  読み込んだ文字列
  '''
  with open(filepath) as f:
    # ファイル終端まで全て読んだデータを返す
    text = f.read().rstrip()
  return text


# --------------------------------------
# バイナリファイル
# --------------------------------------

def write_binary(filepath: str, binary: bytes):
  ''' バイナリファイル書き出し

  Parameters
  --------------
  filepath: 書き出し先ファイルパス
  binary  : 書き出すバイナリ文字列(bytes)
  '''
  with open(filepath, mode='wb') as f:
    f.write(binary)

  return


def read_binary(filepath: str) -> bytes:
  ''' バイナリファイル読み込み

  Parameters
  --------------
  filepath: 読み込みファイルパス

  Returns
  --------------
  読み込んだバイナリ文字列
  '''
  with open(filepath, 'rb') as f:
    binary = f.read()
  return binary


# --------------------------------------
# wavファイル(wavファイル ⇔ numpy配列)
# --------------------------------------

def write_wave_file(filepath, wave_array, fs=16000, bytewidth=2, ch=1):
  ''' 音声データのnumpy配列はwavファイル書き込み

  Parameters
  --------------
  filepath  : 書き出し先ファイルパス
  wave_array: 書き込む音声データ配列 shape(n_length,)
  fs        : サンプリング周波数(デフォルト16000Hz)
  bytewidth : 量子化バイト数(デフォルト2byte(16bit))
  ch        : チャンネル数(デフォルト1:モノラル)
  '''

  with wave.Wave_write(filepath) as w:
    w.setparams((
        ch,                       # channel
        bytewidth,                # byte width
        fs,                       # sampling rate
        len(wave_array),          # number of frames
        "NONE", "not compressed"  # no compression
    ))
    w.writeframes(wave_array)
  return


def read_wave_file(filepath: str):
  ''' 音声ファイルをnumpy配列読み込み

  Parameters
  --------------
  filepath: 読み込みファイルパス

  Returns
  --------------
  wave_array : 読み込んだ音声データ配列 shape(n_length,)
  fs         : サンプリング周波数
  times_array: 読み込んだ音声データの時間軸配列 shape(n_length,)
  '''
  with wave.open(filepath, "rb") as wf:
    fs = wf.getframerate() #16000Hz
    # getnframes -> 全サンプル
    # readframes > 指定した長さのフレーム
    x = wf.readframes(wf.getnframes())
    # frombuffer > バイナリ表記をintに変換
    wave_array = np.frombuffer(x, dtype="int16")

    times_array = np.arange(0.0, len(wave_array )/fs, 1/fs)

  return wave_array, fs, times_array


# --------------------------------------
# ディレクトリ削除
# --------------------------------------

def removeDir(dir_path):
  ''' 中身ごとディレクトリを削除

  Parameters
  --------------
  filepath: 対象ディレクトリパス
  '''
  shutil.rmtree(dir_path)
  return
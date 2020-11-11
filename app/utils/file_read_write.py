def write_text(filepath: str, text: str):
  ''' テキストファイル書き出し

  Parameters
  --------------
  filepath: 書き出し先ファイルパス
  text:     書き出すtextデータ内容
  '''

  with open(filepath, mode='w') as f:
    f.write(text)

  return



def write_binary(filepath: str, binary: bytes):
  ''' バイナリファイル書き出し

  Parameters
  --------------
  filepath: 書き出し先ファイルパス
  binary:     書き出すバイナリ文字列(bytes)
  '''
  with open(filepath, mode='wb') as f:
    f.write(binary)

  return
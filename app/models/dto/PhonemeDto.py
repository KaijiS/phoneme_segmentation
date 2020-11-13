class PhonemeDto():

  def __init__(self, phoneme, filepath, filename, start_time, end_time):
    self.phoneme    : str   = phoneme
    self.filepath   : str   = filepath
    self.filename   : str   = filename
    self.start_time : float = start_time
    self.end_time   : float = end_time



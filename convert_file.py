#!/opt/anaconda3/bin/python
# -*- coding:utf-8 -*-

import os
import glob
import sys

FFMPEG_PATH=os.path.join('.', 'ffmpeg', 'bin', 'ffmpeg')
NAME_TO_ID = {
    'a': 0, 'b': 1, 'bb': 2, 'c': 3, 'cc': 4, 'd': 5, 
    'e': 6, 'ee': 7, 'f': 8, 'ff': 9, 'g': 10, 'gg': 11, 
    'h': 12, 'hh': 13, 'i': 14, 'ii': 15, 'iii': 16, 'iiii': 17, 
    'j': 18, 'jj': 19, 'k': 20, 'l': 21, 'll': 22, 'lll': 23}

FFMPEG_COMMAND = FFMPEG_PATH + ' -i %s -ac 1 -acodec pcm_f32le -ar 16000 %s -v 1'

def ConvertFile(audio, itr, dir_out):
  fname = os.path.basename(audio)
  fname = fname.split('.')
  
  if len(fname) != 2:
    return False

  fname = fname[0]
  if fname not in NAME_TO_ID:
    return False

  ID = NAME_TO_ID[fname]
  output_name = '%d_%d.wav'%(itr, ID)
  output_name = os.path.join(dir_out, output_name)
  
  os.system(FFMPEG_COMMAND%(audio, output_name))
  return True

def ConvertAudioToWav(dir_in, dir_out=os.path.join('.', 'data', 'train')):
  if not os.path.exists(dir_in):
    raise(ValueError(dir_in + ' does not exist'))
  if not os.path.exists(dir_out):
    raise(ValueError(dir_out + ' does not exist'))

  iter_num = 0
  dirs = os.listdir(dir_in)
  
  for d in dirs:
    d = os.path.join(dir_in, d)
    if os.path.isfile(d):
      continue
    
    audios = glob.glob(os.path.join(d, '*.*'))
    if (len(audios) < 20) or (len(audios) > 24):
        continue
    
    for audio in audios:
      if ConvertFile(audio, iter_num, dir_out):
        iter_num += 1

  return iter_num

if __name__ == '__main__':
    ConvertAudioToWav(sys.argv[1])

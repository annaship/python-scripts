#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys

class Fa_seq_len:
  def __init__(self):
    self.usage = """python count_seq_len_fa.py DIRNAME [-ve]"""
    self.all_dirs = set()
    
  def get_files(self, walk_dir_name, ext = ""):
      files = {}
      filenames = []
      for dirname, dirnames, filenames in os.walk(walk_dir_name, followlinks=True):
          if ext:
              filenames = [f for f in filenames if f.endswith(ext)]
        
          for file_name in filenames:
              full_name = os.path.join(dirname, file_name)
              (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
              files[full_name] = (dirname, file_base, file_extension)
      return files

  def is_verbatim(self):
    try: 
      if sys.argv[2] == "-ve":
        return True
    except IndexError:
      return False
    except: 
      print "Unexpected error:", sys.exc_info()[0]
      return False
    return False

  def get_seq_len_distrib(self, f_input):
    for idx, seq in enumerate(f_input.sequences):
      seq_len = len(seq)
      print seq_len
  
  def print_short_seq(self, f_input, file_name):
    for idx, seq in enumerate(f_input.sequences):
      seq_len = len(seq)
      if seq_len < 200:
        print f_input.ids[idx]
        print seq
        print "WARNING, sequence length in %s = %s. It's less than 200!" % (file_name, seq_len)
        self.all_dirs.add(fa_files[file_name][0])


if __name__ == '__main__':
  seq_len = Fa_seq_len()
  is_verbatim = seq_len.is_verbatim()
  
  start_dir = sys.argv[1]
  if (is_verbatim):
    print "Start from %s" % start_dir
    print "Getting file names"
  
  fa_files = seq_len.get_files(start_dir, ".fa")
  if (is_verbatim):
    print "Found %s fa files" % (len(fa_files))
  
  
  for file_name in fa_files:
    if (is_verbatim):
      print file_name

    try:
      f_input  = fa.ReadFasta(file_name)
      # seq_len.print_short_seq(f_input, file_name)
      seq_len.get_seq_len_distrib(f_input)

    except RuntimeError:
      if (is_verbatim):
        print sys.exc_info()[0]
    except:
      print "Unexpected error:", sys.exc_info()[0]
      raise
      next

  if (is_verbatim):
    print "Current directory:"
    print seq_len.all_dirs
  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys
import argparse


class Fa_seq_len:
  def __init__(self):
    self.all_dirs  = set()
    self.start_dir = ""
    
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
  
  def print_short_seq(self, f_input, file_name, min_len):
    for idx, seq in enumerate(f_input.sequences):
      seq_len = len(seq)
      if seq_len < int(min_len):
        print f_input.ids[idx]
        print seq
        print "WARNING, sequence length in %s = %s. It's less than %s!" % (file_name, seq_len, min_len)
        self.all_dirs.add(fa_files[file_name][0])

  def get_args(self, argv):
     try:
       parser = argparse.ArgumentParser(description = self.usage)
     except:
       raise
       
     for opt, arg in opts:
        if opt == '-h':
           print self.usage
           sys.exit()
        elif opt in ("-d", "--dir"):
           self.start_dir = arg


if __name__ == '__main__':
  seq_len = Fa_seq_len()
  # seq_len.get_args(sys.argv[1:])
  
  # parser = argparse.ArgumentParser(description = seq_len.usage)
  parser = argparse.ArgumentParser()

  parser.add_argument("-d", "--dir",
    required = False, action = "store", dest = "start_dir", default = '.',
    help = """Input directory name, default - current""")
  parser.add_argument("-ve", "--verbatim",
    required = False, action = "store_true", dest = "is_verbatim",
    help = """Print an additional inforamtion""")
  parser.add_argument("-l", "--length",
    required = False, action = "store", dest = "min_len", default = '200',
    help = """Seq length threshold, default - 200""")
  parser.add_argument("-e", "--ext",
    required = False, action = "store", dest = "ext", default = '.fa',
    help = """File ending, default - .fa""")
  parser.add_argument("-hi", "--histogram",
    required = False, action = "store_true", dest = "histogram",
    help = """Run get_seq_len_distrib""")
  parser.add_argument("-s", "--short_s",
    required = False, action = "store_true", dest = "short_s",
    help = """Run print_short_seq""")
    
  
  args = parser.parse_args()
  print "args = "
  print args
  
  is_verbatim = args.is_verbatim
  
  start_dir = args.start_dir
  # start_dir = sys.argv[1]
  if (is_verbatim):
    print "Start from %s" % start_dir
    print "Getting file names"
  
  fa_files = seq_len.get_files(start_dir, args.ext)
  if (is_verbatim):
    print "Found %s fa files" % (len(fa_files))
  
  for file_name in fa_files:
    if (is_verbatim):
      print file_name

    try:
      f_input  = fa.ReadFasta(file_name)
      if (args.short_s):
        seq_len.print_short_seq(f_input, file_name, args.min_len)
      if (args.histogram):
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
  
  

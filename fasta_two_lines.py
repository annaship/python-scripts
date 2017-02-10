#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys
import argparse


class My_fasta:
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

  def read_fasta(self):
      pass
  
  def write_fasta(self, entry, split = True, store_frequencies = True):
      f_output = self.out_files["unknown"].store_entry(e)
      

  def print_short_seq(self, f_input, file_name, min_len):
    for idx, seq in enumerate(f_input.sequences):
      my_fasta = len(seq)
      if my_fasta < int(min_len):
        print f_input.ids[idx]
        print seq
        print "WARNING, sequence length in %s = %s. It's less than %s!" % (file_name, my_fasta, min_len)
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
  
  def unsplit_fa(self, input_file_path, output_file_path):
    input = fa.SequenceSource(input_file_path)
    output = fa.FastaOutput(output_file_path)

    while input.next():
      output.store(input, split = False)
    output.close()

  def seq_concat_id_fa(self, input_file_path, output_file_path):
    input = fa.SequenceSource(input_file_path)
    output = open(output_file_path, "w")

    while input.next():
        # print "input.id "
        # print input.id
        # print "input.seq"
        # print input.seq
        # print 'input.id + "#" + input.seq'
        # print input.id + "#" + input.seq
        # output.
      output.write(input.id + "#" + input.seq + "\n")
    output.close()


if __name__ == '__main__':
  my_fasta = My_fasta()
  # my_fasta.get_args(sys.argv[1:])
  
  # parser = argparse.ArgumentParser(description = my_fasta.usage)
  parser = argparse.ArgumentParser()

  parser.add_argument("-d", "--dir",
    required = False, action = "store", dest = "start_dir", default = '.',
    help = """Input directory name, default - current""")
  parser.add_argument("-ve","--verbatim",
    required = False, action = "store_true", dest = "is_verbatim",
    help = """Print an additional inforamtion""")
  # parser.add_argument("-l", "--length",
  #   required = False, action = "store", dest = "min_len", default = '200',
  #   help = """Seq length threshold, default - 200""")
  parser.add_argument("-e", "--ext",
    required = False, action = "store", dest = "ext", default = '.fa',
    help = """File ending, default - .fa""")
  # parser.add_argument("-hi", "--histogram",
  #   required = False, action = "store_true", dest = "histogram",
  #   help = """Run get_my_fasta_distrib""")
  parser.add_argument("-u", "--unsplit",
    required = False, action = "store_true", dest = "unsplit",
    help = """Run unsplit""")
  parser.add_argument("-c", "--concat",
    required = False, action = "store_true", dest = "seq_concat_id_fa",
    help = """Run seq_concat_id_fa""")
  # parser.add_argument("-s", "--short_s",
  #   required = False, action = "store_true", dest = "short_s",
  #   help = """Run print_short_seq""")
    
  
  args = parser.parse_args()
  print "args = "
  print args
  
  is_verbatim = args.is_verbatim
  
  start_dir = args.start_dir
  # start_dir = sys.argv[1]
  if (is_verbatim):
    print "Start from %s" % start_dir
    print "Getting file names"
  
  fa_files = my_fasta.get_files(start_dir, args.ext)
  if (is_verbatim):
    print "Found %s fa files" % (len(fa_files))
  
  program_name = ""
  if args.seq_concat_id_fa:
      program_name = my_fasta.seq_concat_id_fa
      out_file_suffix = ".concat.fa"
  else:
      program_name = my_fasta.unsplit_fa
      out_file_suffix = ".unsplit.fa"
      
  for in_file_name in fa_files:
    if (is_verbatim):
      print in_file_name
      print program_name
      
    try:
        out_file_name = fa_files[in_file_name][1] + out_file_suffix
        # pr = globals()[program_name]
        # pr(in_file_name, out_file_name)
        my_fasta.seq_concat_id_fa(in_file_name, out_file_name)

    except RuntimeError:
      if (is_verbatim):
        print sys.exc_info()[0]
    except:
      print "Unexpected error:", sys.exc_info()[0]
      raise
      next

  if (is_verbatim):
    print "Current directory:"
    print my_fasta.all_dirs
  
  

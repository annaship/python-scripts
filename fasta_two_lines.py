#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys
import argparse


class My_fasta:
  def __init__(self, args):
    self.start_dir = ""
    self.args = args
    
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

  def print_short_seq(self, f_input, file_name, min_len):
    for idx, seq in enumerate(f_input.sequences):
      my_fasta = len(seq)
      if my_fasta < int(min_len):
        print f_input.ids[idx]
        print seq
        print "WARNING, sequence length in %s = %s. It's less than %s!" % (file_name, my_fasta, min_len)
        self.all_dirs.add(fa_files[file_name][0])

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
      output.write(input.id + "#" + input.seq + "\n")
    output.close()
    
  def get_out_file_name(self, out_file_suffix, fa_files, in_file_name):
    return self.args.output_file_name or fa_files[in_file_name][1] + out_file_suffix
   


if __name__ == '__main__':
  
  parser = argparse.ArgumentParser(description = "Exampe: python %(prog)s -c -o 'concat.fa' -e 'unique.nonchimeric.fa'")
  # parser = argparse.ArgumentParser()

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
    help = """Concatenate splited sequences to one line per sequence (default)""")
  parser.add_argument("-c", "--concat",
    required = False, action = "store_true", dest = "seq_concat_id_fa",
    help = """Concatenate each def line with its sequence, divided by '#'.""")
  parser.add_argument("-o", "--output",
    required = False, action = "store", dest = "output_file_name",
    help = """Output file name, default - input file name + '.unsplit.fa' or '.concat.fa' """)
  # parser.add_argument("-s", "--short_s",
  #   required = False, action = "store_true", dest = "short_s",
  #   help = """Run print_short_seq""")
    
  
  args = parser.parse_args()
  my_fasta = My_fasta(args)
  
  is_verbatim = args.is_verbatim
  
  if is_verbatim: print "args = %s" % (args)
  
  start_dir = args.start_dir
  if is_verbatim:
    print "Start from %s" % start_dir
    print "Getting file names"
  
  fa_files = my_fasta.get_files(start_dir, args.ext)
  if is_verbatim: print "Found %s %s file(s)" % (len(fa_files), args.ext)
  
  out_file_name = ""
  for in_file_name in fa_files:
    if is_verbatim: print in_file_name
    try:
      if args.seq_concat_id_fa:
        out_file_suffix = ".concat.fa"
        # out_file_name = args.output_file_name or fa_files[in_file_name][1] + out_file_suffix
        out_file_name = my_fasta.get_out_file_name(out_file_suffix, fa_files, in_file_name)
        my_fasta.seq_concat_id_fa(in_file_name, out_file_name)
        if is_verbatim: print "Running seq_concat_id_fa"
      else:
        out_file_suffix = ".unsplit.fa"
        # out_file_name = args.output_file_name or fa_files[in_file_name][1] + out_file_suffix
        out_file_name = my_fasta.get_out_file_name(out_file_suffix, fa_files, in_file_name)
        my_fasta.unsplit_fa(in_file_name, out_file_name)
        if is_verbatim: print "Running unsplit_fa"
    except:
      raise
      next

  if is_verbatim: print "out_file_name = %s" % (out_file_name)

  if is_verbatim: print "Current directory: %s" % (start_dir)
  
  

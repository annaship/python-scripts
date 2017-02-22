#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys
import argparse
import re


class My_fasta:
  def __init__(self, args):
    self.start_dir = ""
    self.args = args
    self.all_files = {}
    self.too_short_hvr  = {}
    self.has_f_pr    = {}
    self.has_both_pr = {}
    self.has_no_f_pr = {}
    self.has_no_r_pr = {}
    self.total_seq   = 0
    self.good_ones   = ()
    self.refhvr_cuts = {}
    
    
  def query_yes_no(self, question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


  def get_files(self, walk_dir_name, ext = ""):
      # files = {}
      filenames = []
      for dirname, dirnames, filenames in os.walk(walk_dir_name, followlinks=True):
          if ext:
              filenames = [f for f in filenames if f.endswith(ext)]

          for file_name in filenames:
              full_name = os.path.join(dirname, file_name)
              (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
              self.all_files[full_name] = (dirname, file_base, file_extension)

  def get_out_file_name(self, in_file_name, out_file_suffix = ".out"):
    return self.args.output_file_name or self.all_files[in_file_name][1] + out_file_suffix


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

  def cut_region(self, input_file_path, output_file_path):
    input      = fa.SequenceSource(input_file_path)
    output     = open(output_file_path, "w")
    # no_primers = open('no_primers', "w")
    self.total_seq  = 0
    
    while input.next():
      self.total_seq += 1
      refhvr_cut = self.get_region(input, self.args.forward_primer, self.args.distal_primer)    
      if (len(refhvr_cut) > int(self.args.min_refhvr_cut_len)):
        output.write(">" + input.id)
        output.write("\n")
        output.write(refhvr_cut)
        output.write("\n")
      else:
        self.too_short_hvr[input.id] = refhvr_cut

      
      
  def write_cuts(self):
    for input_id, seq in self.refhvr_cuts.items():
      out1 = open("out1", "w")
      if (len(self.refhvr_cuts[input_id]) > int(self.args.min_refhvr_cut_len)):
        out1.write(">" + input_id)
        out1.write("\n")
        out1.write(self.refhvr_cuts[input_id])
        out1.write("\n")
    
  def get_cut_stats(self):
    stats = open('hvr_cut.stats', "w")
    stats.write("total sequences: %s\n" % self.total_seq)
    
    stats.write("\nHave both primers (%s):\n" % len(self.has_both_pr.keys()))
    stats.write(", ".join(sorted(self.has_both_pr.keys())))
    
    stats.write("\nNo forward primer (%s):\n" % len(self.has_no_f_pr.keys()))
    stats.write(", ".join(sorted(self.has_no_f_pr.keys())))

    stats.write("\nForward primer only (no reverse) (%s):\n" % len(self.has_no_r_pr.keys()))
    stats.write(", ".join(sorted(self.has_no_r_pr.keys())))

    too_short = set(self.has_both_pr.keys()) & set(self.too_short_hvr.keys())
    if (len(too_short)) > 0:
      stats.write("\nHave both primers, but region between primers is too short (%s):\n" % len(too_short))
      stats.write(", ".join(sorted(list(too_short))))

    if (len(set(self.good_ones) - set(self.has_both_pr.keys()))) > 0:
      stats.write("\nHave both primers and region between primers is not too short (%s):\n" % len(self.good_ones))
      stats.write(", ".join(sorted(list(self.good_ones))))
    stats.write("\n")

  def get_region(self, input, f_primer, r_primer):
    refhvr_cut_t = ()
    refhvr_cut = ""

    re_f_primer = '^.+' + f_primer
    re_r_primer = r_primer + '.+'

    hvrsequence_119_1_t = re.subn(re_f_primer, '', input.seq)
    if (hvrsequence_119_1_t[1] > 0):
      self.has_f_pr[input.id] = input.seq
      refhvr_cut_t = re.subn(re_r_primer, '', hvrsequence_119_1_t[0])
      if (refhvr_cut_t[1] > 0):
        refhvr_cut = refhvr_cut_t[0]
        self.has_both_pr[input.id] = input.seq
        self.refhvr_cuts[input.id] = refhvr_cut
      else:
        self.has_no_r_pr[input.id] = input.seq
    else:
      self.has_no_f_pr[input.id] = input.seq

    return refhvr_cut


if __name__ == '__main__':

  parser = argparse.ArgumentParser(description = "Exampe: python %(prog)s -c -o 'concat.fa' -e 'unique.nonchimeric.fa'")

  parser.add_argument("-p", "--path",
    required = False, action = "store", dest = "start_dir", default = '.',
    help = """Input directory name, default - current""")
  parser.add_argument("-ve","--verbatim",
    required = False, action = "store_true", dest = "is_verbatim",
    help = """Print an additional inforamtion""")
  parser.add_argument("-e", "--ext",
    required = False, action = "store", dest = "ext", default = '.fa',
    help = """File ending, default - .fa""")
  parser.add_argument("-u", "--unsplit",
    required = False, action = "store_true", dest = "unsplit",
    help = """Concatenate splited sequences to one line per sequence (default)""")
  parser.add_argument("-c", "--concat",
    required = False, action = "store_true", dest = "seq_concat_id_fa",
    help = """Concatenate each def line with its sequence, divided by '#'.""")
  parser.add_argument("-r", "--region",
    required = False, action = "store_true", dest = "cut_region",
    help = """Cut refhvr region. ???Add about reverse-complimenting???""")

  parser.add_argument("-o", "--output",
    required = False, action = "store", dest = "output_file_name",
    help = """Output file name, default - input file name + '.out' """)
  parser.add_argument("-f", "--f_primer",
    required = False, action = "store", dest = "forward_primer", default = "TTGTACACACCGCCC",
    help = """Forward primer, default - 'TTGTACACACCGCCC' v9 1389F """)
  parser.add_argument("-d", "--d_primer",
    required = False, action = "store", dest = "distal_primer", default = "GTAGGTGAACCTGC.GAAG",
    help = """Distal (reversed) primer, default - 'GTAGGTGAACCTGC.GAAG' v9 1389F """)
  parser.add_argument("-l", "--len",
    required = False, action = "store", dest = "min_refhvr_cut_len", default = "50",
    help = """Min refhvr cut length, default - 50""")

  args = parser.parse_args()

  my_fasta = My_fasta(args)
  if not len(sys.argv) > 1:
      print """Running 'unsplit' with default parameters: input ext='.fa', start_dir='.', """
      yes_no = my_fasta.query_yes_no("Do you want to proceed?")
      # print "yes_no = "
      # print yes_no
      if not yes_no:
          sys.exit()

  is_verbatim = args.is_verbatim

  if is_verbatim: print "args = %s" % (args)

  start_dir = args.start_dir
  if is_verbatim:
    print "Start from %s" % start_dir
    print "Getting file names"

  my_fasta.get_files(start_dir, args.ext)
  if is_verbatim: print "Found %s %s file(s)" % (len(my_fasta.all_files), args.ext)

  out_file_names = []
  out_file_name = ""
  for in_file_name in my_fasta.all_files:
    if is_verbatim: print in_file_name
    try:
      out_file_name = my_fasta.get_out_file_name(in_file_name)
      out_file_names.append(out_file_name)
      if args.seq_concat_id_fa:
        my_fasta.seq_concat_id_fa(in_file_name, out_file_name)
        if is_verbatim: print "Running seq_concat_id_fa"
      elif args.unsplit:
        my_fasta.unsplit_fa(in_file_name, out_file_name)
        if is_verbatim: print "Running unsplit_fa"
      elif args.cut_region:
        my_fasta.cut_region(in_file_name, out_file_name)
        my_fasta.get_cut_stats()
        if is_verbatim: print "Running cut_region"
      else:
        if is_verbatim: print "everything else"

    except:
      raise
      next

  # if is_verbatim:
  for out_file_name in out_file_names:
      print "Output file name: '%s'" % (out_file_name)

  if is_verbatim: print "Current directory: %s" % (start_dir)



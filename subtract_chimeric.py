#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import IlluminaUtils.lib.fastalib as fa
import os
import sys
import argparse


class Chimeras:
  def __init__(self):
      self.chimeric_file_name_txt = ""
      self.chimeric_file_name_db  = ""
      self.chg_file               = ""
      self.output_file_name       = ""
      self.dir_name               = ""
      
  def usage(self):
      print("""Subtracts reads provided in *txt.chimeric.fa and db.chimeric.fa from *unique.chg.
      Files should be in the same directory.
      Command line: python /xraid/bioware/linux/seqinfo/bin/subtract_chimeric.py -i FILENAME.unique.chg
      """)

  def get_file_name_parts(self, input_file_arg, args_start_dir = ""):
      self.dir_name = os.path.dirname(input_file_arg)
      if self.dir_name == "":
          self.dir_name = args.start_dir

      
      file_prefix = os.path.basename(input_file_arg).split(".")[0]
      print("file_prefix = ")
      print(file_prefix)
      
      self.unique_file            = file_prefix + ".unique"
      self.chimeric_file_name_txt = file_prefix + ".unique.chimeras.txt.chimeric.fa"
      self.chimeric_file_name_db  = file_prefix + ".unique.chimeras.db.chimeric.fa"
      self.chg_file               = file_prefix + ".unique.chg"
      self.output_file_name       = file_prefix + ".unique.nonchimeric.fa"
    
  def get_chimeric_ids(self, file_name):
      ids = set()
      print("Get ids from %s" % file_name)
      # todo: benchmark
      # read_fasta     = fa.ReadFasta(file_name)
      # # ids.update(set(read_fasta.ids))
      # ids = set(read_fasta.ids)
      chimeric_fasta = fa.SequenceSource(file_name, lazy_init = False) 
      
      while chimeric_fasta.next():
          ids.add(chimeric_fasta.id)
      chimeric_fasta.close()
      return ids
    
  def move_out_chimeric(self):
      txt_ids = self.get_chimeric_ids(os.path.join(self.dir_name, self.chimeric_file_name_txt))
      db_ids  = self.get_chimeric_ids(os.path.join(self.dir_name, self.chimeric_file_name_db))
      all_chimeric_ids = set(txt_ids) | set(db_ids)
      print("len(all_chimeric_ids) = ")
      print(len(all_chimeric_ids))
      
      non_chimeric_fasta = fa.FastaOutput(os.path.join(self.dir_name, self.output_file_name))
      orig_fasta         = fa.SequenceSource(os.path.join(self.dir_name, self.chg_file), lazy_init = False) 

      while orig_fasta.next():
          if not orig_fasta.id in all_chimeric_ids:
              non_chimeric_fasta.store(orig_fasta, store_frequencies = False)
      non_chimeric_fasta.close()

if __name__ == '__main__':
    chimeras = Chimeras()

    # parser = argparse.ArgumentParser(description = chimeras.usage)
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir",
        required = False, action = "store", dest = "start_dir", default = '.',
        help = """Input directory name, default - current""")
    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")

    args = parser.parse_args()
    print("args = ")
    print(args)

    
    chimeras.get_file_name_parts(args.input_file, args.start_dir)
    chimeras.move_out_chimeric()
    
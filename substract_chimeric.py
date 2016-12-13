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

  def get_file_name_parts(self, input_file_arg):
      # print "input_file_arg = "
      # print input_file_arg
      # 
      # print "os.path.basename"
      # print os.path.basename(input_file_arg)
      
      self.dir_name = os.path.dirname(input_file_arg)
      
      file_prefix = os.path.basename(input_file_arg).split(".")[0]
      print "file_prefix = "
      print file_prefix
      
      self.chimeric_file_name_txt = file_prefix + ".unique.chimeras.txt.chimeric.fa"
      self.chimeric_file_name_db  = file_prefix + ".unique.chimeras.db.chimeric.fa"
      self.chg_file               = file_prefix + ".unique.chg"
      self.output_file_name       = file_prefix + ".unique.nonchimeric.fa"
    
  def get_chimeric_ids(self, file_name):
      ids = set()
      print "Get ids from %s" % file_name
      read_fasta     = fa.ReadFasta(file_name)
      ids.update(set(read_fasta.ids))
      return ids

    
  def move_out_chimeric(self):
      chimeric_ids = self.get_chimeric_ids()
      for idx_key in self.input_file_names:
          fasta_file_path    = os.path.join(self.indir, self.input_file_names[idx_key])   
          read_fasta         = fa.ReadFasta(fasta_file_path)
          read_fasta.close()

          non_chimeric_file  = fasta_file_path + self.nonchimeric_suffix
          non_chimeric_fasta = fa.FastaOutput(non_chimeric_file)

          fasta              = fa.SequenceSource(fasta_file_path, lazy_init = False) 
          while fasta.next():
              if not fasta.id in chimeric_ids:
                  non_chimeric_fasta.store(fasta, store_frequencies = False)
          non_chimeric_fasta.close()

if __name__ == '__main__':
    chimeras = Chimeras()
    # seq_len.get_args(sys.argv[1:])

    # parser = argparse.ArgumentParser(description = seq_len.usage)
    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir",
        required = False, action = "store", dest = "start_dir", default = '.',
        help = """Input directory name, default - current""")
    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")

    args = parser.parse_args()
    print "args = "
    print args

    
    chimeras.get_file_name_parts(args.input_file)
    txt_ids = chimeras.get_chimeric_ids(os.path.join(chimeras.dir_name, chimeras.chimeric_file_name_txt))
    print "txt_ids = "
    print txt_ids
    db_ids  = chimeras.get_chimeric_ids(os.path.join(chimeras.dir_name, chimeras.chimeric_file_name_db))
    print "db_ids = "
    print db_ids
    
    
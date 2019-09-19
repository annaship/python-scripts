from itertools import islice
import sys
import os 

def read_fastq(f_name):
  f = open(f_name, "r")
  all_lines = f.readlines()
  spls = [line.strip("\n").split(",") for line in all_lines]
  seq_t_d = {s: t for s, t in spls}
  return seq_t_d

def fix_freq(next_n_lines):
  res = []
  n = 0
  for l in next_n_lines:
    n += 1
    if n == 1:
      res.append(l)
    else:
      res.append(l.replace(",", ";frequency="))

  return res

def get_fastq_f_by4(fastq_f):
  fastq_f_text = open(fastq_f, "r")
  array_by4 = []
  n = 4
  while True:
    next_n_lines = list(islice(fastq_f_text, n))
    next_n_lines_f = fix_freq(next_n_lines)
    if not next_n_lines_f:
            break
    clean_lines = [l.strip("\n").strip(",") for l in next_n_lines_f]
    array_by4.append(clean_lines)
  return array_by4


if __name__ == '__main__':
  out_file_dir = "/Users/ashipunova/work/remove_barcodes"

  file_freq_name = os.path.join(out_file_dir, sys.argv[1])

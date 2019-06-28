# ver 2; by file
import os
import sys
from collections import defaultdict

# save headers?
# args file name

def get_files(walk_dir_name = ".", ext = ""):
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

def get_file_content(filename):
    # args = sys.argv
    # filename = args[1]
    fh = open(filename,'r')
    all_lines = fh.readlines()
    fh.close()
    return all_lines
    
def get_seq_tax(seq_tax_file_name):
  seq_tax_dict = {}

  with open(seq_tax_file_name) as seq_tax:
    for line in seq_tax:
        listedline = line.strip().split('\t')
        if len(listedline) > 1: # we have the "\t" sign in there
            seq_tax_dict[listedline[0]] = listedline[1]

  return seq_tax_dict
  
def print_result(result):
  for pr_dat, counts in result.items():
    out_file_name = pr_dat + "by_seq_id.csv"
    file = open(out_file_name, "w") 
    res_line = "%s, %s\n" % (pr_dat.strip(), ",".join(counts))
    file.write(res_line) 
 
  file.close() 

def print_first_line(seq_tax_dict):
  seqs = seq_tax_dict.keys()
  res_line = ", %s\n" % (",".join(seqs))

  out_file_name = "first_line.csv"
  file = open(out_file_name, "w") 
  file.write(res_line) 
 
  file.close()
  
def print_last_line(seq_tax_dict):
  taxa = seq_tax_dict.values()
  res_line = "Taxonomy, %s\n" % (",".join(taxa))

  out_file_name = "last_line.csv"
  file = open(out_file_name, "w") 
  file.write(res_line) 
 
  file.close()


def get_result(all_dict):
  result = defaultdict()

  for pr_dat, seq_freq_dict in all_dict.items():
    res_text = []
    result[pr_dat] = []
    for seq in seq_tax_dict.keys():
      if seq in seq_freq_dict.keys():
        freq = seq_freq_dict[seq]
        result[pr_dat].append(freq)
      else:
        result[pr_dat].append("0")
  return result

my_dir = "/Users/ashipunova/work/emil/results_py"
seq_tax_file_name = "seq_tax_u.txt"
seq_tax_dict = get_seq_tax(seq_tax_file_name)

file_names = get_files(ext = ".tsv")
# print(file_names)

for file_name in file_names:
  full_name = os.path.join(my_dir, file_name)
  # print(full_name)
  content = get_file_content(full_name) 
  all_dict = defaultdict()
  
  for line in content:
     
     line_arr = line.strip().split()
     # print("Line {}: {}".format(cnt, line_arr))
     # Line 11: ['BBO_IGM_Bv4v5__R3_2', '118510832', '1', 'Bacteria;Firmicutes;Bacilli;Bacillales;Bacillaceae;Bacillus']

     pr_dat = line_arr[0]
     seq = line_arr[1]
     freq = line_arr[2]

     try:
       all_dict[pr_dat][seq] = freq
     except KeyError:         
       all_dict[pr_dat] = {}
       all_dict[pr_dat][seq] = freq
     
  result = get_result(all_dict)

  print_result(result)      
  print_first_line(seq_tax_dict)
  print_last_line(seq_tax_dict)      


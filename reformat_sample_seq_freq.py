import os
import sys
from collections import defaultdict

# save headers

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

my_dir = "/Users/ashipunova/work/emil/results_py"
seq_tax_file_name = "seq_tax_u.txt"
seq_tax_dict = get_seq_tax(seq_tax_file_name)

file_names = ["test1.csv", "test2.csv"]

# fp = open(full_name, 'r')
# with open(filepath) as fp:
#    for cnt, line in enumerate(fp):
#        print("Line {}: {}".format(cnt, line))

# seq_tax = open(seq_tax_file_name, 'r')


all_dict = defaultdict()
res_text = ""

for file_name in file_names:
  full_name = os.path.join(my_dir, file_name)
  print(full_name)
  content = get_file_content(full_name) 
  cnt = 1
  for line in content:
     cnt += 1
     
     line_arr = line.strip().split()
     print("Line {}: {}".format(cnt, line_arr))
     # Line 11: ['BBO_IGM_Bv4v5__R3_2', '118510832', '1', 'Bacteria;Firmicutes;Bacilli;Bacillales;Bacillaceae;Bacillus']

     # all_dict[line_arr[0]]
     pr_dat = line_arr[0]
     seq = line_arr[1]
     freq = line_arr[2]
     # for k in seq_tax_dict.keys():
       # print(k)
       # res_text += line_arr[0] +
     try:
       all_dict[pr_dat][seq] = freq
     except KeyError:         
       all_dict[pr_dat] = {}
       all_dict[pr_dat][seq] = freq
     
print(all_dict)
# {'BBO_IGM_Bv4v5__G6_3': {'118510824': '1', '118510832': '1'}..., 'BBO_IGM_Bv4v5__R3_2': {'118510832': '1'}}
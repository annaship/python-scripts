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

my_dir = "/Users/ashipunova/work/emil/results_py"
seq_tax_file_name = "seq_tax_u.txt"

file_names = ["test1.csv", "test2.csv"]

# fp = open(full_name, 'r')
# with open(filepath) as fp:
#    for cnt, line in enumerate(fp):
#        print("Line {}: {}".format(cnt, line))

# seq_tax = open(seq_tax_file_name, 'r')
# print(seq_tax)
seq_tax_dict = {}

with open(seq_tax_file_name) as seq_tax:
  for line in seq_tax:
      listedline = line.strip().split('\t')
      if len(listedline) > 1: # we have the "\t" sign in there
          seq_tax_dict[listedline[0]] = listedline[1]

print(seq_tax_dict)

all_dict = defaultdict()

for file_name in file_names:
  full_name = os.path.join(my_dir, file_name)
  print(full_name)
  content = get_file_content(full_name) 
  cnt = 1
  for line in content:
     cnt += 1
     
     line_arr = line.strip().split()
     # all_dict[]
     print("Line {}: {}".format(cnt, line_arr))


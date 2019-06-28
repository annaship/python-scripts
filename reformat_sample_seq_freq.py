import os
import sys

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
      if len(listedline) > 1: # we have the = sign in there
          seq_tax_dict[listedline[0]] = listedline[1]

print(seq_tax_dict)

#
# for file_name in file_names:
#    file_name = os.path.join(my_dir, file_name)
#
#    # with open(full_name) as fp:
#    line = fp.readline()
#    cnt = 1
#    while line:
#        print("Line {}: {}".format(cnt, line.strip()))
#        line = fp.readline()
#        if (cnt == 1):
#          get_headers
#        cnt += 1
#        headers = line.strip()

# Line 1: project__dataset  sequence_ill_id  sum_seq_count  taxonomy

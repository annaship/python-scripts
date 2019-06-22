import sys
import pprint
from collections import defaultdict
pp = pprint.PrettyPrinter(indent=4)

def convert_to_num(str_cnt):
    tmp_cnt = str_cnt.rstrip("ms\n")
    # pp.pprint(tmp_cnt)
  
    num_cnt = float(tmp_cnt)
    # pp.pprint(num_cnt)  
    return num_cnt

def get_file_content():
    args = sys.argv
    filename = args[1]
    fh = open(filename,'r')
    all_lines = fh.readlines()
    fh.close()
    return all_lines

all_totals = defaultdict()
all_lines = get_file_content()

n = 0
for line in all_lines:
  n += 1
  try:
    line_arr = line.split(": ")
    try:
      name = line_arr[1]
      str_cnt = line_arr[2]
    except IndexError:
      continue

    num_cnt = convert_to_num(str_cnt)

    curr_cnt = 0
    try:
      curr_cnt = all_totals[name]
    except KeyError:
      all_totals[name] = 0
      
    all_totals[name] = curr_cnt + num_cnt
  except:
    raise
# print n

print("average: ")
for k, v in all_totals.items():
  avg = v / n
  print("%s: %.2f" % (k, avg)) 
print("\n---\n")

print("all_totals: ")
for k, v in all_totals.items():
  print("%s: %.2f" % (k, v)) 
# pp.pprint(all_totals)


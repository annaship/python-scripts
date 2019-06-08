import sys
import pprint
from collections import defaultdict
pp = pprint.PrettyPrinter(indent=4)

args = sys.argv
filename = args[1]
fh = open(filename,'r')
all_lines = fh.readlines()
fh.close()

all_totals = defaultdict()
for line in all_lines:
  try:
    line_arr = line.split(": ")
    name = line_arr[1]
    str_cnt = line_arr[2]

    tmp_cnt = str_cnt.rstrip("ms\n")
    # pp.pprint(tmp_cnt)
  
    num_cnt = float(tmp_cnt)
    # pp.pprint(num_cnt)

    curr_cnt = 0
    try:
      curr_cnt = all_totals[name]
      # pp.pprint(curr_cnt)
    except KeyError:
      all_totals[name] = 0
      
    all_totals[name] = curr_cnt + num_cnt

    # all_totals[name] += 
  # print("LINE: %s" % line)
  except:
    raise

print("all_totals: ")
pp.pprint(all_totals)

def convert_to_num(cnt):
  tmp_cnt = cnt.rstrip("ms")
  pp.pprint(tmp_cnt)
  
  res_cnt = float(tmp_cnt)
  pp.pprint(res_cnt)
  
  return res_cnt
  

# for name, cnt in all_totals.items:
  # print("%s total:\t\t%d" % (name, cnt))

  
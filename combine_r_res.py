import sys
import pprint
from collections import defaultdict
pp = pprint.PrettyPrinter(indent=4)

def convert_to_num(str_cnt):
    tmp_cnt = str_cnt.rstrip("ms\n")
    # pp.pprint(tmp_cnt)
  
    total_cnts = float(tmp_cnt)
    # pp.pprint(total_cnts)  
    return total_cnts

def get_file_content():
    args = sys.argv
    filename = args[1]
    fh = open(filename,'r')
    all_lines = fh.readlines()
    fh.close()
    return all_lines
    
def print_avg(all_totals):
  print("average: ")
  for k, v in all_totals.items():
    total_cnts = v["total_cnts"];
    name_occurance = v["name_occurance"];
  
    avg = total_cnts / name_occurance

    print("%s: %.2f" % (k, avg))

def print_total(all_totals):
  print("all_totals: ")
  for k, v in all_totals.items():
    print("%s: %.2f" % (k, v["total_cnts"]))
  
# ---
all_totals = defaultdict()
all_lines = get_file_content()
name_occurance = 0

for line in all_lines:
  try:
    line_arr = line.split(": ")
    name = line_arr[1]
    str_cnt = line_arr[2]
    all_totals[name]["name_occurance"] += 1
  except KeyError:
    all_totals[name] = {}
    all_totals[name]["name_occurance"] = 1
  except IndexError:
    continue
  except:
    raise

  total_cnts = convert_to_num(str_cnt)

  curr_cnt = 0
  try:
    curr_cnt = all_totals[name]["total_cnts"]
    all_totals[name]["total_cnts"] = curr_cnt + total_cnts    
  except KeyError:
    all_totals[name]["total_cnts"] = 0
            
# print("average: ")
# for k, v in all_totals.items():
#   total_cnts = v["total_cnts"];
#   name_occurance = v["name_occurance"];
#
#   avg = total_cnts / name_occurance
#
#   print("%s: %.2f" % (k, avg))
print_avg(all_totals)
print("\n---\n")

# pp.pprint(all_totals)



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
name_cnt = 0
#
# for i in test_str:
#     if i == 'e':
#         count = count + 1
for line in all_lines:
  try:
    line_arr = line.split(": ")
    name = line_arr[1]
    str_cnt = line_arr[2]
    all_totals[name]["name_cnt"] += 1
  except KeyError:
    all_totals[name] = {}
    all_totals[name]["name_cnt"] = 1
  except IndexError:
    continue
  except:
    raise

  num_cnt = convert_to_num(str_cnt)
  print(num_cnt)

  curr_cnt = 0
  try:
    curr_cnt = all_totals[name]["num_cnt"]
    print("curr_cnt: %s" % num_cnt)
    all_totals[name]["num_cnt"] = curr_cnt + num_cnt
    
  except KeyError:
    all_totals[name]["num_cnt"] = 0
    
  for k, v in all_totals.items():
    # avg = v / n
    # avg = 0
    print("k = %s, v = %s" % (k, v))
        
# #
# #     all_totals[name][num_cnt] = curr_cnt + num_cnt
# #     all_totals[name][name_cnt] = name_cnt
# #
# #   except:
# #     raise
# # # print n
# #
# # print("average: ")
# # for k, v in all_totals.items():
# #   # avg = v / n
# #   avg = 0
# #   print "k = %s, v = %s" % (k, v)
# #   print("%s: %.2f" % (k, avg))
# # print("\n---\n")
# #
# # print("all_totals: ")
# # for k, v in all_totals.items():
# #   print("%s: %.2f" % (k, v))
# # pp.pprint(all_totals)
# #

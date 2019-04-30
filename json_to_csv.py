#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv
import io

def flatten(entry, n=None):
  if n == None:
      n = 0
  if isinstance(entry, dict):
      n = n + 1
      for k, v in entry.items():
        if k == "nomenclature":
          for k1, v1 in entry["nomenclature"].items():
            new_key = "nomenclature.%s" % k1
            print("!!!")
            print(new_key)
    
def get_leaves(item, key=None, n=None):
    if n == None:
        n = 0
    if isinstance(item, dict):
        n = n + 1
        leaves = []
        for i in item.keys():
            new_key = i
            if n == 2:
                new_key = "nomenclature.%s" % i
            leaves.extend(get_leaves(item[i], new_key, n))
        return leaves
    elif isinstance(item, list):
        leaves = []
        for i in item:
            leaves.extend(get_leaves(i, key))
        return leaves
    else:
        return [(key, item)]
        
# def get_leaves(item, key=None, n=None):
#     if n == None:
#         n = 0
#     if isinstance(item, dict):
#         n = n + 1
#         msg = "=" * 3 + "dict" + "=" * 3
#         # print(msg)
#         # print(item)
#         leaves = []
#         for i in item.keys():
#             new_key = i
#             if n == 2:
#                 new_key = "nomenclature.%s" % i
#             leaves.extend(get_leaves(item[i], new_key, n))
#             # print i
#         return leaves
#     elif isinstance(item, list):
#         msg = "-" * 3 + "list" + "-" * 3
#         # print(msg)
#         leaves = []
#         for i in item:
#             leaves.extend(get_leaves(i, key))
#         return leaves
#     else:
#         # print("n = %d") % n
#         # print("key = %s, item = %s") % (key, item)
#         return [(key, item)]
#
#Function that recursively extracts values out of the object into a flattened dictionary
# def flatten_json(data):
#     flat = [] #list of flat dictionaries
#     def flatten(y):
#         out = {}
#
#         def flatten2(x, name=''):
#             if type(x) is dict:
#                 for a in x:
#                     print("a = %s") % a
#                     if a == "name":
#                             flatten2(x["value"], name + x[a] + '_')
#                     else:
#                         flatten2(x[a], name + a + '_')
#             elif type(x) is list:
#                 for a in x:
#                     flatten2(a, name + '_')
#             else:
#                 out[name[:-1]] = x
#
#         flatten2(y)
#         # print("out")
#         # print(out)
#         return out
#
if __name__ == "__main__":
  file_in = "test2.json"
  file_out = "test2_out.json"
  with open(file_in) as f_input, io.open(file_out, "w", encoding='utf8') as f_output:
      csv_output = csv.writer(f_output, delimiter=";")
      write_header = True

      for entry in json.load(f_input):
          # print(entry)
          # leaf_entries = flatten(entry)
          leaf_entries = sorted(get_leaves(entry))
          print(leaf_entries)
          if write_header:
              csv_output.writerow([k for k, v in leaf_entries])
              write_header = False

          csv_output.writerow([unicode(v).encode("utf-8") for k, v in leaf_entries])
  #
# if __name__ == "__main__":
#     ProcessLargeTextFile()

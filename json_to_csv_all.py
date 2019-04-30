#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import csv

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

def split_json(f_input):
  all_data1 = f_input.read()
  rep = '},%s{' % (os.linesep)
  all_data_sep = all_data1.replace('},{', rep)
  return all_data_sep
  
# def make_json_obj(all_data_sep):
#   # json.dumps([all_data_sep])
#   for chunk in json.JSONEncoder().iterencode([all_data_sep]):
    

if __name__ == "__main__":
  file_in = "test.json"
  file_out = "test_out.json"
  with open(file_in) as f_input, open(file_out, "wt") as f_output:
      csv_output = csv.writer(f_output, delimiter=";", quoting=csv.QUOTE_ALL)
      write_header = True
      
      all_data_sep = split_json(f_input)
      # all_data_sep_list = make_json_obj(all_data_sep)

      # for entry in json.loads(all_data_sep_list):
      for entry in json.JSONEncoder().iterencode(all_data_sep):      
          leaf_entries = sorted(get_leaves(entry))
          if write_header:
              row = [k for k, v in leaf_entries]
              csv_output.writerow(row)
              write_header = False

          csv_output.writerow([v for k, v in leaf_entries])

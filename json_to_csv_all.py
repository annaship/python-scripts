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

def split_str(f_input):
  all_data1 = f_input.read()
  rep = '}###%s{' % (os.linesep)
  all_data_sep = all_data1.replace('[', '').replace(']', '').replace('},{', rep)
  all_data_sep_list = all_data_sep.split("###")
  return all_data_sep_list

if __name__ == "__main__":
  file_in = "test.json"
  file_out = "test_out.json"
  with open(file_in) as f_input, open(file_out, "wt") as f_output:
      csv_output = csv.writer(f_output, delimiter=";", quoting=csv.QUOTE_ALL)
      write_header = True

      all_data_sep_list = split_str(f_input)
      for chunk in all_data_sep_list:
          entry = ""
          try:
            entry = json.loads(chunk)
          except ValueError:
            print("*" * 3 + "ERR: " + "*" * 3)
            print(chunk)
            raise

          leaf_entries = sorted(get_leaves(entry))
          if write_header:
              row = [k for k, v in leaf_entries]
              csv_output.writerow(row)
              write_header = False

          csv_output.writerow([v for k, v in leaf_entries])

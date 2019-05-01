#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import json
import csv

# If structture can be different that should be generalized, instead of using "nomenclature" and level 2
def get_leaves(item, key=None, n=None):
    sub_dict_name = "nomenclature"
    sub_dict_level = 2
    
    if n == None:
        n = 0
    if isinstance(item, dict):
        n = n + 1
        leaves = []
        for i in item.keys():
            new_key = i
            if n == sub_dict_level:
                new_key = "%s.%s" % (sub_dict_name, i)
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
  all_data_sep = all_data1.lstrip('[').rstrip(']').replace('},{', rep)
  all_data_sep_list = all_data_sep.split("###")
  return all_data_sep_list

def elapsed(start_name):
  return time.time() - start_name
    
def get_file_names():
  parser = argparse.ArgumentParser()

  parser.add_argument("--json_file_in", "-f", type=str, required=True)
  parser.add_argument("--csv_file_out", "-o", type=str, required=True)
  args = parser.parse_args()
  return(args.json_file_in, args.csv_file_out)
  
def write_into_csv(leaf_entries, write_header):
  if write_header:
      row = [k for k, v in leaf_entries]
      csv_output.writerow(row)
      write_header = False

  csv_output.writerow([v for k, v in leaf_entries])
  return write_header
  
if __name__ == "__main__":
  start_all = time.time()
  
  file_in, file_out = get_file_names()

  with open(file_in) as f_input, open(file_out, "wt") as f_output:
      csv_output = csv.writer(f_output, delimiter=";", quoting=csv.QUOTE_ALL)
      write_header = True

      print("Separating...")
      start_sep = time.time()
      all_data_sep_list = split_str(f_input)
      print('%.3fs: separating time' % elapsed(start_sep))
      all_data_sep_list_len = len(all_data_sep_list)
      print("There are %d entries" % all_data_sep_list_len)

      print("Flattening and writing CSV...")
      convert_and_write_csv_time = time.time()
      list_of_dicts = list(map(lambda chunk: json.loads(chunk), all_data_sep_list))
      leaf_entries_all = list(map(lambda entry: sorted(get_leaves(entry)), list_of_dicts))
      
      for leaf_entries in leaf_entries_all:
        write_header = write_into_csv(leaf_entries, write_header)

      print(leaf_entries_all)
      
      # for chunk in all_data_sep_list:
      # list(map(lambda x: x**2, items))
      #   res = map(lambda chunk: json.loads(chunk), all_data_sep_list)
      #   try:
      #     entry = json.loads(chunk)
      #   except:
      #     print("ERR in :")
      #     print(chunk)
      #     raise
      #   leaf_entries = sorted(get_leaves(entry))
      #   write_header = write_into_csv(leaf_entries, write_header)
        
      print('%.3fs: convert_and_write_csv_time' % elapsed(convert_and_write_csv_time))

  print('---\n%.3fs: total time' % elapsed(start_all))
  

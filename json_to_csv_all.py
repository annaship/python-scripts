#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import json
import csv

# If structture can be different that should be generalized, instead of using "nomenclature"
def get_leaves(item, key=None, n=None):
    sub_dict_name = "nomenclature"
    if n == None:
        n = 0
    if isinstance(item, dict):
        n = n + 1
        leaves = []
        for i in item.keys():
            new_key = i
            if n == 2:
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
      time_sep = elapsed(start_sep)
      print('%.3fs: separating time' % time_sep)
      
      print("Flattening and writing CSV...")
      time_covert_and_write_csv = time.time()
      for chunk in all_data_sep_list:
        entry = json.loads(chunk)
        leaf_entries = sorted(get_leaves(entry))
        write_header = write_into_csv(leaf_entries, write_header)
        
      time_covert_and_write_csv_tot = elapsed(time_covert_and_write_csv)
      print('%.3fs: time_covert_and_write_csv' % time_covert_and_write_csv_tot)

  time_all = elapsed(start_all)
  print('---\n%.3fs: total time' % time_all)
  

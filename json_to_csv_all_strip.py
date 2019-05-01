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
  all_data_sep = all_data1.lstrip('[').rstrip(']').rstrip(',').replace('},{', rep)
  all_data_sep_list = all_data_sep.split("###")
  return all_data_sep_list

def timer(start, end, msg = ""):
  hours, rem = divmod(end-start, 3600)
  minutes, seconds = divmod(rem, 60)
  print(msg)
  print("{:0>2}:{:0>2}:{:05.3f}".format(int(hours), int(minutes), seconds))

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

      sep_end = time.time()
      print("separating time: ")
      timer(start_sep, sep_end, "Separating time: ")
      
      all_data_sep_list_len = len(all_data_sep_list)
      print("There are %d entries" % all_data_sep_list_len)

      print("Convert JSON...")
      start_json_loads_time = time.time()
      list_of_dicts = list(map(lambda chunk: json.loads(chunk), all_data_sep_list))
      end_json_loads_time = time.time()
      timer(start_json_loads_time, end_json_loads_time, "Convert JSON time: ")
      
      print("Convert JSON 2...")
      start_json_loads2_time = time.time()
      list_of_dicts = [json.loads(chunk) for chunk in all_data_sep_list]
      # list(map(lambda chunk: json.loads(chunk), all_data_sep_list))
      end_json_loads2_time = time.time()
      timer(start_json_loads2_time, end_json_loads2_time, "Convert JSON 2 time: ")

      print("Flattening...")
      start_flattening_time = time.time()
      leaf_entries_all = list(map(lambda entry: sorted(get_leaves(entry)), list_of_dicts))
      end_flattening_time = time.time()
      timer(start_flattening_time, end_flattening_time, "Flattening time: ")
      
      print("Flattening 2...")
      start_flattening_time2 = time.time()
      leaf_entries_all = [sorted(get_leaves(entry)) for entry in list_of_dicts]
      end_flattening_time2 = time.time()
      timer(start_flattening_time2, end_flattening_time2, "Flattening 2 time: ")
      
      print("Writing CSV...")
      start_write_csv_time = time.time()
      for leaf_entries in leaf_entries_all:
        write_header = write_into_csv(leaf_entries, write_header)
      end_write_csv_time = time.time()
      timer(start_write_csv_time, end_write_csv_time, "Writing CSV time: ")

  end_all = time.time()
  timer(start_all, end_all, "Total time: ")
  

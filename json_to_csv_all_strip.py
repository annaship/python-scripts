#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import csv
try:
    import simplejson as json
    print("use simplejson")
except ImportError:
    import json
    print("use json")
        
# If structture can be different that should be generalized, instead of using "nomenclature"
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
      timer(start_sep, sep_end, "Separating time: ")

      all_data_sep_list_len = len(all_data_sep_list)
      print("There are %d entries" % all_data_sep_list_len)
            
      print("By chunks: convert JSON, flatten the dict and write to CSV...")
      start_chunks = time.time()      
      for chunk in all_data_sep_list:
        try:
          entry = json.loads(chunk)
        except ValueError: #Value is too big!
          print(chunk)
          raise
          
        leaf_entries = sorted(get_leaves(entry))        
        write_header = write_into_csv(leaf_entries, write_header)
      end_chunks = time.time()
      timer(start_chunks, end_chunks, "Converting, flattening and writing time: ")

  end_all = time.time()
  timer(start_all, end_all, "Total time: ")  

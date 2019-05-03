#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import os
import csv
import json

def flatten(current, key="", result={}):
    if isinstance(current, dict):
        for k in current:
            new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
            flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result
    
"""def recursive_generator(lis):
    yield lis[0]
    yield from recursive_generator(lis[1:])

for k in recursive_generator([6,3,9,1]):
    print(k)""" 


def flatten_gen(current, key="", result={}):
    if isinstance(current, dict):
        for k in current:
            new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
            yield from flatten_gen(current[k], new_key, result)
    else:
        result[key] = current
        yield result
    # return result
    # yield result
    
# with open('sells.log') as file:
#     pizza_col = (line[3] for line in file)
#     per_hour = (int(x) for x in pizza_col if x != 'N/A')
#     print("Total pizzas sold = ",sum(per_hour))
    

def split_str(f_input):
  all_data1 = f_input.read()
  rep = '}###%s{' % (os.linesep)
  all_data_sep = all_data1.lstrip('[').rstrip(']').rstrip(',').replace('},{', rep)
  all_data_sep_list = all_data_sep.split("###")
  return all_data_sep_list

def acc_timer(accumulated_time, msg = ""):
  hours, rem = divmod(accumulated_time, 3600)
  minutes, seconds = divmod(rem, 60)
  print(msg)
  print("{:0>2}:{:0>2}:{:05.3f}".format(int(hours), int(minutes), seconds))  

def get_args():
  parser = argparse.ArgumentParser()

  parser.add_argument("--json_file_in", "-f", type=str, required=True)
  parser.add_argument("--csv_file_out", "-o", type=str, required=True)
  parser.add_argument("--benchmark", "-b", action="store_false", help="Do not mesure and print time")
  
  args = parser.parse_args()

  return args

def write_into_csv(leaf_entries, write_header):
  if write_header:
      row = [k for k, v in leaf_entries.items()]
      csv_output.writerow(row)
      write_header = False

  csv_output.writerow([v for k, v in leaf_entries.items()])
  return write_header

if __name__ == "__main__":
  start_all = time.time()
  
  args = get_args()
  file_in = args.json_file_in
  file_out = args.csv_file_out
  to_benchmark = args.benchmark
  
  if to_benchmark:
    json_total_time = 0
    get_leaves_total_time = 0
    write_into_csv_total_time = 0

  with open(file_in) as f_input, open(file_out, "wt") as f_output:
      csv_output = csv.writer(f_output, delimiter=";", quoting=csv.QUOTE_ALL)
      write_header = True

      print("Separating...")
      if to_benchmark:
        start_sep = time.time()
      all_data_sep_list = split_str(f_input)
      if to_benchmark:
        sep_end = time.time()
        acc_timer((time.time() - start_sep), "Separating time: ")

      all_data_sep_list_len = len(all_data_sep_list)
      if to_benchmark:
        print("There are %d entries" % all_data_sep_list_len)

      print("By chunks: convert JSON, flatten the dict and write to CSV...")
      if to_benchmark:
        start_chunks = time.time()
      # doing separately this 3 operations takes too much memory to keep intermediate results
      for chunk in all_data_sep_list:        
        if to_benchmark:
          start_json = time.time()
        entry = json.loads(chunk)
        if to_benchmark:
          json_total_time += time.time() - start_json

        if to_benchmark:
          start_get_leaves = time.time()
        flatten_dicts = flatten_gen(entry) 
        if to_benchmark:
          get_leaves_total_time += time.time() - start_get_leaves

        for next_dict in flatten_dicts:
          print("LLL")
          print(next_dict)
          if to_benchmark:
            start_write_into_csv = time.time()
          write_header = write_into_csv(next_dict, write_header)
          if to_benchmark:
            write_into_csv_total_time += time.time() - start_write_into_csv

  if to_benchmark:
    acc_timer((time.time() - start_all), '---\nTotal time: ')

    acc_timer(json_total_time, '---\nTime converting JSON:')
    acc_timer(get_leaves_total_time, 'Time flattening the dicts:')
    acc_timer(write_into_csv_total_time, 'Time writing to CSV:')

  print("Done")

#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import csv
import json
import functools
import gc
import os
import psutil
from collections import namedtuple


class Json_str(namedtuple('Json_str', ['file_object', 'buffersize'])):
    __slots__ = ()

    def json_parse(self, file_object, buffersize = 2048):
        """ Small function to parse a file containing JSON objects separated by a new line. This format is used in the live-rundata-xx.json files produces by SMAC.

        taken from http://stackoverflow.com/questions/21708192/how-do-i-use-the-json-module-to-read-in-one-json-object-at-a-time/21709058#21709058
        """
        buffer = ''
        for chunk in iter(functools.partial(file_object.read, buffersize), ''):
            if log_file_path:
                log_file.write("\n---\nIn json_parse. Before replaces")
                log_mem()
            buffer += chunk.lstrip('[').rstrip(']').replace('},]', '}]').strip(' \n')
            buffer = buffer.replace('},{', '}{')

            while buffer:
                if log_file_path:
                    log_file.write("\nIn json_parse. Before raw_decode")
                    log_mem()
                try:
                    result, index = json.JSONDecoder().raw_decode(buffer)
                    yield result
                    buffer = buffer[index:]
                    if log_file_path:
                        log_file.write("\nIn json_parse. After raw_decode")
                        log_mem()
                except ValueError:
                    # Not enough data to decode, read more
                    break

def flatten(current, key="", result={}):
    if isinstance(current, dict):
        for k in current:
            new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
            flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result

def write_into_csv(leaf_entries, write_header):
    if write_header:
        row = [k for k, v in leaf_entries.items()]
        csv_output.writerow(row)
        write_header = False

    csv_output.writerow([v for k, v in leaf_entries.items()])
    if log_file_path:
        log_file.write("\nIn write_into_csv. After writerow")
        log_mem()

    return write_header


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
  parser.add_argument("--buffer_size", "-s", type=int, required=False)
  parser.add_argument("--log_file_path", "-l", type=str, required=False)
                      # , action="store_true")

  args = parser.parse_args()

  return args

def log_mem():
    process = psutil.Process(os.getpid())
    log_file.write("\nmemory_info: ")
    mem_mb = process.memory_info().rss / 1024 / 1024
    log_file.write(str(mem_mb))  # in Mbytes

    memory_dict = dict(psutil.virtual_memory()._asdict())
    log_file.write("\nmemory used: ")
    log_file.write(str(memory_dict['used']  / 1024 / 1024 ))

if __name__ == "__main__":
  start_all = time.time()
  __slots__ = ()
  
  args = get_args()
  file_in = args.json_file_in
  file_out = args.csv_file_out
  to_benchmark = args.benchmark
  buffer_size = args.buffer_size
  log_file_path = args.log_file_path

  if log_file_path:
      # log_file_path = "/Users/ashipunova/split_json.log"
      log_file = open(log_file_path, "a+")
      memory_dict = dict(psutil.virtual_memory()._asdict())
      log_file.write("\nBefore start memory info in MB: ")
      for k,v in memory_dict.items():
          in_mb = v / 1024 / 1024
          msg = "\n%s: %d" % (k, in_mb)
          log_file.write(msg)

  if to_benchmark:
    sep_total_time = 0
    json_total_time = 0
    get_leaves_total_time = 0
    write_into_csv_total_time = 0

  with open(file_in, "r") as f_input, open(file_out, "wt") as f_output:
      csv_output = csv.writer(f_output, delimiter=";", quoting=csv.QUOTE_ALL)
      write_header = True

      collect_ends = ""
      all_data_sep_list_len_total = 0
      print("By chunks: separate, convert JSON, flatten the dict and write to CSV...")
      json_obj = Json_str(f_input, buffer_size)
      for data in json_obj.json_parse(f_input, buffer_size):
          if to_benchmark:
              all_data_sep_list_len_total += 1

              if log_file_path:
                  log_file.write("\n\nEntry # %d" % all_data_sep_list_len_total)
                  log_file.write("\nFlattening...")
                  log_mem()

              start_get_leaves = time.time()
          leaf_entries = flatten(data)
          if to_benchmark:
              get_leaves_total_time += time.time() - start_get_leaves
              if log_file_path:
                  log_file.write("\nget_leaves_total_time = %d" % get_leaves_total_time)
                  log_mem()

          if log_file_path:
              log_file.write("\n\nstart_write_into_csv")

          if to_benchmark:
              start_write_into_csv = time.time()
          write_header = write_into_csv(leaf_entries, write_header)
          if to_benchmark:
              write_into_csv_total_time += time.time() - start_write_into_csv
              if log_file_path:
                  log_file.write("\nwrite_into_csv_total_time = %d" % write_into_csv_total_time)
                  log_mem()

  if to_benchmark:
    print("There are %d entries" % all_data_sep_list_len_total)
    acc_timer((time.time() - start_all), '---\nTotal time: ')

    # acc_timer(sep_total_time, '---\nSeparating time: ')
    # acc_timer(json_total_time, 'Time converting JSON:')
    acc_timer(get_leaves_total_time, 'Time flattening the dicts:')
    acc_timer(write_into_csv_total_time, 'Time writing to CSV:')

  print("Done")

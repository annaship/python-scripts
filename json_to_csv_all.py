#! /usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import time
import csv
import json
import functools
import gc

def flatten(current, key="", result={}):
    if isinstance(current, dict):
        for k in current:
            new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
            flatten(current[k], new_key, result)
    else:
        result[key] = current
    return result


def json_parse(file_object, buffersize = 2048):
    """ Small function to parse a file containing JSON objects separated by a new line. This format is used in the live-rundata-xx.json files produces by SMAC.

    taken from http://stackoverflow.com/questions/21708192/how-do-i-use-the-json-module-to-read-in-one-json-object-at-a-time/21709058#21709058
    """
    buffer = ''
    for chunk in iter(functools.partial(file_object.read, buffersize), ''):
        buffer += chunk.lstrip('[').rstrip(']').replace('},]', '}]')
        buffer = buffer.replace('},{', '}{')
        while buffer:
            try:
                result, index = json.JSONDecoder().raw_decode(buffer)
                yield result
                buffer = buffer[index:]
            except ValueError:
                # Not enough data to decode, read more
                break


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

def split_short_str(input_piece, collect_ends):
  rep = '}###{'
  all_data_sep = (collect_ends + input_piece).lstrip('[').rstrip(']').replace('},{', rep).replace('},]', '}]')
  all_data_sep_list_interim = all_data_sep.split("###")
  collect_ends = all_data_sep_list_interim[-1]
  all_data_sep_list = all_data_sep_list_interim[:-1]
  return (all_data_sep_list, collect_ends)

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
  parser.add_argument("--log_file_path", "-l", action="store_true")

  args = parser.parse_args()

  return args

def write_into_csv(leaf_entries, write_header):
  if write_header:
      row = [k for k, v in leaf_entries.items()]
      csv_output.writerow(row)
      write_header = False

  csv_output.writerow([v for k, v in leaf_entries.items()])
  gc.collect()
  return write_header

if __name__ == "__main__":
  start_all = time.time()
  
  args = get_args()
  file_in = args.json_file_in
  file_out = args.csv_file_out
  to_benchmark = args.benchmark
  buffer_size = args.buffer_size
  log_file_path = args.log_file_path

  if log_file_path:
      log_file_path = "/Users/ashipunova/split_json.log"
      log_file = open(log_file_path, "a+")
      # log_file.write("buffer_size = %d" % buffer_size) % TypeError: %d format: a number is required, not NoneType

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
      for data in json_parse(f_input, buffer_size):
          if to_benchmark:
              all_data_sep_list_len_total += 1

              if log_file_path:
                  log_file.write("\nall_data_sep_list_len_total = %d" % all_data_sep_list_len_total)
                  log_file.write("\nstart_get_leaves\n")

              start_get_leaves = time.time()
          leaf_entries = flatten(data)
          if to_benchmark:
              get_leaves_total_time += time.time() - start_get_leaves
              if log_file_path:
                  log_file.write("\nget_leaves_total_time = %d" % get_leaves_total_time)

          if log_file_path:
              log_file.write("\nstart_write_into_csv\n")

          if to_benchmark:
              start_write_into_csv = time.time()
          write_header = write_into_csv(leaf_entries, write_header)
          if to_benchmark:
              write_into_csv_total_time += time.time() - start_write_into_csv
              if log_file_path:
                  log_file.write("\nwrite_into_csv_total_time = %d" % write_into_csv_total_time)

  if to_benchmark:
    print("There are %d entries" % all_data_sep_list_len_total)
    acc_timer((time.time() - start_all), '---\nTotal time: ')

    # acc_timer(sep_total_time, '---\nSeparating time: ')
    # acc_timer(json_total_time, 'Time converting JSON:')
    acc_timer(get_leaves_total_time, 'Time flattening the dicts:')
    acc_timer(write_into_csv_total_time, 'Time writing to CSV:')

  print("Done")

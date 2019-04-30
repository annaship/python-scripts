#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv
import io

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

if __name__ == "__main__":
  file_in = "test2.json"
  file_out = "test2_out.json"
  with open(file_in) as f_input, io.open(file_out, "w", encoding='utf8') as f_output:
      csv_output = csv.writer(f_output, delimiter=";")
      write_header = True

      for entry in json.load(f_input):
          leaf_entries = sorted(get_leaves(entry))
          print(leaf_entries)
          if write_header:
              csv_output.writerow([k for k, v in leaf_entries])
              write_header = False

          csv_output.writerow([unicode(v).encode("utf-8") for k, v in leaf_entries])
  #
# if __name__ == "__main__":
#     ProcessLargeTextFile()

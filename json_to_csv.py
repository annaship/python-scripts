#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv
import io

def get_leaves(item, key=None):
    if isinstance(item, dict):
        msg = "=" * 3 + "dict" + "=" * 3 
        print(msg)
        leaves = []
        for i in item.keys():
            leaves.extend(get_leaves(item[i], i))
            print i
        return leaves
    elif isinstance(item, list):
        msg = "-" * 3 + "list" + "-" * 3 
        print(msg)
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

          if write_header:
              csv_output.writerow([unicode(k).encode("utf-8") for k, v in leaf_entries])
              write_header = False

          csv_output.writerow([unicode(v).encode("utf-8") for k, v in leaf_entries])
  #
# if __name__ == "__main__":
#     ProcessLargeTextFile()

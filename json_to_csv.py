#! /usr/bin/python
# -*- coding: utf-8 -*-

import json
import csv

def get_leaves(item, key=None):
    if isinstance(item, dict):
        leaves = []
        for i in item.keys():
            leaves.extend(get_leaves(item[i], i))
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
  with open(file_in) as f_input, open(file_out, "wb") as f_output:
      csv_output = csv.writer(f_output)
      write_header = True

      for entry in json.load(f_input):
          leaf_entries = sorted(get_leaves(entry))

          if write_header:
              csv_output.writerow([k for k, v in leaf_entries])
              write_header = False

          # self.writer.writerow([unicode(s).encode("utf-8") for s in row])

          csv_output.writerow([unicode(v).encode("utf-8") for k, v in leaf_entries])
  #
# if __name__ == "__main__":
#     ProcessLargeTextFile()

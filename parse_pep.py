#! /usr/bin/env python

from collections import defaultdict


class Pep():
  def __init__(self, data):
    self.entries_dict = defaultdict()
    str_data = self.strip_n(data)
    self.entries = list(self.group(str_data, 'SeqID:'))
    self.group_dict()
    # self.good_res = []
    self.choose_entry()

  def strip_n(self, data):
    return [l.strip() for l in data]

  def choose_entry(self):
    temp_arr = []
    for e in self.entries:
      if any(x.strip().endswith("[Signal peptide detected]") for x in e):
        temp_arr.append(e)
    for e1 in temp_arr:
      pass

  def group_dict(self):
    for el in self.entries:
      temp_dict = {}
      # print("TTTT")
      try:
        # if el[0].startswith("SeqID"):
        self.entries_dict[el[0]] = {}
        r1 = list(self.group(el, 'Signal+'))
        r2 = list(self.group(r1[1], 'Final Prediction:'))
        # temp_arr = r1[0] + r2
        temp_dict["First part"] = r1[0]
        temp_dict["Signal"] = r2[0]
        temp_dict["Final Prediction"] = r2[1]
        self.entries_dict[el[0]] = temp_dict
        # self.entries_dict[el[0]].append(r2)

      except IndexError:
        pass
      # if el.startswith(sep):
      #   self.entries_dict[el.strip()] = []
      # else:
      #   temp_arr.append(el.strip())

    #     yield temp_arr
    #     temp_arr = []
    #   temp_arr.append(el)
    # yield temp_arr

  def group(self, seq, sep):
    temp_arr = []
    for el in seq:
      if el.startswith(sep):
        yield temp_arr
        temp_arr = []
      temp_arr.append(el)
    yield temp_arr


if __name__ == "__main__":
  file_in = "/Users/ashipunova/work/emil/parse/file_in.txt"
  file_out = "/Users/ashipunova/work/emil/parse/file_out.txt"

  with open(file_in) as f_input:
    data = f_input.readlines()

  # print(data[0:100])
  pep = Pep(data)
  # result = list(pep.group(data, 'SeqID:'))
  # print(result)
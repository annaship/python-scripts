#! /usr/bin/env python


class Pep():
  def __init__(self, data):
    self.entries = list(self.group(data, 'SeqID:'))
    self.good_res = []
    self.choose_entry()

  def choose_entry(self):
    temp_arr = []
    for e in self.entries:
      if any(x.strip().endswith("[Signal peptide detected]") for x in e):
        temp_arr.append(e)
    for e1 in temp_arr:
      pass

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
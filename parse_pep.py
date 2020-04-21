#! /usr/bin/env python

from collections import defaultdict


class Pep():
  def __init__(self, data):
    self.entries_dict = defaultdict()
    str_data = self.strip_n(data)
    self.entries = list(self.group(str_data, 'SeqID:'))
    self.group_dict()
    self.good_res = []
    self.choose_entry()
    self.clean_res()

  def clean_res(self):
    pass
    # for x in pep.entries_dict.values():
    #   if any(e.startswith("Extracellular") for e in x['Final Prediction']):
        # print(x['Final Prediction'])
        # print(x)

  def strip_n(self, data):
    return [l.strip() for l in data]

  def choose_entry(self):
    # temp_arr = []
    for k, v_d in self.entries_dict.items():
      if any(e.endswith("[Signal peptide detected]") for e in v_d['Signal']):
        if any(e.startswith("Extracellular") for e in v_d['Final Prediction']):
          self.good_res.append(v_d)
        # [x for x in self.entries_dict.values() if any(e.startswith("Extracellular") for e in x['Final Prediction'])]
        # self.good_res = [v for k, v in d.items() for d in temp_arr]

    #       for d in pep.good_res:
    #     for k, v in d.items():
    #       print("\n".join(v))
    # self.good_res = [x for x in self.entries_dict.values() if any(e.startswith("Extracellular") for e in x['Final Prediction'])]
    # for x in pep.entries_dict.values():
    #   if any(e.startswith("Extracellular") for e in x['Final Prediction']):

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

  pep = Pep(data)

  for d in pep.good_res:
    for k, v in d.items():
      print("\n".join(v))

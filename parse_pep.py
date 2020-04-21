#! /usr/bin/env python

from collections import defaultdict
import argparse


class Pep:
  def __init__(self, data):
    self.entries_dict = defaultdict()
    str_data = self.strip_n(data)
    self.entries = list(self.group(str_data, 'SeqID:'))
    self.group_dict()
    self.good_res = []
    self.choose_entry()
    self.out_txt = ""
    self.form_res()

    # self.print_res()

  def form_res(self):
    for d in self.good_res:
      all_arr = []
      self.out_txt += "\n"
      for k, v in d.items():
        all_arr = all_arr + v
      self.out_txt += "\n".join(all_arr)

  def print_res(self):
    for d in self.good_res:
      for k, v in d.items():
        print("\n".join(v))

  def strip_n(self, data):
    return [line.strip() for line in data]

  def choose_entry(self):
    for k, v_d in self.entries_dict.items():
      try:
        if any(e.endswith("[Signal peptide detected]") for e in v_d['Signal']):
          if any(e.startswith("Extracellular") for e in v_d['Final Prediction']):
            self.good_res.append(v_d)
      except KeyError:
        pass

  def group_dict(self):
    for el in self.entries:
      temp_dict = {}
      try:
        self.entries_dict[el[0]] = {}
        r1 = list(self.group(el, 'Signal'))
        r2 = list(self.group(r1[1], 'Final Prediction:'))
        temp_dict["First part"] = r1[0]
        temp_dict["Signal"] = r2[0]
        temp_dict["Final Prediction"] = r2[1]
        self.entries_dict[el[0]] = temp_dict

      except IndexError:
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

  parser = argparse.ArgumentParser(description = """Cuts the first 5 characters from sequences and quality lines.
  Input: gzipped fastq files.
  Output: the new shortened fastq entries and a log file with original file name and the cut 5nt sequences.""",
                                   formatter_class = argparse.RawTextHelpFormatter)

  parser.add_argument('-i', '--input_file',
                      required = True, action = 'store', dest = 'input_file',
                      help = """Input file name"""),

  parser.add_argument("-o", "--output_file",
                      required = True, action = "store", dest = "output_file",
                      help = """Output file name""")

  args = parser.parse_args()

  with open(args.input_file) as f_input:
    data = f_input.readlines()

  pep = Pep(data)

  with open(args.output_file, 'w') as f_output:
        f_output.write(pep.out_txt)

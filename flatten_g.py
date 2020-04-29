#! /usr/bin/env python

from collections import defaultdict
import argparse
from collections import Iterable

"""Flatten the input text by 'SeqID' """

class Gene_data:
  """Assuming the following format:
  SeqID: bin.61.orig_c_000000000001_182 rank: A; bfm:BP422_14495 undecaprenyldiphospho-muramoylpentapeptide beta-N-acetylglucosaminyltransferase; K02563 (db=kegg)
  Analysis Report:
    CMSVM+            Unknown                       [No details]
    CWSVM+            Unknown                       [No details]
    CytoSVM+          Unknown                       [No details]
    ECSVM+            Unknown                       [No details]
    ModHMM+           Unknown                       [No internal helices found]
    Motif+            Unknown                       [No motifs found]
    Profile+          Unknown                       [No matches to profiles found]
    SCL-BLAST+        CytoplasmicMembrane           [matched 127540: UDP-N-acetylglucosamine--N-acetylmuramyl-(pentapeptide) pyrophosphoryl-undecaprenol N-acetylglucosamine transferase]
    SCL-BLASTe+       Unknown                       [No matches against database]
    Signal+           Unknown                       [No signal peptide detected]
  Localization Scores:
    CytoplasmicMembrane    9.51
    Cytoplasmic            0.17
    Cellwall               0.16
    Extracellular          0.15
  Final Prediction:
    CytoplasmicMembrane    9.51

-------------------------------------------------------------------------------
  """
  def __init__(self, data):
    self.entries_dict = defaultdict()
    str_data = self.strip_n(data)
    self.entries = list(self.group(str_data, 'SeqID:'))
    # if key with search just search in entries and printout
    self.good_res = []
    self.out_txt = ""
    self.search_str_res = []

    # self.print_res()

  def flatten(self, collection):
    for x in collection:
      if isinstance(x, Iterable) and not isinstance(x, str):
        yield from self.flatten(x)
      else:
        yield x

  def search_in_entry(self, search_str):
    for entry in self.entries:
      self.search_str_res.append([entry for e in entry if e.startswith(search_str)])

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

  parser = argparse.ArgumentParser()

  parser.add_argument('-i', '--input_file',
                      required = True, action = 'store', dest = 'input_file',
                      help = """Input file name"""),

  parser.add_argument("-o", "--output_file",
                      required = True, action = "store", dest = "output_file",
                      help = """Output file name""")

  parser.add_argument("-s", "--search_str", required = True, action = "append", nargs = 1,
                      metavar = "search_str",
                      help = """The category to search in and a String to search for, divided by #""")

  args = parser.parse_args()

  with open(args.input_file) as f_input:
    data = f_input.readlines()

  pep = Gene_data(data)

  if args.search_str:
    pep.search_in_entry(args.search_str)
    if pep.search_str_res:
      out_txt = "\n".join(pep.flatten(pep.search_str_res))
  else:
    pep.group_dict()
    pep.choose_entry()
    pep.form_res()
    out_txt = pep.out_txt

  with open(args.output_file, 'w') as f_output:
        # f_output.write(pep.out_txt)
        f_output.write(out_txt)
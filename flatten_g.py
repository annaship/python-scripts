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
    self.good_res = []
    self.out_txt = ""
    self.search_str_res = []
    self.group_names = ['Analysis Report:', 'Localization Scores', 'Final Prediction:']

  def form_res(self):
    for d in self.good_res:
      all_arr = []
      for k, v in d.items():
        all_arr.append(k)
        # self.out_txt += "\n" + k + "\n"
        for part in v.values():
          all_arr = all_arr + part
      self.out_txt += "\n"
      self.out_txt += "\n".join(all_arr)

  # def print_res(self):
  #   for d in self.good_res:
  #     for k, v in d.items():
  #       print("\n".join(v))

  def strip_n(self, data):
    return [line.strip() for line in data]

  def get_search_pairs(self, search_str_arr):
    self.search_str_res = [el[0].split("#") for el in search_str_arr]

  def choose_entry(self, search_str_arr):
    self.get_search_pairs(search_str_arr)
    for key_id, val_dict in self.entries_dict.items():
      test_list = []
      for pair in self.search_str_res:
        try:
          test_list.append(any(pair[1] in e for e in val_dict[pair[0]]))
        except KeyError:
          pass
      if all(test_list):
        self.good_res.append({key_id: val_dict})

  def recursive_group_dict(self, test_element, temp_dict):
    for group_number, group_name in enumerate(self.group_names):
      temp_res = []
      # separate_id_from_body = list(self.group(test_element, group_name))
      if group_number < len(self.group_names) - 1:
        temp_res = list(self.group(test_element, self.group_names[group_number + 1]))
        temp_dict[group_name] = temp_res[0]
        self.recursive_group_dict(temp_res[1], temp_dict)
      else:
        temp_dict[self.group_names[group_number + 1]] = temp_res[1]
        self.entries_dict[test_element[0]] = temp_dict

  def group_dict(self):
    for el in self.entries:
      temp_dict = {}
      try:
        self.entries_dict[el[0]] = {}
        self.recursive_group_dict(el[1:], temp_dict)

          # temp_dict[group_name] = gr_res[0]
          # gr1 = list(self.group(el, 'Analysis Report:'))
          # gr2 = list(self.group(gr1[1], 'Localization Scores:'))
          # temp_dict['Analysis Report'] = gr2[0]
          # gr3 = list(self.group(gr2[1], 'Final Prediction:'))
          # temp_dict['Localization Scores'] = gr3[0]
          # temp_dict['Final Prediction'] = gr3[1]
          # self.entries_dict[el[0]] = temp_dict

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
                      help = """The category to search in and a String to search for, divided by '#'""")

  args = parser.parse_args()

  with open(args.input_file) as f_input:
    data = f_input.readlines()

  pep = Gene_data(data)

  pep.group_dict()
  pep.choose_entry(args.search_str)
  pep.form_res()
  out_txt = pep.out_txt

  with open(args.output_file, 'w') as f_output:
        f_output.write(out_txt)
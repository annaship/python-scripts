from itertools import islice

def get_sequence_taxa():
  sequence_taxa_f_name = "/Users/ashipunova/work/dada2/stephen_fastq/t_taxa.txt"
  sequence_taxa_f = open(sequence_taxa_f_name, "r")
  all_lines = sequence_taxa_f.readlines()
  spls = [line.strip("\n").split("#") for line in all_lines]
  seq_t_d = {s: t for s, t in spls}
  return seq_t_d

def get_dada_freq_res():
  freq_csv = "/Users/ashipunova/work/dada2/stephen_fastq/seqtab.nochim.csv"
  freq_csv_f = open(freq_csv, "r")
  array_by4 = []
  n = 4
  while True:
      next_n_lines = list(islice(freq_csv_f, n))
      if not next_n_lines:
              break
      array_by4.append(next_n_lines)
  return array_by4

# array_by4 = ..., ['ATGCCGCGTGTATGAAGAAGGCCTTCGGGTTGTAAAGTACTTTCAGCGGGGAGGAAGGCGTTGAGGTTAATAACCTCAGCGATTGACGTTACCCGCAGAAGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTCTGTCAAGTCGGATGTGAAATCCCCGGGCTTAACCTGGGAACTGCATTTGAAACTGGCAGGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTGAAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTGGGGAGCAAACAGGATT\n', 'BP04-L-NCAP-16S;0\n', 'BP05-B-NCAP-16S;0\n', 'BP06-G-NCAP-16S;1\n']]

# seq_t.items() = ..., ('ATGCCGCGTGTATGAAGAAGGCCTTCGGGTTGTAAAGTACTTTCAGCGGGGAGGAAGGCGTTGAGGTTAATAACCTCAGCGATTGACGTTACCCGCAGAAGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTCTGTCAAGTCGGATGTGAAATCCCCGGGCTTAACCTGGGAACTGCATTTGAAACTGGCAGGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTGAAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTGGGGAGCAAACAGGATT', 'k_Bacteria;p_Proteobacteria;c_Gammaproteobacteria;o_Enterobacteriales;f_Enterobacteriaceae;GenusNA;s_NA')])

def combine_seq_freq_by_tax(curr_arr, seq_t_d):
  new_dict = {}
  for arr4 in curr_arr:
      for s, t in seq_t_d.items():
        if arr4[0].strip("\n") == s:
          new_dict[t] = arr4
  return new_dict
        
# new_dict = ...,
# 'k_Bacteria;p_Proteobacteria;c_Gammaproteobacteria;o_Enterobacteriales;f_Enterobacteriaceae;GenusNA;s_NA': ['ATGCCGCGTGTATGAAGAAGGCCTTCGGGTTGTAAAGTACTTTCAGCGGGGAGGAAGGCGTTGAGGTTAATAACCTCAGCGATTGACGTTACCCGCAGAAGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTCTGTCAAGTCGGATGTGAAATCCCCGGGCTTAACCTGGGAACTGCATTTGAAACTGGCAGGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTGAAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTGGGGAGCAAACAGGATT\n', 'BP04-L-NCAP-16S;0\n', 'BP05-B-NCAP-16S;0\n', 'BP06-G-NCAP-16S;1\n']}

def combine_seq_freq_by_tax_n_dataset(seq_freq_by_tax_d):
  dict_by_tax_n_dataset = {}
  for taxon, arr in seq_freq_by_tax_d.items():
    new_arr = [a.strip("\n") for a in arr]
    dict_by_tax_n_dataset[taxon] = ",".join(new_arr)

  return dict_by_tax_n_dataset

def write_out(curr_dict, dict_name):
  f_out = open("/Users/ashipunova/work/dada2/stephen_fastq/freq_tax.txt", "a")
  for t, f in curr_dict.items():
      f_out.write("%s,%s,%s\n" % (dict_name, t, f))
  f_out.close()

def write_out_by_dataset(curr_dict, dict_name):
  f_out = open("/Users/ashipunova/work/dada2/stephen_fastq/freq_tax_by_dat.txt", "a")
  f_out.write("%s\n" % (dict_name))
  for t, f in curr_dict.items():
    f_out.write("%s,%s\n" % (f, t))
  f_out.close()
  
def write_out_by_tax(curr_dict):
  head_line = """BP04_L_NCAP_16S,BP04_B_NCAP_16S,BP04_G_NCAP_16S,taxonomy"""

  f_out = open("/Users/ashipunova/work/dada2/stephen_fastq/freq_tax_by_tax.txt", "a")
  f_out.write("%s\n" % (head_line))
  for t, f in curr_dict.items():
    print("%s,%s\n" % (f, t))
    # f_out.write("%s,%s\n" % (f, t))
  f_out.close()  

if __name__ == '__main__':

  sequence_taxa_d = get_sequence_taxa()
  array_by4 = get_dada_freq_res()
  seq_freq_by_tax_d = combine_seq_freq_by_tax(array_by4, sequence_taxa_d)
  combine_seq_freq_by_tax_n_dataset = combine_seq_freq_by_tax_n_dataset(seq_freq_by_tax_d)
  
  BP04_L_NCAP_16S = {t: a[1].split(";")[1].strip("\n") for t, a in seq_freq_by_tax_d.items()}
  BP04_B_NCAP_16S = {t: a[2].split(";")[1].strip("\n") for t, a in seq_freq_by_tax_d.items()}
  BP04_G_NCAP_16S = {t: a[3].split(";")[1].strip("\n") for t, a in seq_freq_by_tax_d.items()}

  # write_out(BP04_L_NCAP_16S, "BP04_L_NCAP_16S")
  # write_out(BP04_B_NCAP_16S, "BP04_B_NCAP_16S")
  # write_out(BP04_G_NCAP_16S, "BP04_G_NCAP_16S")
  
  write_out_by_tax(combine_seq_freq_by_tax_n_dataset)
  write_out_by_tax(combine_seq_freq_by_tax_n_dataset)
  write_out_by_tax(combine_seq_freq_by_tax_n_dataset)  
  
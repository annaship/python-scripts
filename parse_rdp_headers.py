"""
Get more levels from
release11_2_Archaea_unaligned.fa.gz
release11_2_Bacteria_unaligned.fa.gz
and make taxonomy.map

S000871964	Acidimicrobium_ferrooxidans	Acidimicrobium	NA
should be
S000871964	Acidimicrobium_ferrooxidans	Acidimicrobium  Acidimicrobiaceae	NA

"""
import IlluminaUtils.lib.fastalib as fa
import gzip
from itertools import izip
from collections import defaultdict
import time
import util

class Util():

  def print_out_dict(self, dict_name):
    print dict_name
    for k, v in dict_name.items():
        print "%s: %s" % (k, v)

  def write_to_file(self, file_name, text):
      f = open(file_name, 'w')
      f.write(text)
      f.close
  # def combine_insert_term_query(self, all_term_dict_l):
  #     # insert_term_query_1 = """(2, "%s", "%s", "%s", "%s", "%s", "%s")\n""" % (term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
  #
  #     insert_term_query = [create_insert_term_query(goTerm) for goTerm in all_term_dict_l]
  #     max_lines = 7000
  #     for chunk in chunks(insert_term_query, max_lines):
  #         print_out_term_query(", ".join(chunk))
  #     return insert_term_query
  #
  def chunks(self, arr, max_lines):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(arr), max_lines):
          yield arr[i:i + max_lines]
    
  # def print_out_term_query(self, to_print):
  #     first_line = """
  #     INSERT IGNORE INTO term (ontology_id, term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
  #       VALUES
  #     """
  #
  #     i = 0
  #     while os.path.exists("out%s.sql" % i):
  #         i += 1
  #     target = open("out%s.sql" % i, "w")
  #
  #     write_file(first_line, to_print, target) 
                   
class Parse_RDP():
  def __init__(self):
    # self.classification = {}
    self.taxonomy = {}
    self.sequences = {}
    self.organisms = {}
    self.my_utils = Util()
    self.insert_seq_first_line = """INSERT IGNORE INTO spingo_rdp_sequence (locus, spingo_rdp_sequence_comp)
      VALUES 
    """
    self.tax_ranks = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    
      
  def read_file(self, in_fa_gz_file_name):
    print in_fa_gz_file_name
    input = fa.SequenceSource(in_fa_gz_file_name)
    # input1 = fa.ReadFasta(in_fa_gz_file_name)
    # print "len(input1.ids)"
    # print len(input1.ids)    
    
    while input.next():
      locus = self.parse_id(input.id)
      self.sequences[locus] = input.seq
    # print self.classification
    # print self.sequences
    t0 = utils.benchmark_w_return_1("insert_seq")
    self.insert_seq()
    utils.benchmark_w_return_2(t0, "insert_seq")

  def run_insert_seq(self, query_chunk):
      query = self.insert_seq_first_line + query_chunk
      return mysql_utils.execute_no_fetch(query)
        
  def insert_seq(self):  
    query_a = []
    for k, v in self.sequences.items():
      query_a.append("('%s', COMPRESS('%s'))" % (k, v)) 

    if (utils.is_local() == True):
      max_lines = 3
    else:
      max_lines = 7000
      
    for chunk in self.my_utils.chunks(query_a, max_lines):
        query_chunk = ", ".join(chunk)
        
        rowcount, lastrowid = self.run_insert_seq(query_chunk)
        print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
        
  def make_taxonomy_dict(self, lineage):
    print lineage
    taxonomy1 = {}
    taxonomy1_arr = lineage.split(";")
    taxonomy1 = dict(zip(taxonomy1_arr[1::2], taxonomy1_arr[0::2]))
    return taxonomy1
    
  # def make_classification(self, first_part):
  #   return " ".join(first_part.split()[1:])

  def make_organism(self, definition):
    try:
      organism, clone = definition.split(";")
    except ValueError:
      organism = definition
      clone = "empty_clone"
    except:
      raise
    return (organism, clone)
    
  def parse_id(self, header):
    first_part, lineage = header.split("\t")
    locus = first_part.split()[0]
    self.taxonomy[locus] = self.make_taxonomy_dict(lineage)
    # self.classification[locus] = self.make_classification(first_part)
    self.organisms[locus] = self.make_organism(" ".join(first_part.split()[1:]))
    return locus

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "spingo_rdp", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "bpcweb7.bpcservers.private", db = "test", read_default_group = "client")

  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  # print a
  # ((('spingo_rdp',), ('spingo_rdp_sequence',)), ['Tables_in_spingo_rdp'])

  parser = Parse_RDP()
    # todo: ARGS
  if (utils.is_local() == True):
    in_fa_gz_file_name = "/Users/ashipunova/Dropbox/mix/today_ch/spingo_assign/small_current_bact.fa"
  else:
    in_fa_gz_file_name = "/workspace/ashipunova/taxonomy/spingo_assign/current_Bacteria_unaligned.fa"

  t0 = utils.benchmark_w_return_1("read_file")
  parser.read_file(in_fa_gz_file_name)
  utils.benchmark_w_return_2(t0, "read_file")
  
  # print "parser.classification"
  # print parser.classification
  print "parser.taxonomy"
  print parser.taxonomy
  print "parser.organisms"
  print parser.organisms
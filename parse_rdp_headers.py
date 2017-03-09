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
    self.classification = {}
    self.taxonomy = {}
    self.sequences = {}
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
    taxonomy1_arr = []
    taxonomy1_arr = lineage.split(";")
    print "taxonomy1_arr = "
    print taxonomy1_arr
    taxonomy1 = dict(zip(taxonomy1_arr[1::2], taxonomy1_arr[0::2]))
    print "taxonomy1 = "
    print taxonomy1
    return taxonomy1
    
  def parse_id(self, header):
    first_part, lineage = header.split("\t")
    # print first_part.split()
    locus = first_part.split()[0]
    definition = " ".join(first_part.split()[1:])
    self.classification[locus] = definition
    self.taxonomy[locus] = self.make_taxonomy_dict(lineage)
    
    try:
      organism, clone = definition.split(";")
    except ValueError:
      organism = definition
      clone = "empty_clone"
    except:
      raise
    
    return locus
  

class Spingo_Taxonomy():
    def __init__(self):
        # self.arc_filename = "/users/ashipunova/spingo/database/release11_2_Archaea_unaligned.fa.gz"
        # self.bact_filename = "/users/ashipunova/spingo/database/release11_2_Bacteria_unaligned.fa.gz"
        """
        cut -f1 taxonomy.map > mapped_ind.txt
        gzip -dc release11_2_Archaea_unaligned.fa.gz | grep -F -f mapped_ind.txt >mapped_arc_headers.txt
        time gzip -dc release11_2_Bacteria_unaligned.fa.gz | grep -F -f mapped_ind.txt >mapped_bact_headers.txt

        """
        self.tax_map_filename = "/users/ashipunova/spingo/database/taxonomy.map_orig"
        self.arc_filename = "/users/ashipunova/spingo/database/mapped_arc_headers.txt"
        self.bact_filename = "/users/ashipunova/spingo/database/mapped_bact_headers.txt"

        self.tax_map_file_content = []
        self.arc_file_content = []
        self.bact_file_content = []
        self.taxmap_dict = {}
        self.new_map_arr = []
                
        # self.my_dict = defaultdict()

        

    def get_file_content(self, in_filename):
        with open(in_filename, 'rb') as f:
            return f.readlines()

    def get_taxmap_dict(self):
        for line in self.tax_map_file_content:
            self.taxmap_dict[line.split("\t")[0]] = line.split("\t")[1:]


    def pairwise(self, iterable):
        tax_array = iterable[0].strip().split(";")
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        # print "tax_array = %s" % (tax_array)
        a = iter(tax_array)
        return izip(a, a)
        
    def make_taxonomy_by_rank(self, i_dict):
        tax_w_rank_dict = defaultdict()
        for k, v in i_dict.items():
            # print "=" * 10            
            # print k
            tax_w_rank_dict[k] = {}
            for x, y in spingo_tax.pairwise(v[1]):
               # print "%s: %s" % (y, x)
               if not y.startswith("rootrank"):
                   try:
                       tax_w_rank_dict[k][y] = x
                   except KeyError:
                       pass
                   except:
                       raise
        
        return tax_w_rank_dict

    def get_mapped_dict(self, arr):
        m_d = {}
        for line in arr:
            # print "line = %s" % line
            
            # S003805392 Ferrimicrobium acidiphilum; PS130, ['Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ferrimicrobium;genus\n']
            l     = line.split("\t")
            # print "l = %s" % l
            
            first_part = l[0].split(" ")
            ind   = first_part[0].strip(">")
            binom = first_part[1:]
            tax   = l[1:]
            
            # print "ind = %s; binom = %s; tax = %s" % (ind, binom, tax)
            m_d[ind] = (binom, tax)
        return m_d

    def make_current_string(self, key, tax_val, orig_tax_map_val):
        orig_string = "\t".join(orig_tax_map_val).strip()
        try:
            return "%s\t%s\t%s" % (key, orig_string, tax_val["family"])
        except KeyError:
            return "%s\t%s\t%s" % (key, orig_string, "")
        except:
            raise
            
    def combine_two_dicts(self, d1, d2):            
      ds = [d1, d2]
      d = {}
      for k in d1:
          d[k] = tuple(d[k] for d in ds)
      return d

    def make_new_tax_map(self, tax_w_rank_dict):
      self.new_map_arr = []
      comb_dict = self.combine_two_dicts(tax_w_rank_dict, self.taxmap_dict)
      print "CCC comb_dict = "
      for key, v2 in comb_dict.items():
        self.new_map_arr.append(self.make_current_string(key, v2[0], v2[1]))

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
  
  print parser.classification
  print parser.taxonomy
  
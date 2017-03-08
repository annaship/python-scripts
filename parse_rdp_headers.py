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
  def benchmark_w_return_1(self, message):
    print  "\n"
    print "-" * 10
    print message
    return time.time()
    
  def benchmark_w_return_2(self, t0):
    t1 = time.time()
    total = float(t1-t0) / 60
    print 'time: %.2f m' % total
    
  def print_out_dict(self, dict_name):
    print dict_name
    for k, v in dict_name.items():
        print "%s: %s" % (k, v)

  def write_to_file(self, file_name, text):
      f = open(file_name, 'w')
      f.write(text)
      f.close
                   
class Parse_RDP():
  def __init__(self):
    self.classification = {}
    self.sequences = {}
    
      
  def read_file(self, in_fa_gz_file_name):
    input = fa.SequenceSource(in_fa_gz_file_name)

    while input.next():
      locus = self.parse_id(input.id)
      self.sequences[locus] = input.seq
    print self.classification
    print self.sequences
    # self.insert_seq()
    rowcount, lastrowid = self.insert_seq()
    print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
    # query = "show tables"
    # a = mysql_utils.execute_fetch_select(query)
    # print a
    # ((('spingo_rdp',), ('spingo_rdp_sequence',)), ['Tables_in_spingo_rdp'])
    
    
  def insert_seq(self):  
    query_a = []
    query = """INSERT IGNORE INTO spingo_rdp_sequence (locus, spingo_rdp_sequence_comp)    
      VALUES 
    """

    for k, v in self.sequences.items():
      query_a.append("('%s', COMPRESS('%s'))" % (k, v)) 

    query += ", ".join(query_a)
    print query
    return mysql_utils.execute_no_fetch(query)

    
    
      
  def parse_id(self, header):
    first_part, lineage = header.split("\t")
    # print first_part.split()
    # print lineage
    locus = first_part.split()[0]
    definition = " ".join(first_part.split()[1:])
    organism, clone = definition.split(";")
    self.classification[locus] = definition
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
    pass
    # mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps", read_default_group = "client")

  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  # print a
  # ((('spingo_rdp',), ('spingo_rdp_sequence',)), ['Tables_in_spingo_rdp'])

  parser = Parse_RDP()
    # todo: ARGS
  in_fa_gz_file_name = "/Users/ashipunova/Dropbox/mix/today_ch/spingo_assign/small_current_bact.fa"
  parser.read_file(in_fa_gz_file_name)
    
    

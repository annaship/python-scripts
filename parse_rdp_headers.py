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

          
                   
class Parse_RDP():
  def __init__(self):
    self.taxonomy = {}
    self.taxonomy_sorted  = {}
    self.sequences = {}
    self.organisms = {}
    self.my_utils = Util()
    self.tax_ranks = ['domain', 'phylum', 'klass', 'order', 'family', 'genus', 'species']
    self.insert_seq_first_line = """INSERT IGNORE INTO spingo_rdp_sequence (locus, spingo_rdp_sequence_comp)
      VALUES 
    """
    self.insert_tax_first_line = """INSERT IGNORE INTO spingo_rdp_taxonomy (locus, taxonomy)
      VALUES 
    """
    self.insert_spingo_rdp_first_line = """INSERT IGNORE INTO spingo_rdp (locus, organism, clone)
      VALUES 
    """
    if (utils.is_local() == True):
      self.max_lines = 3
    else:
      self.max_lines = 7000
    
    self.insert_one_taxon_first_lines = {}
    self.make_one_taxon_first_lines()
    
  def make_one_taxon_first_lines(self):
    for rank in self.tax_ranks:
      line = "INSERT IGNORE INTO `%s` (`%s`) VALUES" % (rank, rank)
      self.insert_one_taxon_first_lines[rank] = (line)
  
  def clean_taxonomy(self):
    """    taxonomy
        {'S000632094': {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'class': 'Actinobacteria', 'phylum': '"Actinobacteria"', 'suborder': '"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
    """    
    for k, v in self.taxonomy.items():
      v["klass"] = v.pop("class")
      
      taxonomy_7_ranks = {key: v[key] for key in v if (key in self.tax_ranks)}
      # print "VVV"
      # print taxonomy_7_ranks
      
      self.taxonomy_sorted[k] = sorted(taxonomy_7_ranks.items(), key=lambda (k, taxonomy_7_ranks): self.tax_ranks.index(k))

    """
    print tax_dict
    {'domain': 'Eukaryota', 'family': 'Prymnesiaceae', 'order': 'Prymnesiales', 'phylum': 'Haptophyta', 'species': 'palpebrale', 'genus': 'Prymnesium', 'class': 'Haptophyceae'}
    
    """
    """
    print sorted(tax_dict.items(), key=lambda (k,v): self.ranks.index(k))
    [('domain', 'Eukaryota'), ('phylum', 'Haptophyta'), ('class', 'Haptophyceae'), ('order', 'Phaeocystales'), ('family', 'Phaeocystaceae'), ('genus', 'Phaeocystis'), ('species', 'sp._JD-2012')]
    """
          
  def read_file(self, in_fa_gz_file_name):
    print in_fa_gz_file_name
    input = fa.SequenceSource(in_fa_gz_file_name)
    # input1 = fa.ReadFasta(in_fa_gz_file_name)
    # print "len(input1.ids)"
    # print len(input1.ids)    
    
    while input.next():
      t0 = utils.benchmark_w_return_1("parse_id")
      locus = self.parse_id(input.id)
      utils.benchmark_w_return_2(t0, "parse_id")
      
      self.sequences[locus] = input.seq

    t0 = utils.benchmark_w_return_1("clean_taxonomy")
    self.clean_taxonomy()
    utils.benchmark_w_return_2(t0, "clean_taxonomy")
    
    t0 = utils.benchmark_w_return_1("insert_seq")
    self.insert_seq()
    utils.benchmark_w_return_2(t0, "insert_seq")

    t0 = utils.benchmark_w_return_1("insert_tax")
    self.insert_tax()
    utils.benchmark_w_return_2(t0, "insert_tax")

  def run_insert_chunk(self, first_line, query_chunk):
      query = first_line + query_chunk
      return mysql_utils.execute_no_fetch(query)
        
  def insert_seq(self):  
    query_a = []
    for k, v in self.sequences.items():
      query_a.append("('%s', COMPRESS('%s'))" % (k, v)) 

    for chunk in utils.chunks(query_a, self.max_lines):
        query_chunk = ", ".join(chunk)
        
        rowcount, lastrowid = self.run_insert_chunk(self.insert_seq_first_line, query_chunk)
        print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
        
  def insert_sping_rdp_info(self):
    self.insert_spingo_rdp_first_line
  
  # todo: insert taxonomy all? or separate?
  def insert_tax(self):  
    query_a = []
    for locus, tax_dict in self.taxonomy_sorted.items():
        # out_line = self.insert_tax_first_line
        # print tax_dict
        #[('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]
        taxon_string = ";".join([x[1].strip('"') for x in tax_dict])
        query_a.append("('%s', '%s')" % (locus, taxon_string))

    for chunk in utils.chunks(query_a, self.max_lines):
        query_chunk = ", ".join(chunk)

        rowcount, lastrowid = self.run_insert_chunk(self.insert_tax_first_line, query_chunk)
        print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)

  def make_taxonomy_dict(self, lineage):
    # print lineage
    taxonomy1 = {}
    taxonomy1_arr = lineage.split(";")
    taxonomy1 = dict(zip(taxonomy1_arr[1::2], taxonomy1_arr[0::2]))
    return taxonomy1
    
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
    self.taxonomy[locus]  = self.make_taxonomy_dict(lineage)
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
  
  # print "parser.taxonomy"
  # print parser.taxonomy
  # print "parser.insert_one_taxon_first_lines"
  # print parser.insert_one_taxon_first_lines
  #
  print "parser.taxonomy_sorted"
  print parser.taxonomy_sorted
  
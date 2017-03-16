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

# class Util():
#
#   def write_to_file(self, file_name, text):
#       f = open(file_name, 'w')
#       f.write(text)
#       f.close


class Parse_RDP():
  def __init__(self):
    self.taxonomy = {}
    self.taxonomy_sorted  = {}
    self.taxonomy_unsorted_dict = {}
    self.taxa_by_rank = {}
    self.sequences = {}
    self.organisms = {}
    self.tax_ranks = ['domain', 'phylum', 'klass', 'order', 'family', 'genus', 'species']

  def clean_taxonomy(self):
    """    taxonomy
        {'S000632094': {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'class': 'Actinobacteria', 'phylum': '"Actinobacteria"', 'suborder': '"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
    """
    for locus, v in self.taxonomy.items():
      try:
        v["klass"] = v.pop("class")
      except KeyError:
        pass
        # todo: add empty_... to all missing rank lavels?
      except:
        raise

      taxonomy_7_ranks = {key.strip(): v[key].strip('"').strip() for key in v if (key.strip() in self.tax_ranks)}
#       print "VVV"
#       print taxonomy_7_ranks
# {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'phylum': '"Actinobacteria"', 'klass': 'Actinobacteria', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
      self.taxonomy_unsorted_dict[locus] = taxonomy_7_ranks
      self.taxonomy_sorted[locus] = sorted(taxonomy_7_ranks.items(), key=lambda (locus, taxonomy_7_ranks): self.tax_ranks.index(locus))

    """
    print tax_dict
    {'domain': 'Eukaryota', 'family': 'Prymnesiaceae', 'order': 'Prymnesiales', 'phylum': 'Haptophyta', 'species': 'palpebrale', 'genus': 'Prymnesium', 'class': 'Haptophyceae'}

    """
    """
    print sorted(tax_dict.items(), key=lambda (k,v): self.ranks.index(k))
    [('domain', 'Eukaryota'), ('phylum', 'Haptophyta'), ('class', 'Haptophyceae'), ('order', 'Phaeocystales'), ('family', 'Phaeocystaceae'), ('genus', 'Phaeocystis'), ('species', 'sp._JD-2012')]
    """

    self.separate_taxa_by_rank()

  def separate_taxa_by_rank(self):
    # print "self.taxonomy_unsorted_dict:"
    # for locus, v in self.taxonomy_unsorted_dict.items():
    #     for rank_name, taxon in v.items():
    #       print "rank_name = %s, taxon = %s" % (rank_name, taxon)
    # print "locus = %s, v = %s" % (locus, v)
    # try:
    #      taxa_by_rank[rank_name] = [dd[rank_name] for dd in self.taxonomy_unsorted_dict.values()]
    #      taxa_by_rank[rank_name] = set([dd[rank_name] for dd in self.taxonomy_unsorted_dict.values()])
    #    except KeyError:
    #      pass
    # [dd['domain'] for dd in d]
    # taxa_list_w_empty_ranks_dict = defaultdict(list)
    #
    # # taxa_list_w_empty_ranks_dict = {taxonomy: tax_list + [""] * (len(self.tax_ranks) - len(tax_list)) for locus, tax_list in self.taxonomy_unsorted_dict.items()}
    # for locus, tax_list in self.taxonomy_unsorted_dict.items():
    #   print "tax_list = "
    #   print tax_list
    #   print "len(self.tax_ranks) = "
    #   print len(self.tax_ranks)
    #   print "len(tax_list) = "
    #   print len(tax_list)
    #
    inner_taxa_by_rank = {}
    for d in self.taxonomy_unsorted_dict.values():
      try:
        inner_taxa_by_rank['family'].append(d['family'])
      except KeyError:
        inner_taxa_by_rank['family'] = []
        inner_taxa_by_rank['family'].append('empty_family')
      except:
        raise
        
    print "DDD"
    print "inner_taxa_by_rank"
    print inner_taxa_by_rank
    
    # print taxa_list_w_empty_ranks_dict
    # inner_taxa_by_rank = defaultdict(list)
    # for locus, dd in self.taxonomy_unsorted_dict.items():
    #   print "dd"
    #   print dd
    #   """
    #   {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'phylum': 'Actinobacteria', 'klass': 'Actinobacteria', 'genus': 'Ilumatobacter', 'order': 'Acidimicrobiales'}
    #   {'domain': 'Bacteria'}
    #   ...
    #   """
    #   for k, v in dd.items():
    #     inner_taxa_by_rank[k].append(v)
    #
    # # for rank_name in self.tax_ranks:
    # #   print "rank_name = %s" % rank_name
    # #   try:
    # #     for dd in self.taxonomy_unsorted_dict.values():
    # #       print "dd[rank_name] = %s" % (dd[rank_name])
    # #       print "UUU [dd[rank_name] for dd in self.taxonomy_unsorted_dict.values()]"
    # #       print [dd[rank_name] for dd in self.taxonomy_unsorted_dict.values()]
    # #     # self.taxa_by_rank[rank_name].append([dd[rank_name] for dd in self.taxonomy_unsorted_dict.values()])
    # #   except KeyError:
    # #     pass
    # #   except:
    # #     raise

  def read_file_and_collect_info(self, in_fa_gz_file_name):
    print in_fa_gz_file_name
    input = fa.SequenceSource(in_fa_gz_file_name)

    while input.next():
      t0 = utils.benchmark_w_return_1("parse_id")
      locus = self.parse_id(input.id)
      utils.benchmark_w_return_2(t0, "parse_id")

      self.sequences[locus.strip()] = input.seq.strip()

  def make_taxonomy_dict(self, lineage):
    taxonomy1 = {}
    taxonomy1_arr = lineage.split(";")
    taxonomy1 = dict(zip(taxonomy1_arr[1::2], taxonomy1_arr[0::2]))
    """
      print "taxonomy1"
      print taxonomy1
      {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'class': 'Actinobacteria', 'phylum': '"Actinobacteria"', 'suborder': '"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
    """
    return taxonomy1

  def make_organism(self, definition):
    try:
      organism, clone = definition.split(";")
    except ValueError:
      organism = definition
      clone = "empty_clone"
    except:
      raise
    return (organism.strip(), clone.strip())

  def parse_id(self, header):
    first_part, lineage = header.split("\t")
    locus = first_part.split()[0].strip()
    self.taxonomy[locus]  = self.make_taxonomy_dict(lineage)
    self.organisms[locus] = self.make_organism(" ".join(first_part.split()[1:]))
    return locus

class DB_operations(Parse_RDP):
  def __init__(self, parse_rdp):
    self.sequences = parse_rdp.sequences
    self.taxonomy_sorted = parse_rdp.taxonomy_sorted
    self.organisms = parse_rdp.organisms
    self.taxa_by_rank = parse_rdp.taxa_by_rank

    self.tax_ranks = parse_rdp.tax_ranks
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

  def run_insert_chunk(self, first_line, query_chunk):
      query = first_line + query_chunk
      return mysql_utils.execute_no_fetch(query)

  def run_query_by_chunks(self, query_array, first_line):
    for chunk in utils.chunks(query_array, self.max_lines):
        query_chunk = ", ".join(chunk)

        rowcount, lastrowid = self.run_insert_chunk(first_line, query_chunk)
        print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)

  # todo: insert taxonomy all? or separate?
  def insert_tax(self):
    query_a = []
    for locus, tax_dict in self.taxonomy_sorted.items():
        # out_line = self.insert_tax_first_line
        # print tax_dict
        #[('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]
        taxon_string = ";".join([x[1] for x in tax_dict])
        query_a.append("('%s', '%s')" % (locus, taxon_string))

    self.run_query_by_chunks(query_a, self.insert_tax_first_line)

  def insert_separate_taxa(self):
    print "TTT"
    for k, v in self.taxa_by_rank.items():
      print k, set(v)
      """
      domain set(['Bacteria'])
      family set(['Acidimicrobiaceae'])
      phylum set(['Actinobacteria'])
      klass set(['Actinobacteria'])
      genus set(['Acidimicrobium'])
      order set(['Acidimicrobiales'])
      """

  #   query_a = []
  #   for locus, tax_dict in self.taxonomy_sorted.items():
  #       # out_line = self.insert_tax_first_line
  #       # print tax_dict
  #       #[('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]
  #       taxon_string = ";".join([x[1].strip('"').strip() for x in tax_dict])
  #       query_a.append("('%s', '%s')" % (locus, taxon_string))
  #
  #   self.run_query_by_chunks(query_a, self.insert_tax_first_line)


  def insert_seq(self):
    query_a = []
    for k, v in self.sequences.items():
      query_a.append("('%s', COMPRESS('%s'))" % (k, v))

    self.run_query_by_chunks(query_a, self.insert_seq_first_line)

  def insert_sping_rdp_info(self):
    print self.insert_spingo_rdp_first_line
    print "self.organisms"
    print self.organisms
    """
    INSERT IGNORE INTO spingo_rdp (locus, organism, clone)

    {'S000632094': ('uncultured Acidimicrobium sp.', ' SK269'), 'S000632122': ('uncultured Acidimicrobium sp.', ' SK297'), 'S000632121': ('uncultured Acidimicrobium sp.', ' SK296'), 'S000494604': ('uncultured bacterium', ' YRM60L1H09060904'), 'S000494589': ('uncultured bacterium', ' YRM60L1D06060904'), 'S000367885': ('Acidimicrobium sp. Y0018', 'empty_clone'), 'S000541758': ('bacterium TH3', 'empty_clone')}
    """
    query_a = []
    for locus, v in self.organisms.items():
      # query_a.append("('%s', '%s', '%s')" % (locus.strip(), v[0].strip(), v[1].strip()))
      query_a.append("('%s', '%s', '%s')" % (locus, v[0], v[1]))

    print "query_a"
    print query_a
    self.run_query_by_chunks(query_a, self.insert_spingo_rdp_first_line)



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

  db_operations = DB_operations(parser)


  """
  read file
    parse it - get
      id
      seq
      taxonomy
        separate binomial
        all taxa ranks
  upload separate values to db
    get ids
  upload combined ids
  read NCBI data file
    add accession_ids
  """
  t0 = utils.benchmark_w_return_1("read_file_and_collect_info")
  parser.read_file_and_collect_info(in_fa_gz_file_name)
  utils.benchmark_w_return_2(t0, "read_file_and_collect_info")

  t0 = utils.benchmark_w_return_1("clean_taxonomy")
  parser.clean_taxonomy()
  utils.benchmark_w_return_2(t0, "clean_taxonomy")

  t0 = utils.benchmark_w_return_1("insert_seq")
  db_operations.insert_seq()
  utils.benchmark_w_return_2(t0, "insert_seq")

  t0 = utils.benchmark_w_return_1("insert_tax")
  db_operations.insert_tax()
  utils.benchmark_w_return_2(t0, "insert_tax")

  t0 = utils.benchmark_w_return_1("insert_sping_rdp_info")
  db_operations.insert_sping_rdp_info()
  utils.benchmark_w_return_2(t0, "insert_sping_rdp_info")

  t0 = utils.benchmark_w_return_1("insert_separate_taxa")
  db_operations.insert_separate_taxa()
  utils.benchmark_w_return_2(t0, "insert_separate_taxa")



  """
  TODO:
  insert each rank separately
  insert combined taxa ids
  mysql_utils.get_all_name_id(table_name, id_name = "", field_name = "", where_part = "")


  """

  # print "parser.taxonomy"
  # print parser.taxonomy
  # print "parser.insert_one_taxon_first_lines"
  # print parser.insert_one_taxon_first_lines
  #
  # print "parser.taxonomy_sorted"
  # print parser.taxonomy_sorted

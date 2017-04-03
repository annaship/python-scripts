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

class Parse_RDP():
  def __init__(self):
    self.taxonomy = {}
    self.taxonomy_sorted  = {}
    self.taxonomy_unsorted_dict = {}
    self.taxa_by_rank = {}
    self.sequences = {}
    self.organisms = {}
    self.tax_ranks = ['domain', 'phylum', 'klass', 'order', 'family', 'genus', 'species']

  def get_only_valid_rank_taxa(self, taxa_string_dict):
    # print taxa_string_dict
    # {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'class': 'Actinobacteria', 'phylum': '"Actinobacteria"', 'suborder': '"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
    
    try:
      taxa_string_dict["klass"] = taxa_string_dict.pop("class")
    except KeyError:
      pass
      # done: add empty_... to all missing rank lavels?
    except:
      raise
    return taxa_string_dict
    
  def add_all_valid_rank_taxa(self, taxa_string_dict):
    """    print taxa_string_dict
    {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'phylum': '"Actinobacteria"', 'klass': 'Actinobacteria', 'suborder':'"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}"""
    missing_ranks = list(set(self.tax_ranks) - set(taxa_string_dict.keys()))
    for rank in missing_ranks:
      taxa_string_dict[rank] = "empty_" + rank
    return taxa_string_dict
    
  def clean_taxonomy(self):
    """    taxonomy
        {'S000632094': {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'rootrank': 'Lineage=Root', 'subclass': 'Acidimicrobidae', 'class': 'Actinobacteria', 'phylum': '"Actinobacteria"', 'suborder': '"Acidimicrobineae"', 'genus': 'Acidimicrobium', 'order': 'Acidimicrobiales'}
    """
    for locus, taxa_string_dict in self.taxonomy.items():
      taxa_string_dict = self.get_only_valid_rank_taxa(taxa_string_dict)
      taxa_string_dict = self.add_all_valid_rank_taxa(taxa_string_dict)
      
      taxonomy_7_ranks = {key.strip(): taxa_string_dict[key].strip('"').strip() for key in taxa_string_dict if (key.strip() in self.tax_ranks)}
      """      print "VVV"
            print taxonomy_7_ranks
            {'domain': 'Bacteria', 'family': 'Acidimicrobiaceae', 'order': 'Acidimicrobiales', 'phylum': 'Actinobacteria', 'klass': 'Actinobacteria', 'genus': 'Acidimicrobium', 'species': 'empty_species'}
      """      
      self.taxonomy_unsorted_dict[locus] = taxonomy_7_ranks
      self.taxonomy_sorted[locus] = sorted(taxonomy_7_ranks.items(), key=lambda (locus, taxonomy_7_ranks): self.tax_ranks.index(locus))

    """
    print tax_dict
    {'domain': 'Eukaryota', 'family': 'Prymnesiaceae', 'order': 'Prymnesiales', 'phylum': 'Haptophyta', 'species': 'palpebrale', 'genus': 'Prymnesium', 'class': 'Haptophyceae'}

    """
    self.separate_taxa_by_rank()
    
  def separate_taxa_by_rank(self):
    self.taxa_by_rank = utils.initialize_dict_of_lists(self.tax_ranks)      
    
    for taxa_dict in self.taxonomy_unsorted_dict.values():
      for rank in self.tax_ranks:
        self.taxa_by_rank[rank].append(taxa_dict[rank])

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
    self.id_taxon_dict_by_rank = {}

  def run_insert_chunk(self, first_line, query_chunk):
      query = first_line + query_chunk
      return mysql_utils.execute_no_fetch(query)

  def run_query_by_chunks(self, query_array, first_line):
    for chunk in utils.chunks(query_array, self.max_lines):
        query_chunk = ", ".join(chunk)

        rowcount, lastrowid = self.run_insert_chunk(first_line, query_chunk)
        print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)

  # done: insert taxonomy all? or separate?
  def insert_tax(self):
    query_a = []
    for locus, tax_arr in self.taxonomy_sorted.items():
        """print tax_arr
        [('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]"""
        taxon_string = ";".join([x[1] for x in tax_arr])
        query_a.append("('%s', '%s')" % (locus, taxon_string))

    self.run_query_by_chunks(query_a, self.insert_tax_first_line)

  def make_one_taxon_first_lines(self):
    for rank in self.tax_ranks:
      line = "INSERT IGNORE INTO `%s` (`%s`) VALUES" % (rank, rank)
      self.insert_one_taxon_first_lines[rank] = (line)

  def insert_separate_taxa(self):
    for rank, taxa_list in self.taxa_by_rank.items():
      query_a = ["('%s')" % taxon for taxon in set(taxa_list)]
      self.run_query_by_chunks(query_a, self.insert_one_taxon_first_lines[rank])
      
      """
        domain set(['Bacteria'])
        family set(['empty_family', 'Acidimicrobiaceae'])
        species set(['empty_species'])
        phylum set(['empty_phylum', 'Actinobacteria'])
        klass set(['empty_klass', 'Actinobacteria'])
        genus set(['empty_genus', 'Acidimicrobium', 'Ilumatobacter'])
        order set(['Acidimicrobiales', 'empty_order'])
      """

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

  # def truncate_all(self):
  #   sql = "show tables"
  #   res, field_names = mysql_utils.execute_fetch_select(sql)
  #   # print "RRR"
  #   for table_name in res:
  #     # print table_name[0]
  #     truncate_query = "TRUNCATE TABLE `%s`;" % (table_name[0])
  #     mysql_utils.execute_no_fetch(truncate_query)
      

    # print mysql_utils.execute_no_fetch(query)

  def get_all_taxa_ids(self):
    """
    print "SSS self.taxonomy_sorted = "
    print self.taxonomy_sorted
    {'S000632094': [('domain', 'Bacteria'), ('phylum', 'Actinobacteria'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium'), ('species', 'empty_species')], 'S000632122': [(
    """
    for locus, taxa_list in self.taxonomy_sorted.items():
      for rank_taxon_tpl in taxa_list:
        print rank_taxon_tpl
        rank, taxon = rank_taxon_tpl
      # mysql_utils.get_id(field_name, table_name, where_part, rows_affected = [0,0]):
  
  
  """
  TODO: benchmark with all entries and benchmark list comprehenson
      all_results = [mysql_utils.execute_fetch_select("select * from `%s` where `%s` = '%s'" % (rank, rank, taxon)) for taxon in set(taxa_list)]
  """
  def get_all_taxa_ids_in_bulk(self):
    all_results = []
    for rank, taxa_list in self.taxa_by_rank.items():
      for taxon in set(taxa_list):
        query = "select * from `%s` where `%s` = '%s'" % (rank, rank, taxon)
        all_results.append(mysql_utils.execute_fetch_select(query))
    return all_results

  def make_dict_taxa_id(self):
    res = self.get_all_taxa_ids_in_bulk()
    """print res
    [(((1L, 'Bacteria'),), ['domain_id', 'domain']), (((1L, 'empty_family'),), ['family_id', 'family']), (((2L, 'Acidimicrobiaceae'),), ['family_id', 'family']), (((1L, 'empty_species'),), ['species_id', 'species']), (((1L, 'empty_phylum'),), ['phylum_id', 'phylum']), (((2L, 'Actinobacteria'),), ['phylum_id', 'phylum']), (((1L, 'empty_klass'),), ['klass_id', 'klass']), (((2L, 'Actinobacteria'),), ['klass_id', 'klass']), (((1L, 'empty_genus'),), ['genus_id', 'genus']), (((2L, 'Acidimicrobium'),), ['genus_id', 'genus']), (((3L, 'Ilumatobacter'),), ['genus_id', 'genus']), (((1L, 'Acidimicrobiales'),), ['order_id', 'order']), (((2L, 'empty_order'),), ['order_id', 'order'])]
    
    """
    self.id_taxon_dict_by_rank = utils.initialize_dict_of_lists(self.tax_ranks)
    
    for tpl_res in res:
      self.id_taxon_dict_by_rank[tpl_res[1][1]].append(tpl_res[0][0])

  def insert_combined_taxa_ids(self):
    combined_taxa_ids_first_line = """INSERT INTO spingo_rdp_taxonomy (domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, updated_at)
    VALUES"""
    
    print "CCC"
    for locus, tax_arr in self.taxonomy_sorted.items():
      # print "locus = %s, tax_arr = %s" % (locus, tax_arr)
      #   tax_arr: [('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]
      for rank_taxa_list in tax_arr:
        print "DDDDD"
        print "rank_taxa_list"
        print rank_taxa_list
        id_taxa_list = self.id_taxon_dict_by_rank[rank_taxa_list[0]]
        
        print "self.id_taxon_dict_by_rank[rank_taxa_list[0]] = id_taxa_list"
        print id_taxa_list
        # print [i for i, v in enumerate(tax_arr) if v[1] == rank_taxa_list[1]]
        # print [v[0] for v in rank_taxa_list if v[1] == rank_taxa_list[1]]
        for v in id_taxa_list:
          print "rank_taxa_list[1] = %s, v = %s" % (rank_taxa_list[1], v)
          # if rank_taxa_list[1] == v:
          #   print id_taxa_list[]
          """
          self.id_taxon_dict_by_rank[rank_taxa_list[0]] = id_taxa_list
          [(1L, 'empty_genus'), (2L, 'Acidimicrobium'), (3L, 'Ilumatobacter')]
          rank_taxa_list[1] = Acidimicrobium, v = (1L, 'empty_genus')
          rank_taxa_list[1] = Acidimicrobium, v = (2L, 'Acidimicrobium')
          rank_taxa_list[1] = Acidimicrobium, v = (3L, 'Ilumatobacter')
          DDDDD
          rank_taxa_list
          ('species', 'empty_species')
          self.id_taxon_dict_by_rank[rank_taxa_list[0]] = id_taxa_list
          [(1L, 'empty_species')]
          rank_taxa_list[1] = empty_species, v = (1L, 'empty_species')
          insert_combined_taxa_ids time: 0.00 m
          
          """
      
      # for rank, id_taxon_list in self.id_taxon_dict_by_rank.items():
      #   print "rank = %s, id_taxon_list = " % (rank)
      #   print id_taxon_list 
        # {'domain': [(1L, 'Bacteria')], 'family': [(1L, 'empty_family'), (2L, 'Acidimicrobiaceae')], 'species': [(1L, 'empty_species')], 'phylum': [(1L, 'empty_phylum'), (2L, 'Actinobacteria')], 'klass': [(1L, 'empty_klass'), (2L, 'Actinobacteria')], 'genus': [(1L, 'empty_genus'), (2L, 'Acidimicrobium'), (3L, 'Ilumatobacter')], 'order': [(1L, 'Acidimicrobiales'), (2L, 'empty_order')]}
        
    # (), 
    # see insert_tax(self)
    # ...
    #   for locus, tax_arr in self.taxonomy_sorted.items():
    #   tax_arr: [('domain', 'Bacteria'), ('phylum', '"Actinobacteria"'), ('klass', 'Actinobacteria'), ('order', 'Acidimicrobiales'), ('family', 'Acidimicrobiaceae'), ('genus', 'Acidimicrobium')]
    

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "spingo_rdp", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  # print a
  
  query_custom_tables = """
  SELECT table_name FROM information_schema.tables
  WHERE TABLE_NAME LIKE "custom_metadata_%"
  AND table_schema = "vamps2"
  """
  all_custom_tables = mysql_utils.execute_fetch_select(query_custom_tables)
  # print all_custom_tables
  
  # for t in all_custom_tables[0]:
  #   print t[0]

  
  query_project_ids = """select project_id, project from project where project like "DCO%" """
  all_dco_project_ids = mysql_utils.execute_fetch_select(query_project_ids)
  
  # print "all_dco_project_ids"
  # print all_dco_project_ids
  dco_cutom_tables = ['custom_metadata_' + str(int(x[0])) for x in all_dco_project_ids[0]]
  
  all_project_ids = [str(int(x[0])) for x in all_dco_project_ids[0]]
  # print dco_cutom_tables
  # print len(dco_cutom_tables)
  # 64
  
  for table_name in dco_cutom_tables:
    get_metadata_query = """ select 
    
    """
  
  dco_custom_fields_query = """select distinct project_id, field_name, field_units, example from custom_metadata_fields where project_id in (%s)""" % (", ".join(all_project_ids))
  # print dco_custom_fields_query
  dco_custom_fields = mysql_utils.execute_fetch_select(dco_custom_fields_query)
  # print dco_custom_fields
  """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
  
  my_dict = {}
  # defaultdict(dict)
  # my_dict = utils.initialize_dict_of_lists(all_project_ids)
  
  all_field_names = []
  all_field_name__descr = []
  for dco_custom_field_info in dco_custom_fields[0]:
    # print "dco_custom_field_info"
    # print dco_custom_field_info
    # (860L, 'resistivity', 'ohm-meters', 'n.d.')
    # (860L, 'trace element geochemistry', '', 'yes')
    project_id = dco_custom_field_info[0]
    field_name = dco_custom_field_info[1]
    # my_dict[project_id]field_name].append
    query = """select `%s` from custom_metadata_%s""" % (field_name, str(project_id))
    # print query
    custom_metadata = mysql_utils.execute_fetch_select(query)
    custom_metadata_list = [y[0] for y in set([x for x in custom_metadata[0]])]
    # print custom_metadata_list
    # print "field_name = %s" % field_name
    # print dco_custom_field_info[3] == custom_metadata_list[0]
    # 
    # if not (dco_custom_field_info[3] == custom_metadata_list[0]):
    #   print "dco_custom_field_info[3] = %s, custom_metadata_list[0] = %s" % (dco_custom_field_info[3], custom_metadata_list[0])
    
    str_project_id = str(project_id)
    field_name__descr = field_name + "__" + dco_custom_field_info[2]
    all_field_names.append(field_name)
    all_field_name__descr.append(field_name__descr)
    if str_project_id not in my_dict:
        my_dict[str_project_id] = {}

    if field_name not in my_dict[str_project_id]:
        my_dict[str_project_id][field_name__descr] = []

    my_dict[str_project_id][field_name__descr].append(custom_metadata_list)
  
    for x in custom_metadata_list:
      if dco_custom_field_info[3] != x:
        # print "dco_custom_field_info[3] = %s, x = %s" % (dco_custom_field_info[3], x)
        pass
    
  # print my_dict
  # lat_lon': [['', '28.596 S, 173.381 W', '28.596 S, 173.280 W']], 'samp_store_temp': [['-80']]}}
  
  print "555"
  for str_project_id, d1 in my_dict.items():
    """
    all_dco_project_ids
    (((300L, 'DCO_BKR_Av4v5'), (110L, 'DCO_BKR_Bv4v5'), (301L, 'DCO_BOM_Av6'), (101L, 'DCO_BOM_Bv6'), (302L, 'DCO_BPC_Bv6'), (103L, 'DCO_BRA_Av6'), (303L, 'DCO_BRA_Bv6'),
    """
    
    project_name = [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    for field_name__descr, custom_metadata_list in d1.items():
      for custom_metadatum in custom_metadata_list:
        pass
        # print project_name[0], field_name__descr, custom_metadatum
        
        "/workspace/ashipunova/metadata/dco$ python dco_metadata_exapmles_per_dataset.py >all_dco_metadata.csv"
        
        # ===
  my_dict2 = {}
  for str_project_id, d1 in my_dict.items():  
    project_name = [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    for field_name__descr, custom_metadata_list in d1.items():
      for custom_metadatum in custom_metadata_list:
        if field_name__descr not in my_dict2:
            my_dict2[field_name__descr] = []
        
        my_dict2[field_name__descr].append(custom_metadatum)
  
  for k, v in my_dict2.items():
    print k, set([item for sublist in v for item in sublist])
    
  print len(set(all_field_name__descr))
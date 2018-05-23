# from collections import defaultdict
# import time
import util
import mysqlclient
import csv
import sys
from collections import defaultdict

class Query():
  """
  create the table on vampsdev
  add foreign keys
  add code to rebuild_vamps_files.py to use look_up_tax
  test rebuild_vamps_files.py on vampsdev
  remove foreign keys
  move to vamps prod
  add foreign keys
  test rebuild_vamps_files.py on vampsdb
  """
  def __init__(self):
    self.create_table_look_up_tax_query = """CREATE TABLE IF NOT EXISTS look_up_tax
      AS
      SELECT seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id, dataset, domain, phylum, klass, `order`, family, genus, species, strain, sequence_comp, run, run_key,illumina_index,lane, primer_suite 
      FROM sequence_pdr_info 
      JOIN silva_taxonomy_info_per_seq USING(sequence_id) 
      JOIN silva_taxonomy USING(silva_taxonomy_id) 
      join dataset using(dataset_id)
      join domain using(domain_id)
      join phylum using(phylum_id)
      join klass using(klass_id)
      join `order` using(order_id)
      join family using(family_id)
      join genus using(genus_id)
      join species using(species_id)
      join strain using(strain_id)
      join sequence using(sequence_id)
      join run_info_ill using(run_info_ill_id, dataset_id)
      join run using(run_id)
      join run_key using(run_key_id)
      join illumina_index using(illumina_index_id)
      join primer_suite using(primer_suite_id)
      limit 1"""
  
  def alter_table_look_up_tax(self):
    q1 = """ALTER TABLE look_up_tax
        ADD COLUMN look_up_tax_id int(11) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;"""
    # q2 = """ALTER TABLE look_up_tax
    #   ADD UNIQUE KEY seq_dat (sequence_id, run_info_ill_id),
    #   ADD KEY all_fields (dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id);"""
    try:
      res = mysql_utils.execute_no_fetch_w_info(q1)
      print(q1, res)
    except MySQLdb.OperationalError as e:
      print(e)
      # try:
      #   res = mysql_utils.execute_no_fetch_w_info(q2)
      #   print(q2, res)
      # except MySQLdb.OperationalError as e:
      #   print(e)

  def get_max_id(self):
      return mysql_utils.execute_fetch_select("SELECT max(sequence_pdr_info_id) FROM sequence_pdr_info")

  def update_table_look_up_tax(self):
      chunk_size = 100000
      q_update_table_look_up_tax = """INSERT INTO look_up_tax (seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id, dataset, domain, phylum, klass, `order`, family, genus, species, strain, sequence_comp, run, run_key,illumina_index,lane, primer_suite)
      SELECT seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id, dataset, domain, phylum, klass, `order`, family, genus, species, strain, sequence_comp, run, run_key,illumina_index,lane, primer_suite 
      FROM sequence_pdr_info 
      JOIN silva_taxonomy_info_per_seq USING(sequence_id) 
      JOIN silva_taxonomy USING(silva_taxonomy_id) 
      join dataset using(dataset_id)
      join domain using(domain_id)
      join phylum using(phylum_id)
      join klass using(klass_id)
      join `order` using(order_id)
      join family using(family_id)
      join genus using(genus_id)
      join species using(species_id)
      join strain using(strain_id)
      join sequence using(sequence_id)
      join run_info_ill using(run_info_ill_id, dataset_id)
      join run using(run_id)
      join run_key using(run_key_id)
      join illumina_index using(illumina_index_id)
      join primer_suite using(primer_suite_id)
      LIMIT %s, %s
      ON DUPLICATE KEY UPDATE
        seq_count = VALUES(seq_count), 
        dataset = VALUES(dataset), 
        domain = VALUES(domain), 
        phylum = VALUES(phylum), 
        klass = VALUES(klass), 
        `order` = VALUES(`order`), 
        family = VALUES(family), 
        genus = VALUES(genus), 
        species = VALUES(species), 
        strain = VALUES(strain), 
        sequence_comp = VALUES(sequence_comp), 
        run_info_ill_id = VALUES(run_info_ill_id)
        """

      print("IN update_table_look_up_tax")
      max_id = self.get_max_id()[0][0][0]
      print("max_id = %s" % max_id)
      # for counter in range(1, int(max_id), chunk_size):        
      for counter in range(21436000, int(max_id), chunk_size):                  
          print("counter = %s" % counter)
          mysql_utils.execute_no_fetch_w_info(q_update_table_look_up_tax % (counter, chunk_size))

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps2", read_default_group = "client")

  q = Query()
  # res = mysql_utils.execute_no_fetch_w_info(q.create_table_look_up_tax_query)
  # print(q.create_table_look_up_tax_query, res)

  # q.alter_table_look_up_tax()
  # print("update_table_look_up_tax")
  q.update_table_look_up_tax()
  
  """TODO: args - create, update"""

  #
  # t = utils.benchmark_w_return_1("get_metadata_info")
  # metadata.get_metadata_info()
  # utils.benchmark_w_return_2(t, "get_metadata_info")
  #

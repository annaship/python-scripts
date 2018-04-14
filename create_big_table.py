# from collections import defaultdict
# import time
import util
import MySQLdb
import csv
import sys
from collections import defaultdict

class Query():
  """
  Get data from
  project
  dataset
  custom_fields
  custom and required metadata
  """
  def __init__(self):
    self.create_table_look_up_tax_query = """CREATE TABLE IF NOT EXISTS look_up_tax
      AS
      SELECT seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id FROM sequence_pdr_info JOIN silva_taxonomy_info_per_seq USING(sequence_id) JOIN silva_taxonomy USING(silva_taxonomy_id) limit 1"""
  
  def alter_table_look_up_tax(self):
    q1 = """ALTER TABLE look_up_tax
        ADD COLUMN look_up_tax_id int(11) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;"""
    q2 = """ALTER TABLE look_up_tax        
      ADD UNIQUE KEY seq_dat (sequence_id, run_info_ill_id),
      ADD KEY all_fields (dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id);"""
    try:
      res = mysql_utils.execute_no_fetch_w_info(q1)
      print(q1, res)
    except MySQLdb.OperationalError as e:
      print(e)
      try:
        res = mysql_utils.execute_no_fetch_w_info(q2)
        print(q2, res)
      except MySQLdb.OperationalError as e:
        print(e)

  def get_max_id(self):
      return mysql_utils.execute_fetch_select("SELECT max(look_up_tax_id) FROM look_up_tax")

  def update_table_look_up_tax(self):
      chunk_size = 30
      q_update_table_look_up_tax = """INSERT INTO look_up_tax (seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id)
      SELECT seq_count, dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id, run_info_ill_id FROM sequence_pdr_info JOIN silva_taxonomy_info_per_seq USING(sequence_id) JOIN silva_taxonomy USING(silva_taxonomy_id)
      LIMIT %s, %s
      ON DUPLICATE KEY UPDATE
        seq_count = VALUES(seq_count), 
        dataset_id = VALUES(dataset_id), 
        domain_id = VALUES(domain_id), 
        phylum_id = VALUES(phylum_id), 
        klass_id = VALUES(klass_id), 
        order_id = VALUES(order_id), 
        family_id = VALUES(family_id), 
        genus_id = VALUES(genus_id), 
        species_id = VALUES(species_id), 
        strain_id = VALUES(strain_id), 
        sequence_id = VALUES(sequence_id), 
        run_info_ill_id = VALUES(run_info_ill_id)
        """

      for counter in range(1, int(self.get_max_id()[0][0][0]), chunk_size):
          mysql_utils.execute_no_fetch_w_info(q_update_table_look_up_tax % (counter, chunk_size))


if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  q = Query()
  res = mysql_utils.execute_no_fetch_w_info(q.create_table_look_up_tax_query)
  print(q.create_table_look_up_tax_query, res)

  q.alter_table_look_up_tax()
  q.update_table_look_up_tax()
  
  """TODO: args - create, update"""

  #
  # t = utils.benchmark_w_return_1("get_metadata_info")
  # metadata.get_metadata_info()
  # utils.benchmark_w_return_2(t, "get_metadata_info")
  #

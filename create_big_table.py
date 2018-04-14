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
    pass
  
  def create_table_look_up_tax(self):
    create_table_look_up_tax_query = """create table look_up_tax
      as
      SELECT sum(seq_count), dataset_id, domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id, sequence_id FROM sequence_pdr_info JOIN silva_taxonomy_info_per_seq USING(sequence_id) JOIN silva_taxonomy USING(silva_taxonomy_id) limit 1"""

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  # project_name_startswith = sys.argv[1] if len(sys.argv) == 2 else 'DCO'
  q = Query()
  res = mysql_utils.execute_no_fetch_w_info(q)
  print(res)
  
  #
  # t = utils.benchmark_w_return_1("get_metadata_info")
  # metadata.get_metadata_info()
  # utils.benchmark_w_return_2(t, "get_metadata_info")
  #

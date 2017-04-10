# from collections import defaultdict
# import time
import util
import MySQLdb
import csv
import sys

class Metadata():
  def __init__(self, project_name_startswith):
    self.project_name_startswith = project_name_startswith
  
  def get_required_info(self):
    t = utils.benchmark_w_return_1("get_all_custom_tables")
    all_custom_table_names = self.get_all_custom_tables()
    utils.benchmark_w_return_2(t, "get_all_custom_tables")
    
    t = utils.benchmark_w_return_1("get_project_ids")
    project_ids = self.get_project_ids()
    utils.benchmark_w_return_2(t, "get_project_ids")
    
    
  def get_custom_info(self):
    pass

  def combine_req_n_custome(self):
    pass
    
  def add_all_empty_fields(self):
    pass
    
  def write_csv_file(self):
    pass
  
  def get_all_custom_tables(self):
    query_custom_tables = """
    SELECT table_name FROM information_schema.tables
    WHERE TABLE_NAME LIKE "custom_metadata_%"
    AND table_schema = "vamps2"
    """
    return mysql_utils.execute_fetch_select(query_custom_tables)
    
  def get_project_ids(self):
    query_project_ids = """select project_id, project from project where project like '%s%%' """ % (self.project_name_startswith)
    return mysql_utils.execute_fetch_select(query_project_ids)


if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  project_name_startswith = sys.argv[1] if len(sys.argv) == 2 else 'DCO'
  metadata = Metadata(project_name_startswith)
  
  t = utils.benchmark_w_return_1("get_required_info")
  metadata.get_required_info()
  utils.benchmark_w_return_2(t, "get_required_info")
  
  t = utils.benchmark_w_return_1("get_custom_info")
  metadata.get_custom_info()
  utils.benchmark_w_return_2(t, "get_custom_info")
  
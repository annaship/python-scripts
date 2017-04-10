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

    t = utils.benchmark_w_return_1("all_project_ids_to_str")
    all_project_ids_str = self.all_project_ids_to_str(project_ids)
    utils.benchmark_w_return_2(t, "all_project_ids_to_str")
    
    t = utils.benchmark_w_return_1("get_custom_fields")
    custom_fields = self.get_custom_fields(all_project_ids_str)
    print "PPP"
    print custom_fields
    utils.benchmark_w_return_2(t, "get_custom_fields")
    # self.make_custom_table_name_list(all_project_ids_str)
    
    
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

  def get_custom_fields(self, all_project_ids_str):
    for table_name in self.make_custom_table_name_list(all_project_ids_str):
      get_metadata_query = """ select 

      """

    custom_fields_query = """SELECT DISTINCT project_id, field_name, field_units, example FROM custom_metadata_fields WHERE project_id in (%s)""" % (", ".join(all_project_ids_str))
    # print custom_fields_query
    custom_fields = mysql_utils.execute_fetch_select(custom_fields_query)
    print custom_fields
    """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
    return custom_fields
   
  def all_project_ids_to_str(self, all_project_ids):
    return [str(int(x[0])) for x in all_project_ids[0]]

  def make_custom_table_name_list(self, all_project_ids_str):
    return ['custom_metadata_' + x for x in all_project_ids_str]
  


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
  
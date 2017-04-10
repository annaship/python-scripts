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

    # t = utils.benchmark_w_return_1("all_project_ids_to_str")
    # all_project_ids_str = self.all_project_ids_to_str(project_ids)
    # utils.benchmark_w_return_2(t, "all_project_ids_to_str")
    
    t = utils.benchmark_w_return_1("get_custom_fields")
    custom_fields = self.get_custom_fields(self.all_project_ids_to_str(project_ids))
    utils.benchmark_w_return_2(t, "get_custom_fields")

    t = utils.benchmark_w_return_1("get_project_datasets_metadata")
    raw_metadata = self.get_project_datasets_metadata(custom_tables)
    print raw_metadata
    utils.benchmark_w_return_2(t, "get_project_datasets_metadata")
        
  def get_project_datasets_metadata(self, custom_tables):
    custom_metadata_values_per_project_dataset = []

    for custom_table in custom_tables:
      # TODO: combine with get_custom_metadata_per_project
      poject_dataset_query = """SELECT DISTINCT project_id, project, dataset.dataset as sample, %s.* FROM %s JOIN dataset USING(dataset_id) JOIN project USING(project_id) JOIN required_metadata_info USING(dataset_id)"""
      try:
        res = mysql_utils.execute_fetch_select_where(poject_dataset_query, (custom_table, custom_table))
        # print res
        custom_metadata_values_per_project_dataset.append(res)
        # (((300L, 'DCO_BKR_Av4v5', 'Knox_63E_6H2', 1L, 238918L, '2330', 'MP Biomedical FAST DNA', '451', '58.2', '8.02', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '8.82', 'Vared Clay/Silty Clay', '14.8', 'Knox63E6H2', 11.5), (300L, 'DCO_BKR_Av4v5', 'Aar_DrillFluid_59E_NC', 2L, 238915L, '', 'MP Biomedical FAST DNA', '', '', '', 'Baltic Sea Basin', '', '', '-80', '16S DNA', '', 'drill fluid', '', 'AarDrillFluid59ENC', 0.0), (300L, 'DCO_BKR_Av4v5', 'Aar_59E_25H2', 3L, 238914L, '810', 'MP Biomedical FAST DNA', '35', '6.1', '7.01', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '7.93', 'Vared Clay/Silty Clay', '9.05', 'Aar59E25H2', 81.5), (300L, 'DCO_BKR_Av4v5', 'Knox_65C_7H2', 4L, 238917L, '5400', 'MP Biomedical FAST DNA', '87', '7.17', '7.41', 'Baltic Sea Basin', 'perfluorocarbon tracer', '170', '-80', '16S DNA', '', 'Vared Clay/Silty Clay', '6.8', 'Knox65C7H2', 20.35), (300L, 'DCO_BKR_Av4v5', 'Knox_60B_10H2', 5L, 238916L, '0', 'MP Biomedical FAST DNA', '34', '9.05', '7.89', 'Baltic Sea Basin', 'perfluorocarbon tracer', '8300', '-80', '16S DNA', '8.36', 'Vared Clay/Silty Clay', '26.7', 'Knox60B10H2', 27.4)), ['project_id', 'project', 'sample', 'custom_metadata_300_id', 'dataset_id', 'methane', 'dna_extraction_meth', 'tot_depth_water_col', 'alkalinity', 'pH', 'geo_loc_name', 'quality_method', 'sulfate', 'samp_store_temp', 'target_gene', 'microbial_biomass_microscopic', 'lithology', 'salinity', 'sample_id', 'depth'])
      except MySQLdb.ProgrammingError:
        pass
      # _mysql_exceptions.ProgrammingError
      except:
        raise
      # MySQLdb.OperationalError, e
    return custom_metadata_values_per_project_dataset
    
    
    print "PPP"
    print custom_fields
    
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
    query_project_ids = """SELECT project_id, project FROM project WHERE project LIKE %s """ 
    # % (self.project_name_startswith)
    return mysql_utils.execute_fetch_select_where(query_project_ids, (self.project_name_startswith + "%"))

  def get_custom_fields(self, all_project_ids_str):
    custom_fields_query = """SELECT DISTINCT project_id, field_name, field_units, example FROM custom_metadata_fields WHERE project_id in (%s)""" % (", ".join(all_project_ids_str))
    # print custom_fields_query
    custom_fields = mysql_utils.execute_fetch_select(custom_fields_query)
    # print custom_fields
    """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
    return custom_fields
   
  def all_project_ids_to_str(self, all_project_ids):
    return [str(int(x[0])) for x in all_project_ids[0]]

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
  
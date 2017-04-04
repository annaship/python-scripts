import IlluminaUtils.lib.fastalib as fa
import gzip
from itertools import izip
from collections import defaultdict
import time
import util
import MySQLdb

class Metadata():
  def __init__(self):
    pass

  def get_all_all_custom_tables(self):
    query_custom_tables = """
    SELECT table_name FROM information_schema.tables
    WHERE TABLE_NAME LIKE "custom_metadata_%"
    AND table_schema = "vamps2"
    """
    return mysql_utils.execute_fetch_select(query_custom_tables)
  
  def get_all_dco_project_ids(self):
    query_project_ids = """select project_id, project from project where project like "DCO%" """
    return mysql_utils.execute_fetch_select(query_project_ids)
    
  def all_dco_project_ids_to_str(self, all_dco_project_ids):
    return [str(int(x[0])) for x in all_dco_project_ids[0]]
    
  def make_dco_cutom_table_name_list(self, all_project_ids_str):
    return ['custom_metadata_' + x for x in all_project_ids_str]

  def get_dco_custom_fields(self, dco_custom_tables):
    for table_name in dco_custom_tables:
      get_metadata_query = """ select 

      """

    dco_custom_fields_query = """SELECT DISTINCT project_id, field_name, field_units, example FROM custom_metadata_fields WHERE project_id in (%s)""" % (", ".join(all_project_ids_str))
    # print dco_custom_fields_query
    dco_custom_fields = mysql_utils.execute_fetch_select(dco_custom_fields_query)
    # print dco_custom_fields
    """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
    return dco_custom_fields
    
  # TODO: get all join project and dataset?
  def get_custom_metadata_per_project(self, project_id, field_name):
    query = """select `%s` from custom_metadata_%s""" % (field_name, str(project_id))
    # print query
    return mysql_utils.execute_fetch_select(query)
    
  def make_custom_metadata_distinct_list(self, custom_metadata):
    return [y[0] for y in set([x for x in custom_metadata[0]])]
  
  def populate_dict_of_dicts(self, my_dict, key, key_to_use = ""):
    if key_to_use == "":
      key_to_use = key
    # print "9" * 9
    # print my_dict
    # print "key = %s" % key
    if key not in my_dict:
        my_dict[key_to_use] = {}
    return my_dict

  def populate_dict_of_lists(self, my_dict, key, key_to_use = ""):
    if key_to_use == "":
      key_to_use = key
    if key not in my_dict:
        my_dict[key_to_use] = []
    return my_dict
  
  def make_my_dict(self, my_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list):
    my_dict = self.populate_dict_of_dicts(my_dict, str_project_id)

    if field_name not in my_dict[str_project_id]:
        my_dict[str_project_id][field_name__descr] = []

    my_dict[str_project_id][field_name__descr].append(custom_metadata_distinct_list)
    return my_dict
    
  def get_project_name(self, all_dco_project_ids, str_project_id):
    return [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    
  def make_custom_metadata_per_field_dict(self, my_dict2, custom_metadata_distinct_list, field_name__descr):
    for custom_metadatum in custom_metadata_distinct_list:
      my_dict2 = self.populate_dict_of_lists(my_dict2, field_name__descr)
      
      my_dict2[field_name__descr].append(custom_metadatum)
    return my_dict2
    
  def print_all_from_dict_of_lists(self, custom_metadata_per_field_dict):
    for k, v in custom_metadata_per_field_dict.items():
      print k, set([item for sublist in v for item in sublist])

    print len(set(all_field_name__descr))
    # print set(all_field_name__descr)
    
  def get_project_datasets_custom_metadata(self, dco_custom_tables):
    custom_metadata_values_per_project_dataset = []
    
    for dco_custom_table in dco_custom_tables:
      # TODO: combine with get_custom_metadata_per_project
      dco_poject_dataset_query = """SELECT DISTINCT project_id, project, dataset.dataset as sample, %s.* FROM %s JOIN dataset USING(dataset_id) JOIN project USING(project_id)""" % (dco_custom_table, dco_custom_table)
      try:
        res = mysql_utils.execute_fetch_select(dco_poject_dataset_query)
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
  
if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  metadata = Metadata()
  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  # print a
  
  all_custom_tables = metadata.get_all_all_custom_tables()
  
  query_project_ids = """select project_id, project from project where project like "DCO%" """
  all_dco_project_ids = metadata.get_all_dco_project_ids()
  
  all_project_ids_str = metadata.all_dco_project_ids_to_str(all_dco_project_ids)
  # print dco_custom_tables
  # print len(dco_custom_tables)
  # 64

  dco_custom_tables = metadata.make_dco_cutom_table_name_list(all_project_ids_str)
  dco_custom_fields = metadata.get_dco_custom_fields(dco_custom_tables)
  # print "=" * 5
  # print dco_custom_fields
  
  custom_metadata_distinct_list_per_field_per_project_dict = {}
  
  all_field_names = []
  all_field_name__descr = []
  for dco_custom_field_info in dco_custom_fields[0]:
    # print "dco_custom_field_info"
    # print dco_custom_field_info
    # (860L, 'resistivity', 'ohm-meters', 'n.d.')
    # (860L, 'trace element geochemistry', '', 'yes')
    project_id = dco_custom_field_info[0]
    field_name = dco_custom_field_info[1]
    # ((('',), ('',), ('',), ('',), ('',), ('',), ('',), ('',), ('3363',), ('2796',), ('',), ('',), ('',), ('',), ('',), ('',), ('4500',), ('4286',)), ['methane'])
    
    custom_metadata_distinct_list = metadata.make_custom_metadata_distinct_list(metadata.get_custom_metadata_per_project(project_id, field_name))
    # ['3363', '4500', '', '4286', '2796']
    
    str_project_id = str(project_id)
    field_name__descr = field_name + "__" + dco_custom_field_info[2]
    all_field_names.append(field_name)
    all_field_name__descr.append(field_name__descr)

    custom_metadata_distinct_list_per_field_per_project_dict = metadata.make_my_dict(custom_metadata_distinct_list_per_field_per_project_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list)

  custom_metadata_per_field_dict = {}
  for str_project_id, d1 in custom_metadata_distinct_list_per_field_per_project_dict.items():  
    project_name = metadata.get_project_name(all_dco_project_ids, str_project_id)      
    for field_name__descr, custom_metadata_distinct_list in d1.items():
      custom_metadata_per_field_dict = metadata.make_custom_metadata_per_field_dict(custom_metadata_per_field_dict, custom_metadata_distinct_list, field_name__descr)
  
  # === make project_dataset x all_fields table ===
  # custom_metadata_values_per_project_dataset = [] #list of dicts
  #
  #
  # for dco_custom_table in dco_custom_tables:
  #   dco_poject_dataset_query = """SELECT DISTINCT * FROM %s JOIN dataset USING(dataset_id) JOIN project USING(project_id)""" % (dco_custom_table)
  #   try:
  #     print "IIIIII"
  #     print mysql_utils.execute_fetch_select(dco_poject_dataset_query)
  #     # ((300L, 238918L, 1L, '2330', 'MP Biomedical FAST DNA', '451', '58.2', '8.02', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '8.82', 'Vared Clay/Silty Clay', '14.8', 'Knox63E6H2', 11.5, 'Knox_63E_6H2', 'Hole 63E', datetime.datetime(2016, 6, 16, 8, 22, 43), datetime.datetime(2016, 6, 16, 8, 22, 43), 'DCO_BKR_Av4v5', 'DCO_BKR_Av4v5', 'BKR_BAL_Av4v5', '5v4vA_RKB_OCD', '', 104L, 1, datetime.datetime(2016, 6, 16, 8, 22, 43), datetime.datetime(2016, 6, 16, 8, 22, 43)),
  #     # ...
  #     # (300L, 238916L, 5L, '0', 'MP Biomedical FAST DNA', '34', '9.05', '7.89', 'Baltic Sea Basin', 'perfluorocarbon tracer', '8300', '-80', '16S DNA', '8.36', 'Vared Clay/Silty Clay', '26.7', 'Knox60B10H2', 27.4, 'Knox_60B_10H2', 'Hole 60B', datetime.datetime(2016, 6, 16, 8, 22, 43), datetime.datetime(2016, 6, 16, 8, 22, 43), 'DCO_BKR_Av4v5', 'DCO_BKR_Av4v5', 'BKR_BAL_Av4v5', '5v4vA_RKB_OCD', '', 104L, 1, datetime.datetime(2016, 6, 16, 8, 22, 43), datetime.datetime(2016, 6, 16, 8, 22, 43))), ['project_id', 'dataset_id', 'custom_metadata_300_id', 'methane', 'dna_extraction_meth', 'tot_depth_water_col', 'alkalinity', 'pH', 'geo_loc_name', 'quality_method', 'sulfate', 'samp_store_temp', 'target_gene', 'microbial_biomass_microscopic', 'lithology', 'salinity', 'sample_id', 'depth', 'dataset', 'dataset_description', 'created_at', 'updated_at', 'project', 'title', 'project_description', 'rev_project_name', 'funding', 'owner_user_id', 'public', 'created_at', 'updated_at'])
  #   except:
  #     pass
    
  #   dco_dataset_query = """SELECT DISTINCT project, dataset FROM %s JOIN dataset_id WHERE project_id in (%s)""" % (dco_custom_table))
  # ===
  
  custom_metadata_values_per_project_dataset = metadata.get_project_datasets_custom_metadata(dco_custom_tables)
  
  print "PPP"
  # print custom_metadata_values_per_project_dataset
  for x in custom_metadata_values_per_project_dataset:
    project_id = x[0][0][0]
    file_name = "custom_metadata_per_project_%s.csv" % (project_id)
    utils.write_to_csv_file(file_name, x, file_mode = "wb")
    # data_from_db, field_names = x
  
  
  metadata.print_all_from_dict_of_lists(custom_metadata_per_field_dict)

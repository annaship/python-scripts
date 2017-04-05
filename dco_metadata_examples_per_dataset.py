import IlluminaUtils.lib.fastalib as fa
import gzip
from itertools import izip
from collections import defaultdict
import time
import util
import MySQLdb
import csv

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
    
  def make_empty_marker_line(self, dataset_len):
    empty_marker = [1] * dataset_len
    empty_marker.insert(0, "All fields are empty?")
    return empty_marker
  
  def make_rows_for_all_fields(self, custom_m_field_names, dataset_cnt):
    return set(all_field_name__descr) - set(custom_m_field_names)
    
  def make_custom_metadata_matrix(self, custom_metadata_matrix, one_table_res_data):
    for one_dataset in one_table_res_data:
      """
      (300L, 'DCO_BKR_Av4v5', 'Knox_63E_6H2', 1L, 238918L, '2330', 'MP Biomedical FAST DNA', '451', '58.2', '8.02', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '8.82', 'Vared Clay/Silty Clay', '14.8', 'Knox63E6H2', 11.5)
      """

      project_dataset = "%s--%s" % (one_dataset[1], one_dataset[2])
      one_line = list(one_dataset[5:])
      one_line.insert(0, project_dataset)
      custom_metadata_matrix.append(one_line)
    return custom_metadata_matrix
  
  def make_custom_m_field_names_unis(self, project_id, one_table_res, all_field_name__descr_per_project):
    # all_field_name__descr_per_project
    # 88L: ['methane__microMolar', 'sulfate__micromole_per_kilogram', 'sulfide__micromole_per_kilogram', 'conductivity__milliseimenPerCentimeter', 'sample_id__Alphanumeric', 'pH__logH+', 'sodium__micromole_per_kilogram', 'iron_II__micromole_per_kilogram', 'calcium__micromole_per_kilogram', 'chloride__micromole_per_kilogram', 'temp__celsius', 'pressure__decibar', 'potassium__micromole_per_kilogram', 'geo_loc_name__Alphanumeric', 'isol_growth_cond__Alphanumeric', 'dna_extraction_meth__Alphanumeric', 'nitrite__micromole_per_kilogram', 'env_feature__Alphanumeric', 'redox_state__Alphanumeric', 'sample_volume__liter', 'sequencing_meth__Alphanumeric', 'env_material__Alphanumeric', 'samp_store_temp__celsius', 'quality_method__Alphanumeric', 'target_gene__Alphanumeric', 'depth__meter']
    
    # print "dco_custom_fields[0]"
    # print dco_custom_fields[0]
    # print "one_table_res"
    # print one_table_res
    
    # print "YYY"
    # print all_field_name__descr_per_project[project_id]
    custom_m_field_names = []
    
    for a in one_table_res[1][5:]:
      for b in all_field_name__descr_per_project[project_id]:
        if b.startswith(a):
          # print a, b
          custom_m_field_names.append(b)
          
      
    # custom_m_field_names = one_table_res[1][5:]
    custom_m_field_names.insert(0, "Field--Unit for all DCO projects")
  
    # print "PPP"
    return custom_m_field_names
  
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
  all_field_name__descr_per_project = defaultdict(list)
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

    all_field_name__descr_per_project[project_id].append(field_name__descr)
    
    custom_metadata_distinct_list_per_field_per_project_dict = metadata.make_my_dict(custom_metadata_distinct_list_per_field_per_project_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list)

  # print "LLL"
  # print all_field_name__descr_per_project
  # 88L: ['methane__microMolar', 'sulfate__micromole_per_kilogram', 'sulfide__micromole_per_kilogram', 'conductivity__milliseimenPerCentimeter', 'sample_id__Alphanumeric', 'pH__logH+', 'sodium__micromole_per_kilogram', 'iron_II__micromole_per_kilogram', 'calcium__micromole_per_kilogram', 'chloride__micromole_per_kilogram', 'temp__celsius', 'pressure__decibar', 'potassium__micromole_per_kilogram', 'geo_loc_name__Alphanumeric', 'isol_growth_cond__Alphanumeric', 'dna_extraction_meth__Alphanumeric', 'nitrite__micromole_per_kilogram', 'env_feature__Alphanumeric', 'redox_state__Alphanumeric', 'sample_volume__liter', 'sequencing_meth__Alphanumeric', 'env_material__Alphanumeric', 'samp_store_temp__celsius', 'quality_method__Alphanumeric', 'target_gene__Alphanumeric', 'depth__meter']
  
  custom_metadata_per_field_dict = {}
  for str_project_id, d1 in custom_metadata_distinct_list_per_field_per_project_dict.items():  
    project_name = metadata.get_project_name(all_dco_project_ids, str_project_id)      
    for field_name__descr, custom_metadata_distinct_list in d1.items():
      custom_metadata_per_field_dict = metadata.make_custom_metadata_per_field_dict(custom_metadata_per_field_dict, custom_metadata_distinct_list, field_name__descr)
  
  custom_metadata_values_per_project_dataset = metadata.get_project_datasets_custom_metadata(dco_custom_tables)
  
  metadata_per_project_dataset_dict = {}
  # print custom_metadata_values_per_project_dataset
  for one_table_res in custom_metadata_values_per_project_dataset:
    # print one_table_res
    """
(((300L, 'DCO_BKR_Av4v5', 'Knox_63E_6H2', 1L, 238918L, '2330', 'MP Biomedical FAST DNA', '451', '58.2', '8.02', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '8.82', 'Vared Clay/Silty Clay', '14.8', 'Knox63E6H2', 11.5
300L, 'DCO_BKR_Av4v5', 'Aar_DrillFluid_59E_NC', 2L, 238915L, '', 'MP Biomedical FAST DNA', '', '', '', 'Baltic Sea Basin', '', '', '-80', '16S DNA', '', 'drill fluid', '', 'AarDrillFluid59ENC', 0.0
300L, 'DCO_BKR_Av4v5', 'Aar_59E_25H2', 3L, 238914L, '810', 'MP Biomedical FAST DNA', '35', '6.1', '7.01', 'Baltic Sea Basin', 'perfluorocarbon tracer', '70', '-80', '16S DNA', '7.93', 'Vared Clay/Silty Clay', '9.05', 'Aar59E25H2', 81.5
300L, 'DCO_BKR_Av4v5', 'Knox_65C_7H2', 4L, 238917L, '5400', 'MP Biomedical FAST DNA', '87', '7.17', '7.41', 'Baltic Sea Basin', 'perfluorocarbon tracer', '170', '-80', '16S DNA', '', 'Vared Clay/Silty Clay', '6.8', 'Knox65C7H2', 20.35
300L, 'DCO_BKR_Av4v5', 'Knox_60B_10H2', 5L, 238916L, '0', 'MP Biomedical FAST DNA', '34', '9.05', '7.89', 'Baltic Sea Basin', 'perfluorocarbon tracer', '8300', '-80', '16S DNA', '8.36', 'Vared Clay/Silty Clay', '26.7', 'Knox60B10H2', 27.4)), ['project_id', 'project', 'sample', 'custom_metadata_300_id', 'dataset_id', 'methane', 'dna_extraction_meth', 'tot_depth_water_col', 'alkalinity', 'pH', 'geo_loc_name', 'quality_method', 'sulfate', 'samp_store_temp', 'target_gene', 'microbial_biomass_microscopic', 'lithology', 'salinity', 'sample_id', 'depth'])
    
    """
    project_id = one_table_res[0][0][0]
    
    custom_m_field_names = metadata.make_custom_m_field_names_unis(project_id, one_table_res, all_field_name__descr_per_project)

    all_fields = metadata.make_rows_for_all_fields(custom_m_field_names, len(one_table_res[0]))
    # print "AAA"
    # print custom_m_field_names
    # print all_fields
    custom_m_field_names = custom_m_field_names + list(all_fields)
    # print "AAA"
    # print custom_m_field_names
    # print all_fields
    
    

    # print "GGG"
    # print all_field_name__descr
    # print "PPP"
    # print custom_m_field_names
    """    
    ['Field--Name for all DCO projects', 'diss_inorg_carb', 'rock_type', 'geo_loc_name', 'chloride', 'pH', 'calcium', 'samp_store_temp', 'redox_state', 'samp_store_dur', 'phosphate', 'access_point_type', 'sample_id', 'dna_extraction_meth', 'tot_depth_water_col', 'depth']
    """    
    custom_metadata_matrix = []
    custom_metadata_matrix.append(custom_m_field_names)
    
    dataset_len = len(one_table_res[0][0]) - 5
    
    empty_marker = metadata.make_empty_marker_line(dataset_len)
    custom_metadata_matrix.append(empty_marker)
    
    custom_metadata_matrix = metadata.make_custom_metadata_matrix(custom_metadata_matrix, one_table_res[0])

    # custom_metadata_matrix.append(list(all_fields))
    # print "zzz custom_metadata_matrix"
    # print custom_metadata_matrix
    transposed_matrix = zip(*custom_metadata_matrix)
    # print "CCC transposed_matrix"
    # print transposed_matrix
    """
    [('diss_inorg_carb', '10900', '41100', '65800', '21400', '23500', '5100', '35000', '33000'), ('rock_type', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment'), ('geo_loc_name', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea'), ('chloride', '558186.2', '511987.9', '588246', '520077.9', '753698.1', '551636.8', '548302.6', '522290.7'), ('pH', '7.67', '7.94', '7.76', '8.15', '7.78', '7.38', '7.65', '7.72'), ('calcium', '8718.8', '3592.5', '3614.5', '4464', '5166.6', '9726.9', '2601.1', '2654.1'), ('samp_store_temp', '-80', '-80', '-80', '-80', '-80', '-80', '-80', '-80'), ('redox_state', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic'), ('samp_store_dur', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y'), ('phosphate', '70.48', '37.01', '268.05', '6.99', '113.5', '19.83', '146.57', '121.17'), ('access_point_type', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core'), ('sample_id', 'BS-2 (B)', 'BS-7 (B)', 'BS-6 (B)', 'BS-8 (B)', 'BS-3 (B)', 'BS-1 (B)', 'BS-5 (B)', 'BS-4 (B)'), ('dna_extraction_meth', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil'), ('tot_depth_water_col', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9'), ('depth', 1.65, 214.17, 89.32, 404.61, 5.65, 0.15, 11.65, 8.65)]
    
    """
    file_name = "custom_metadata_per_project_%s.csv" % (project_id)
    
    with open(file_name, "wb") as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerows(transposed_matrix)
      
  print "DDD"
  for k, v in custom_metadata_per_field_dict.items():
    print k.split("__")[0], set([item for sublist in v for item in sublist])
  print "FFF"

  # metadata.print_all_from_dict_of_lists(custom_metadata_per_field_dict) 
  # TODO: add required
  # add units
  # add all feilds
  # restructure: all operations with custom_field table, all operations with custom_metadata tables, all operations with req. table
  # get_project_datasets interm. TODO: make a dict
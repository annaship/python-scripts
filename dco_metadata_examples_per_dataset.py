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

  def get_dco_custom_fields(self, dco_custom_tables, all_project_ids_str):
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
    query = """SELECT `%s` FROM custom_metadata_%s""" % (field_name, str(project_id))
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

  def make_dict_field_values(self, dict_field_values, str_project_id, field_name, custom_metadata_distinct_list):
    dict_field_values = self.populate_dict_of_lists(dict_field_values, field_name)
    # print "UUU"
    # print dict_field_values
    # dict_field_values[field_name] = []
    dict_field_values[field_name].append(custom_metadata_distinct_list)
    return dict_field_values

    
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
  
  def make_rows_for_all_fields(self, custom_md_field_names_for_1_pr, dataset_cnt):
    return set(all_field_name__descr) - set(custom_md_field_names_for_1_pr)
    
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
  
  def make_custom_md_field_names_for_1_pr_unis(self, project_id, one_table_res, all_field_name__descr_per_project):
    # all_field_name__descr_per_project
    # 88L: ['methane__microMolar', 'sulfate__micromole_per_kilogram', 'sulfide__micromole_per_kilogram', 'conductivity__milliseimenPerCentimeter', 'sample_id__Alphanumeric', 'pH__logH+', 'sodium__micromole_per_kilogram', 'iron_II__micromole_per_kilogram', 'calcium__micromole_per_kilogram', 'chloride__micromole_per_kilogram', 'temp__celsius', 'pressure__decibar', 'potassium__micromole_per_kilogram', 'geo_loc_name__Alphanumeric', 'isol_growth_cond__Alphanumeric', 'dna_extraction_meth__Alphanumeric', 'nitrite__micromole_per_kilogram', 'env_feature__Alphanumeric', 'redox_state__Alphanumeric', 'sample_volume__liter', 'sequencing_meth__Alphanumeric', 'env_material__Alphanumeric', 'samp_store_temp__celsius', 'quality_method__Alphanumeric', 'target_gene__Alphanumeric', 'depth__meter']
    
    # print "dco_custom_fields[0]"
    # print dco_custom_fields[0]
    # print "one_table_res"
    # print one_table_res
    
    # print "YYY"
    # print all_field_name__descr_per_project[project_id]
    custom_md_field_names_for_1_pr = []
    
    for a in one_table_res[1][5:]:
      for b in all_field_name__descr_per_project[project_id]:
        if b.startswith(a):
          # print a, b
          custom_md_field_names_for_1_pr.append(b)
          
      
    # custom_md_field_names_for_1_pr = one_table_res[1][5:]
    custom_md_field_names_for_1_pr.insert(0, "Field--Unit for all DCO projects")
  
    # print "PPP"
    return custom_md_field_names_for_1_pr
  
  # TODO: make a "flatten dict value" method
  def make_field_values_dict_flat(self, field_values_dict):
    field_values_dict_flat = defaultdict(list)
    for k, v in field_values_dict.items():
      field_values_dict_flat[k] = list(utils.flatten_2d_list(v))
    return field_values_dict_flat

  def print_all_values_per_field_name(self, field_values_dict_flat):
    for k, v in field_values_dict_flat.items():
      distinct_list = list(set(v))
      print k, utils.sort_case_insesitive(distinct_list)
      # sorted(list(set([item for sublist in v for item in sublist])))

  def make_empty_fields(self, all_field_name__descr, custom_md_field_names_for_1_pr):
    return set(all_field_name__descr) - set(custom_md_field_names_for_1_pr)
    
  def make_transposed_empty_fields_lines(self, empty_fields):
    all_zeros = [0]*len(empty_fields)
    add_lines = [empty_fields, all_zeros]
    return zip(*add_lines)
    
  def custom_metadata(self):
    all_custom_tables = self.get_all_all_custom_tables()

    query_project_ids = """select project_id, project from project where project like "DCO%" """
    all_dco_project_ids = self.get_all_dco_project_ids()

    all_project_ids_str = self.all_dco_project_ids_to_str(all_dco_project_ids)
    # print dco_custom_tables
    # print len(dco_custom_tables)
    # 64

    dco_custom_tables = self.make_dco_cutom_table_name_list(all_project_ids_str)
    dco_custom_fields = self.get_dco_custom_fields(dco_custom_tables, all_project_ids_str)
    # print "=" * 5
    # print dco_custom_fields

    custom_metadata_distinct_list_per_field_per_project_dict = {}
    field_values_dict = defaultdict(list)

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
  
      custom_metadata_distinct_list = self.make_custom_metadata_distinct_list(self.get_custom_metadata_per_project(project_id, field_name))
      # ['3363', '4500', '', '4286', '2796']
  
      str_project_id = str(project_id)
      field_name__descr = field_name + "__" + dco_custom_field_info[2]
      all_field_names.append(field_name)
      all_field_name__descr.append(field_name__descr)

      all_field_name__descr_per_project[project_id].append(field_name__descr)
  
      custom_metadata_distinct_list_per_field_per_project_dict = self.make_my_dict(custom_metadata_distinct_list_per_field_per_project_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list)

      field_values_dict = self.make_dict_field_values(field_values_dict, str_project_id, field_name, custom_metadata_distinct_list)


    # field_values_dict_flat = defaultdict(list)
    # for k, v in field_values_dict.items():
    #   field_values_dict_flat[k] = utils.flatten_2d_list(v)
    field_values_dict_flat = self.make_field_values_dict_flat(field_values_dict)
    # print "LLL"
    # print field_values_dict_flat



    """
    print "LLL"
    print field_values_dict
    'geo_loc_name': [['sweden', 'finland', 'Finland'], ['Olkiluoto'], ['Pacific Ocean'], ['Baltic Sea Basin'], ['Baltic Sea Basin'], ['Olkiluoto'], ['Pacific Ocean'], ['Andaman Sea'], ['Andaman Sea'], ['Canada', 'USA', 'Italy'], ['USA', 'Federated States of Micronesia'], ['USA', 'Federated States of Micronesia'], ['USA (Minnesota)'], ['USA'], ['USA'], ['Sweden', 'Finland'], ['Sweden', 'Finland'], ['South Africa'], ['South Africa'], ['Pacific Ocean'], ['Pacific Ocean'], ['Arctic deep sea'], ['Arctic deep sea'], ['Pacific Ocean', 'Los Angeles'], ['Bering Sea'], ['Atlantic Ocean', 'Rehoboth Bay, DE, USA'], ['Iceland'], ['Iceland'], ['Gulf of Caifornia', 'Gulf of California'], ['Gulf of Caifornia', 'Gulf of California'], ['Mediterranean Sea, Discovery Basin', 'Mediterranean Sea', 'Black Sea'], ['Mediterranean Sea, Discovery Basin', 'Mediterranean Sea', 'Black Sea'], ['Pacific Ocean'], ['Pacific Ocean'], ['Southwestern Taiwan'], ['South Africa'], ['South Africa'], ['Pacific Ocean'], ['Pacific Ocean', 'Atlantic Ocean'], ['Rehoboth Bay, DE, USA'], ['Pacific Ocean, USA'], ['Pacific Ocean', 'Atlantic Ocean'], ['Atlantic Ocean'], ['', 'Nevares Spring'], ['Bering Sea'], ['Pacific Ocean, USA'], ['N/A', 'Ionian Sea'], ['N/A', 'Ionian Sea'], ['Greece']]
    """
  
    """
    print "LLL"
    print all_field_name__descr_per_project
    88L: ['methane__microMolar', 'sulfate__micromole_per_kilogram', 'sulfide__micromole_per_kilogram', 'conductivity__milliseimenPerCentimeter', 'sample_id__Alphanumeric', 'pH__logH+', 'sodium__micromole_per_kilogram', 'iron_II__micromole_per_kilogram', 'calcium__micromole_per_kilogram', 'chloride__micromole_per_kilogram', 'temp__celsius', 'pressure__decibar', 'potassium__micromole_per_kilogram', 'geo_loc_name__Alphanumeric', 'isol_growth_cond__Alphanumeric', 'dna_extraction_meth__Alphanumeric', 'nitrite__micromole_per_kilogram', 'env_feature__Alphanumeric', 'redox_state__Alphanumeric', 'sample_volume__liter', 'sequencing_meth__Alphanumeric', 'env_material__Alphanumeric', 'samp_store_temp__celsius', 'quality_method__Alphanumeric', 'target_gene__Alphanumeric', 'depth__meter']
    """

    custom_metadata_per_field_dict = {}
    for str_project_id, d1 in custom_metadata_distinct_list_per_field_per_project_dict.items():  
      project_name = self.get_project_name(all_dco_project_ids, str_project_id)      
      for field_name__descr, custom_metadata_distinct_list in d1.items():
        custom_metadata_per_field_dict = self.make_custom_metadata_per_field_dict(custom_metadata_per_field_dict, custom_metadata_distinct_list, field_name__descr)

    custom_metadata_values_per_project_dataset = self.get_project_datasets_custom_metadata(dco_custom_tables)

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
  
      custom_md_field_names_for_1_pr = self.make_custom_md_field_names_for_1_pr_unis(project_id, one_table_res, all_field_name__descr_per_project)

      # all_fields = self.make_rows_for_all_fields(custom_md_field_names_for_1_pr, len(one_table_res[0]))
      # print "AAA"
      # print project_id
      # print custom_md_field_names_for_1_pr
      # print all_fields

      empty_fields = self.make_empty_fields(all_field_name__descr, custom_md_field_names_for_1_pr)
      transposed_add_lines_empty_fields = self.make_transposed_empty_fields_lines(empty_fields)
      # # print "AAA"
      # # print custom_md_field_names_for_1_pr
      # # if project_id == 465:
      # #   print "AAA"
      # #   print empty_fields
      
      # print "GGG"
      # print all_field_name__descr
  
      # print "PPP"
      # print custom_md_field_names_for_1_pr
      """    
      ['Field--Name for all DCO projects', 'diss_inorg_carb', 'rock_type', 'geo_loc_name', 'chloride', 'pH', 'calcium', 'samp_store_temp', 'redox_state', 'samp_store_dur', 'phosphate', 'access_point_type', 'sample_id', 'dna_extraction_meth', 'tot_depth_water_col', 'depth']
      """    
      custom_metadata_matrix = []
      custom_metadata_matrix.append(custom_md_field_names_for_1_pr)
  
      dataset_len = len(one_table_res[0][0]) - 5
  
      empty_marker = self.make_empty_marker_line(dataset_len)
      custom_metadata_matrix.append(empty_marker)
  
      custom_metadata_matrix = self.make_custom_metadata_matrix(custom_metadata_matrix, one_table_res[0])

      # custom_metadata_matrix.append(list(all_fields))
      # print "zzz custom_metadata_matrix"
      # print custom_metadata_matrix
      transposed_matrix = zip(*custom_metadata_matrix)
      # print "CCC transposed_matrix"
      # print transposed_matrix
      """
      [('diss_inorg_carb', '10900', '41100', '65800', '21400', '23500', '5100', '35000', '33000'), ('rock_type', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment', 'sediment'), ('geo_loc_name', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea', 'Bering Sea'), ('chloride', '558186.2', '511987.9', '588246', '520077.9', '753698.1', '551636.8', '548302.6', '522290.7'), ('pH', '7.67', '7.94', '7.76', '8.15', '7.78', '7.38', '7.65', '7.72'), ('calcium', '8718.8', '3592.5', '3614.5', '4464', '5166.6', '9726.9', '2601.1', '2654.1'), ('samp_store_temp', '-80', '-80', '-80', '-80', '-80', '-80', '-80', '-80'), ('redox_state', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic', 'anoxic'), ('samp_store_dur', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y', 'P2Y'), ('phosphate', '70.48', '37.01', '268.05', '6.99', '113.5', '19.83', '146.57', '121.17'), ('access_point_type', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core', 'piston core'), ('sample_id', 'BS-2 (B)', 'BS-7 (B)', 'BS-6 (B)', 'BS-8 (B)', 'BS-3 (B)', 'BS-1 (B)', 'BS-5 (B)', 'BS-4 (B)'), ('dna_extraction_meth', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil', 'Mo Bio Power Soil'), ('tot_depth_water_col', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9', '1950.9'), ('depth', 1.65, 214.17, 89.32, 404.61, 5.65, 0.15, 11.65, 8.65)]
  
      """
      # empty_fields = list(all_fields) - custom_md_field_names_for_1_pr
  
      file_name = "custom_metadata_per_project_%s.csv" % (project_id)
  
      with open(file_name, "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(transposed_matrix)
        csv_writer.writerows(transposed_add_lines_empty_fields)
  
    
  def get_required_metadata_dict(self):
    query_required_metadata = """
SELECT
  `required_metadata_info`.`required_metadata_id` AS `required_metadata_id`,
  project_id,
  project,
  dataset_id,
  dataset,
  collection_date,
  env_biome_id,
  `env_biome`.`term_name` AS `env_biome`,
  latitude,
  longitude,
  target_gene_id,
  target_gene,
  dna_region_id,
  dna_region,
  sequencing_platform_id,
  sequencing_platform,
  domain_id,
  domain,
  geo_loc_name_id,
  `geo_loc_name`.`term_name` AS `geo_loc_name`,
  env_feature_id,
  `env_feature`.`term_name` AS `env_feature`,
  env_matter_id,
  `env_matter`.`term_name` AS `env_matter`,
  env_package_id,
  env_package,
  adapter_sequence_id,
  `run_key`.`run_key` AS `adapter_sequence`,
  index_sequence_id,
  `illumina_index`.`illumina_index` AS `index_sequence`,
  primer_suite_id,
  primer_suite
FROM `required_metadata_info` 
JOIN `dataset` USING(dataset_id)
JOIN `project` USING(project_id)
JOIN `dna_region` USING(dna_region_id) 
JOIN `sequencing_platform` USING(sequencing_platform_id) 
JOIN `target_gene` USING(target_gene_id)
JOIN `domain` USING(domain_id)
JOIN `term` `env_feature` ON(`env_feature`.`term_id` = `required_metadata_info`.`env_feature_id`) 
JOIN `term` `env_matter` ON(`env_matter`.`term_id` = `required_metadata_info`.`env_matter_id`) 
JOIN `term` `env_biome` ON(`env_biome`.`term_id` = `required_metadata_info`.`env_biome_id`) 
JOIN `term` `geo_loc_name` ON(`geo_loc_name`.`term_id` = `required_metadata_info`.`geo_loc_name_id`) 
JOIN `env_package` USING(env_package_id) 
JOIN `run_key` ON(`run_key`.`run_key_id` = `required_metadata_info`.`adapter_sequence_id`)
JOIN `illumina_index` ON(`illumina_index`.`illumina_index_id` = `required_metadata_info`.`index_sequence_id`) 
JOIN `primer_suite` USING(primer_suite_id) 
JOIN ref_primer_suite_primer USING(primer_suite_id)
    """
    return mysql_utils.execute_fetch_select_to_dict(query_required_metadata)
  
  def get_primer_info_dict(self):
    # SELECT * FROM ref_primer_suite_primer
    # JOIN primer USING(primer_id)
    # JOIN primer_suite USING(primer_suite_id)
    #
    query_primer_info = """
    SELECT distinct primer_suite, primer, direction, region, sequence, domain FROM ref_primer_suite_primer
    JOIN primer USING(primer_id)
    JOIN primer_suite USING(primer_suite_id)
    order by primer_suite    
    """
    return mysql_utils.execute_fetch_select_to_dict(query_primer_info)
    
  #TODO: split - refactore
  def make_required_metadata_dict_slice(self, required_metadata_dict, required_metadata_fields_ok_list, primer_suite_primers_dict):
  # required_metadata_dict = {k: required_metadata_dict[k] for k in required_metadata_fields_ok_list}
  
    required_metadata_dict_slice = defaultdict(dict)
    for row in required_metadata_dict:
      current_project_id = row['project_id']
      current_primer_suite = row['primer_suite']
      # print "row"
      # print row      
      required_metadata_dict_slice[current_project_id] = {}
      temp_dict = {}
      
      temp_dict['forward_primer'] = ", ".join(primer_suite_primers_dict[current_primer_suite]['F'])
      temp_dict['reverse_primer'] = ", ".join(primer_suite_primers_dict[current_primer_suite]['R'])
      
      for field in set(required_metadata_fields_ok_list) - set(['forward_primer', 'reverse_primer']):
        try:
          temp_dict[field] = row[field]
        except:
          raise
      required_metadata_dict_slice[current_project_id] = temp_dict
    return required_metadata_dict_slice

  def make_primer_suite_primers_dict(self, primer_info_dict):
    primer_suite_primers_dict =  defaultdict(lambda : defaultdict(list))
    for row in primer_info_dict:
      primer_suite_primers_dict[row['primer_suite']][row['direction']].append(row['sequence'].replace(".", "N"))
    return primer_suite_primers_dict
    
  def make_required_metadata(self):
    required_metadata_dict =  self.get_required_metadata_dict()
    # print "MMM"
    # print required_metadata_dict
    
    """
  ...{'domain': 'Bacteria', 'required_metadata_id': 25490L, 'dna_region': 'v6', 'geo_loc_name_id': 8583L, 'adapter_sequence': 'NNNNTCAGC', 'dna_region_id': 12, 'adapter_sequence_id': 1535, 'dataset': '0_2_i_1', 'env_package_id': 19, 'dataset_id': 338482L, 'domain_id': 3L, 'target_gene': '16s', 'env_feature': 'unknown', 'collection_date': 'unknown', 'env_biome': 'unknown', 'index_sequence_id': 43, 'target_gene_id': 1, 'env_feature_id': 6191L, 'geo_loc_name': 'United States of America', 'latitude': None, 'sequencing_platform_id': 2, 'project_id': 516L, 'env_matter_id': 6191L, 'sequencing_platform': 'illumina', 'index_sequence': 'GTAGTA', 'primer_suite_id': 23, 'primer_suite': 'Bacterial V6 Suite', 'env_package': 'unknown', 'longitude': None, 'project': 'VTS_MIC_Bv6', 'env_biome_id': 6191L, 'env_matter': 'unknown'})
    """
    
    primer_info_dict = self.get_primer_info_dict()
    # print "MMM"
    # print primer_info_dict
    # next((item for item in dicts if item["name"] == "Pam"), None)
    """
    ...{'direction': 'R', 'sequence': 'CTGTAGAGGGGG+TAGAA', 'primer_suite': 'Vibrio V4', 'region': 'v4', 'domain': 'bacteria', 'primer': '680R-Vib'})
    """
    primer_suite_primers_dict = self.make_primer_suite_primers_dict(primer_info_dict)
      
    """
    print primer_suite_primers_dict
    ...'Archaeal V6 Suite': defaultdict(<type 'list'>, {'R': ['GWGGTRCATGGCY?GY?CG'], 'F': ['AATTGGA.?TCAACGCC.G']})
    """
    """
    TODO:
    add fields:
    forward_primer
    latitude--Decimal Degrees bounded +-90C
    longitude--Decimal Degrees bounded +-180C
    reverse_primer
    Anchor for trimming (454 sequencing only)
    custom:
    depth continental subsurface--meter
    depth subseafloor--meters
    depth Water Column--meter
    depth within a core -- cm
    
    """
  
    req_fields_all_list = ("Anchor for trimming (454 sequencing only)", "adapter_sequence", "collection_date", "dataset", "direction", "dna_region", "domain", "env_biome", "env_feature", "env_matter", "env_package", "forward_primer", "geo_loc_name", "illumina_index", "latitude--Decimal Degrees bounded +-90C", "longitude--Decimal Degrees bounded +-180C", "project", "reverse_primer", "sequencing_platform", "target_gene")
  
    required_metadata_fields_ok_list = ("project", "dataset", "collection_date", "env_biome", "latitude", "longitude", "target_gene", "dna_region", "sequencing_platform", "domain", "geo_loc_name", "env_feature", "env_matter", "env_package", "adapter_sequence", "index_sequence", "forward_primer", "reverse_primer")
  
    required_metadata_dict_slice = self.make_required_metadata_dict_slice(required_metadata_dict, required_metadata_fields_ok_list, primer_suite_primers_dict)
  
    #
    print "GGG required_metadata_dict_slice"
    print required_metadata_dict_slice
    """  print "GGG required_metadata_dict_slice"
      print required_metadata_dict_slice
    860L: {'env_feature': 'hydrothermal vent', 'domain': 'Bacteria', 'dna_region': 'v4v5', 'adapter_sequence': 'NNNNATGCT', 'collection_date': '2016-05-18', 'env_package': 'extreme habitat', 'index_sequence': 'ACTTGA', 'longitude': None, 'env_biome': 'unknown', 'project': 'DCO_DAL_Bv4v5', 'geo_loc_name': 'Greece', 'latitude': None, 'forward_primer': 'CCAGCAGCCGCGGTAAN, CCAGCAGCTGCGGTAAN', 'reverse_primer': 'ACT[CT]AAANGAATTGACGG, ACTCAAAAGAATTGACGG, ACTCAAAGAAATTGACGG', 'dataset': 'NeoErasmio', 'env_matter': 'water', 'target_gene': '16s', 'sequencing_platform': 'illumina'}
    
    """
    return required_metadata_dict_slice

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
  
  # Uncomment !
  # metadata.custom_metadata()
      
  # print "DDD"
  # metadata.print_all_values_per_field_name(field_values_dict_flat)
  # print "FFF"

  # metadata.print_all_from_dict_of_lists(custom_metadata_per_field_dict) 
  # TODO: add required
  # add units
  # add all feilds
  # restructure: all operations with custom_field table, all operations with custom_metadata tables, all operations with req. table
  # get_project_datasets interm. TODO: make a dict
  
  # === required metadata ===
  
  required_metadata_dict_slice = metadata.make_required_metadata()
#   required_metadata_dict =  metadata.get_required_metadata_dict()
#   # print "MMM"
#   # print required_metadata_dict
#   
#   """
# ...{'domain': 'Bacteria', 'required_metadata_id': 25490L, 'dna_region': 'v6', 'geo_loc_name_id': 8583L, 'adapter_sequence': 'NNNNTCAGC', 'dna_region_id': 12, 'adapter_sequence_id': 1535, 'dataset': '0_2_i_1', 'env_package_id': 19, 'dataset_id': 338482L, 'domain_id': 3L, 'target_gene': '16s', 'env_feature': 'unknown', 'collection_date': 'unknown', 'env_biome': 'unknown', 'index_sequence_id': 43, 'target_gene_id': 1, 'env_feature_id': 6191L, 'geo_loc_name': 'United States of America', 'latitude': None, 'sequencing_platform_id': 2, 'project_id': 516L, 'env_matter_id': 6191L, 'sequencing_platform': 'illumina', 'index_sequence': 'GTAGTA', 'primer_suite_id': 23, 'primer_suite': 'Bacterial V6 Suite', 'env_package': 'unknown', 'longitude': None, 'project': 'VTS_MIC_Bv6', 'env_biome_id': 6191L, 'env_matter': 'unknown'})
#   """
#   
#   primer_info_dict = metadata.get_primer_info_dict()
#   print "MMM"
#   # print primer_info_dict
#   # next((item for item in dicts if item["name"] == "Pam"), None)
#   """
#   ...{'direction': 'R', 'sequence': 'CTGTAGAGGGGG+TAGAA', 'primer_suite': 'Vibrio V4', 'region': 'v4', 'domain': 'bacteria', 'primer': '680R-Vib'})
#   """
#   primer_suite_primers_dict = metadata.make_primer_suite_primers_dict(primer_info_dict)
#     
#   """
#   print primer_suite_primers_dict
#   ...'Archaeal V6 Suite': defaultdict(<type 'list'>, {'R': ['GWGGTRCATGGCY?GY?CG'], 'F': ['AATTGGA.?TCAACGCC.G']})
#   """
#   """
#   TODO:
#   add fields:
#   forward_primer
#   latitude--Decimal Degrees bounded +-90C
#   longitude--Decimal Degrees bounded +-180C
#   reverse_primer
#   Anchor for trimming (454 sequencing only)
#   custom:
#   depth continental subsurface--meter
#   depth subseafloor--meters
#   depth Water Column--meter
#   depth within a core -- cm
#   
#   """
# 
#   req_fields_all_list = ("Anchor for trimming (454 sequencing only)", "adapter_sequence", "collection_date", "dataset", "direction", "dna_region", "domain", "env_biome", "env_feature", "env_matter", "env_package", "forward_primer", "geo_loc_name", "illumina_index", "latitude--Decimal Degrees bounded +-90C", "longitude--Decimal Degrees bounded +-180C", "project", "reverse_primer", "sequencing_platform", "target_gene")
# 
#   required_metadata_fields_ok_list = ("project", "dataset", "collection_date", "env_biome", "latitude", "longitude", "target_gene", "dna_region", "sequencing_platform", "domain", "geo_loc_name", "env_feature", "env_matter", "env_package", "adapter_sequence", "index_sequence", "forward_primer", "reverse_primer")
# 
#   required_metadata_dict_slice = metadata.make_required_metadata_dict_slice(required_metadata_dict, required_metadata_fields_ok_list, primer_suite_primers_dict)
# 
#   #
#   print "GGG required_metadata_dict_slice"
#   print required_metadata_dict_slice
#   """  print "GGG required_metadata_dict_slice"
#     print required_metadata_dict_slice
#   860L: {'env_feature': 'hydrothermal vent', 'domain': 'Bacteria', 'dna_region': 'v4v5', 'adapter_sequence': 'NNNNATGCT', 'collection_date': '2016-05-18', 'env_package': 'extreme habitat', 'index_sequence': 'ACTTGA', 'longitude': None, 'env_biome': 'unknown', 'project': 'DCO_DAL_Bv4v5', 'geo_loc_name': 'Greece', 'latitude': None, 'forward_primer': 'CCAGCAGCCGCGGTAAN, CCAGCAGCTGCGGTAAN', 'reverse_primer': 'ACT[CT]AAANGAATTGACGG, ACTCAAAAGAATTGACGG, ACTCAAAGAAATTGACGG', 'dataset': 'NeoErasmio', 'env_matter': 'water', 'target_gene': '16s', 'sequencing_platform': 'illumina'}
#   
#   """
  
  for project_id, required_metadata_dict in required_metadata_dict_slice.items():
    file_name = "custom_metadata_per_project_%s.csv" % (project_id)
    print file_name
    # TODO: 
    # get dataset_len = len(one_table_res[0])
    # write to csv 
    # key, val in required_metadata_dict.items()
    # key, 1, (val * dataset_len times)
    # TODO:
    # add Mithc's fields
    # add ankor for v4v5 and v3v5
    
    # with open(file_name, "wb") as csv_file:
    #   csv_writer = csv.writer(csv_file)
    #   csv_writer.writerows(transposed_matrix)
    #   csv_writer.writerows(transposed_add_lines_empty_fields)

  
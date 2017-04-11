# from collections import defaultdict
# import time
import util
import MySQLdb
import csv
import sys
from collections import defaultdict

class Metadata():
  """
  Get data from 
  project
  dataset
  custom_fields
  custom and required metadata
  """
  def __init__(self, project_name_startswith):
    self.project_name_startswith = project_name_startswith
  
  def get_metadata_info(self):
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
    raw_custom_fields_units = self.get_custom_fields(all_project_ids_str)
    utils.benchmark_w_return_2(t, "get_custom_fields")

    """
    print "UUU"
    print raw_custom_fields_units
    (((88L, 'methane', 'microMolar', '3363'), (88L,
    """
    
    t = utils.benchmark_w_return_1("get_raw_metadata")
    raw_metadata = self.get_raw_metadata(all_project_ids_str)
    utils.benchmark_w_return_2(t, "get_raw_metadata")

    # print "RRR"
    # print raw_metadata

    """
    print "RRR"
    print raw_metadata
    ...}, {'domain': 'Bacteria', 'required_metadata_id': 16766L, 'dna_region': 'v6v4', 'geo_loc_name_id': 6542L, 'adapter_sequence': 'GACGT', 'dna_region_id': 13, 'adapter_sequence_id': 129, 'dataset': '1374_20R_Bac', 'env_package_id': 3, 'sample_id': '1374-20R', 'sample_volume': '0.005', 'dataset_id': 336354L, 'domain_id': 3L, 'target_gene': '16s', 'rock_type': 'igneous', 'env_feature': 'endolithic habitat', 'samp_store_temp': '-80', 'collection_date': 'unknown', 'formation_name': 'Louisville Seamounts, Rigil Guyot', 'env_biome': 'marine biome', 'custom_metadata_430.geo_loc_name': 'Pacific Ocean', 'target_gene_id': 1, 'tot_depth_water_col': '1545', 'env_feature_id': 1256L, 'lat_lon': '28.596 S, 173.381 W', 'geo_loc_name': 'Pacific Ocean', 'latitude': -28.596, 'sequencing_platform_id': 1, 'project_id': 430L, 'env_matter_id': 1269L, 'custom_metadata_430.dataset_id': 336354L, 'illumina_index': 'unknown', 'run': '20130405', 'dna_extraction_meth': 'CTAB phenol/chloroform extraction', 'lithology': 'aphyric basalt breccia', 'updated_at': datetime.datetime(2017, 3, 13, 12, 54, 33), 'illumina_index_id': 83, 'sequencing_platform': '454', 'primer_suite_id': 9, 'primer_suite': 'Bacterial V6-V4 Suite', 'created_at': datetime.datetime(2016, 6, 17, 13, 38, 34), 'env_package': 'extreme habitat', 'longitude': -173.381, 'project': 'DCO_SYL_Bv6v4', 'depth': 102.9, 'custom_metadata_430_id': 7L, 'env_biome_id': 1116L, 'env_matter': 'rock', 'custom_metadata_430.target_gene': '16S rDNA'})})    
    """
    
    t = utils.benchmark_w_return_1("mix_field_units_metadata")
    field_units_metadata = self.mix_field_units_metadata(raw_custom_fields_units, raw_metadata)
    utils.benchmark_w_return_2(t, "mix_field_units_metadata")
    
  def make_custom_fields_units_per_project(self, raw_custom_fields_units):
    custom_fields_units_per_project = defaultdict(dict)
    
    for field_unit_tuple in raw_custom_fields_units[0]:
      project_id  = field_unit_tuple[0]
      field_name  = field_unit_tuple[1]
      field_units = field_unit_tuple[2]
      custom_fields_units_per_project[str(project_id)][field_name] = field_name + "--" + field_units
    
    return custom_fields_units_per_project

  def mix_field_units_metadata(self, raw_custom_fields_units, raw_metadata):
    # ['project_id', 'field_name', 'field_units', 'example']
    print "UUU"
    
    custom_fields_units_per_project = self.make_custom_fields_units_per_project(raw_custom_fields_units)
    print custom_fields_units_per_project
    
    
    
    for project_id_str in raw_metadata:
      print "*" * 8
      print project_id_str
      for m_dict in raw_metadata[project_id_str]:
        print "-" * 8
        print m_dict
        # print raw_custom_fields_units[0][int(project_id_str)]
    
    # for field_unit_tuple in raw_custom_fields_units[0]:
    #   project_id  = field_unit_tuple[0]
    #   field_name  = field_unit_tuple[1]
    #   field_units = field_unit_tuple[2]
    #   print project_id
    #   for x in raw_metadata[str(project_id)]:
    #     
    #     print x

  def get_raw_metadata(self, all_project_ids_str):
    raw_metadata = defaultdict(list)
    for project_id_str in all_project_ids_str:
      raw_metadata_query = """SELECT DISTINCT
      `required_metadata_info`.`required_metadata_id` AS `required_metadata_id`,
      `dataset`.`project_id` AS `project_id`,
      `project`.`project` AS `project`,
      `required_metadata_info`.`dataset_id` AS `dataset_id`,
      `dataset`.`dataset` AS `dataset`,
      `required_metadata_info`.`collection_date` AS `collection_date`,
      `required_metadata_info`.`env_biome_id` AS `env_biome_id`,
      `env_biome`.`term_name` AS `env_biome`,
      `required_metadata_info`.`latitude` AS `latitude`,
      `required_metadata_info`.`longitude` AS `longitude`,
      `required_metadata_info`.`target_gene_id` AS `target_gene_id`,
      `target_gene`.`target_gene` AS `target_gene`,
      `required_metadata_info`.`dna_region_id` AS `dna_region_id`,
      `dna_region`.`dna_region` AS `dna_region`,
      `required_metadata_info`.`sequencing_platform_id` AS `sequencing_platform_id`,
      `sequencing_platform`.`sequencing_platform` AS `sequencing_platform`,
      `required_metadata_info`.`domain_id` AS `domain_id`,
      `domain`.`domain` AS `domain`,
      `required_metadata_info`.`geo_loc_name_id` AS `geo_loc_name_id`,
      `geo_loc_name`.`term_name` AS `geo_loc_name`,
      `required_metadata_info`.`env_feature_id` AS `env_feature_id`,
      `env_feature`.`term_name` AS `env_feature`,
      `required_metadata_info`.`env_matter_id` AS `env_matter_id`,
      `env_matter`.`term_name` AS `env_matter`,
      `required_metadata_info`.`env_package_id` AS `env_package_id`,
      `env_package`.`env_package` AS `env_package`,
      `required_metadata_info`.`adapter_sequence_id` AS `adapter_sequence_id`,
      `run_key`.`run_key` AS `adapter_sequence`,
      `required_metadata_info`.`illumina_index_id` AS `illumina_index_id`,
      `illumina_index`.`illumina_index` AS `illumina_index`,
      `run`.`run` AS `run`,
      `required_metadata_info`.`primer_suite_id` AS `primer_suite_id`,
      `primer_suite`.`primer_suite` AS `primer_suite`,
      `required_metadata_info`.`created_at` AS `created_at`,
      `required_metadata_info`.`updated_at` AS `updated_at`,
      custom_metadata_%s.*
      FROM `required_metadata_info` 
      JOIN `dataset` USING(dataset_id)
      JOIN `project` USING(project_id)
      JOIN `dna_region` USING(dna_region_id)
      JOIN `sequencing_platform` USING(sequencing_platform_id)
      JOIN `target_gene` USING(target_gene_id)
      JOIN `domain`  USING(domain_id)
      JOIN `term` `env_feature` ON(`env_feature`.`term_id` = `required_metadata_info`.`env_feature_id`) 
      JOIN `term` `env_matter` ON(`env_matter`.`term_id` = `required_metadata_info`.`env_matter_id`) 
      JOIN `term` `env_biome` ON(`env_biome`.`term_id` = `required_metadata_info`.`env_biome_id`) 
      JOIN `term` `geo_loc_name` ON(`geo_loc_name`.`term_id` = `required_metadata_info`.`geo_loc_name_id`) 
      JOIN `env_package` USING(env_package_id)
      JOIN `run_key` ON(`run_key`.`run_key_id` = `required_metadata_info`.`adapter_sequence_id`) 
      JOIN `illumina_index` USING(illumina_index_id)
      JOIN `primer_suite` USING(primer_suite_id)
      JOIN `run` USING(run_id)
      JOIN custom_metadata_%s USING(dataset_id);
      """ % (project_id_str, project_id_str)

      try:
        res = mysql_utils.execute_fetch_select_to_dict(raw_metadata_query)          
        raw_metadata[project_id_str] = res
      except MySQLdb.ProgrammingError:
        pass
      # _mysql_exceptions.ProgrammingError
      except:
        raise
      
    return raw_metadata
    
  def make_filed_units_pairs_per_project(self):
    pass
    
  def make_project_dataset_pairs_per_project(self):
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
    
  def make_custom_table_names_list(self, all_project_ids_str):
    return ['custom_metadata_' + x for x in all_project_ids_str]
    
  """
  TODO:
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
  
  """

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  project_name_startswith = sys.argv[1] if len(sys.argv) == 2 else 'DCO'
  metadata = Metadata(project_name_startswith)
  
  t = utils.benchmark_w_return_1("get_metadata_info")
  metadata.get_metadata_info()
  utils.benchmark_w_return_2(t, "get_metadata_info")
    
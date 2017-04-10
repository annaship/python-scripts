# from collections import defaultdict
# import time
import util
import MySQLdb
import csv
import sys
from collections import defaultdict

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
    utils.benchmark_w_return_2(t, "get_custom_fields")

    t = utils.benchmark_w_return_1("get_raw_metadata")
    raw_metadata = self.get_raw_metadata(all_project_ids_str)
    # print "RRR"
    # print raw_metadata
    utils.benchmark_w_return_2(t, "get_raw_metadata")
        
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
    
  def make_custom_table_names_list(self, all_project_ids_str):
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
  
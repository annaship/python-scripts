#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import MySQLdb
import csv
import sys
from collections import defaultdict

class RequiredMetadata():
  # find ids by value
  # find and print errors
  # readonly:
  # VAMPS project name
  # VAMPS dataset name
  # abstract
  # Country
  # Longhurst Zone
  # Domain
  # Target gene name
  # DNA region
  # Sequencing method
  # Forward PCR Primer
  # Reverse PCR Primer
  # Index sequence (for Illumina)
  # Adapter sequence
  # Sequencing run date
  
  def __init__(self, fields, content_list, content_dict):
    self.required_metadata_fields_to_update = ["collection_date",
      "env_biome_id",
      "env_feature_id",
      "env_material_id",
      "env_package_id",
      "latitude",
      "longitude"]
    self.required_metadata_fields_to_update_project = ["pi_email",
      "pi_name",
      "project_title",
      "references"]
  
    self.fields = fields
    self.content_list = content_list
    self.content_dict = content_dict
    self.required_metadata_update = defaultdict(dict)
    self.req_field_names_from_db = []
    
    self.get_required_fields()
    
  def put_required_field_names_in_dict(self, dataset_id):
    for f_name in self.req_field_names_from_db:
      self.required_metadata_update[dataset_id][f_name] = ""
    
  def get_required_fields(self):
    #required_metadata_info
    # pass
    req_field_names_t = metadata.get_field_names("required_metadata_info")
    # print req_field_names_t
      
    
    #   print field
    # print "type(req_field_names_from_db)"
    # print type(req_field_names_from_db)
# <type 'tuple'>
    # print list(req_field_names_from_db)
  
    req_field_names_from_db = zip(*req_field_names_t[0])
    print "req_field_names_from_db"
    print req_field_names_from_db

    for d in self.content_dict:
      dataset_id = d['dataset_id']
      self.put_required_field_names_in_dict(dataset_id)

    # print "type(csv_file_fields)"
    # print type(csv_file_fields)
# <type 'list'>

    intersection = list(set(req_field_names_from_db[0]) & set(self.fields))
    # print "\nintersection == "
    # print intersection
    # ['collection_date', 'latitude', 'dataset_id', 'longitude']
  
    for name in intersection:
      for d in self.content_dict:
        dataset_id = d['dataset_id']
        # print "dataset_id"
        # print dataset_id
        for k, v in d.items():
          if k == name:
            # print "k = %s, v = %s" % (k, v)
            self.required_metadata_update[dataset_id][k] = v
          
              
    needed_req_all = list(set(req_field_names_from_db[0]) - set(self.fields))
    # print "\nneeded_req_all == "
    # print needed_req_all
    # ['adapter_sequence_id', 'required_metadata_id', 'geo_loc_name_id', 'run_id', 'created_at', 'dna_region_id', 'updated_at', 'domain_id', 'target_gene_id', 'env_feature_id', 'env_package_id', 'illumina_index_id', 'env_biome_id', 'sequencing_platform_id', 'primer_suite_id', 'env_material_id']

    list_of_fields_rm_id = [field_name.rstrip("_id") for field_name in needed_req_all]
    # for field_name in needed_req_all:
    #   no_id_field = field_name.rstrip("_id")
    #   print "field_name = %s, no_id_field = %s" % (field_name, no_id_field)
    print "list_of_fields_rm_id"
    print list_of_fields_rm_id
  
    intersection_no_id = list(set(list_of_fields_rm_id) & set(self.fields))
    print "intersection_no_id ="
    print intersection_no_id
    # ['illumina_index', 'env_feature', 'domain', 'run', 'adapter_sequence', 'env_package', 'env_biome', 'env_material', 'dna_region', 'target_gene']
  
    req_metadata_from_csv_no_id = defaultdict(dict)
    for name in intersection_no_id:
      for d in self.content_dict:
        dataset_id = d['dataset_id']
        # print "dataset_id"
        # print dataset_id
      
        for k, v in d.items():
          if k == name:
            print "k = %s, v = %s" % (k, v)
            req_metadata_from_csv_no_id[dataset_id][k] = v
            # k = illumina_index, v = unknown
            # k = env_feature, v = aquifer

    # print "req_metadata_from_csv_no_id"
    # print req_metadata_from_csv_no_id
    #{'illumina_index': 'unknown', 'env_feature': 'aquifer', 'domain': 'Bacteria', 'run': '20080709', 'adapter_sequence': 'TGTCA', 'env_package': 'Please choose one', 'env_biome': 'Please choose one', 'env_material': 'water', 'dna_region': 'v3v5', 'target_gene': '16s'}

    # rr = mysql_utils.get_all_name_id("illumina_index")
    # print rr
    #(('AACATC', 45), ('AAGCCT', 71), ...
  
    self.find_id_by_value(req_metadata_from_csv_no_id)

  def find_id_by_value(self, req_metadata_from_csv_no_id):
    for dataset, inner_d in req_metadata_from_csv_no_id.items():   
      print "dataset = %s, inner_d = %s" % (dataset, inner_d)
      for field, val in inner_d.items():    
        print "field = %s, val = %s" % (field, val)
        where_part = "WHERE %s = '%s'" % (field, val)
        field_id_name = field + "_id"
        try:
          res = mysql_utils.get_all_name_id(field, where_part = where_part)
          print "res"
          print res
          if res:
            self.required_metadata_update[dataset][field_id_name] = int(res[0][1])
        except MySQLdb.Error, e:
          utils.print_both("Error %d: %s" % (e.args[0], e.args[1]))
          # def get_all_name_id(self, table_name, id_name = "", field_name = "", where_part = ""):

          if field in ['env_feature', 'env_biome', 'env_material']:
            field_name = "term_name"
            where_part = "WHERE %s = '%s'" % (field_name, val)
            res1 = mysql_utils.get_all_name_id("term", field_name = field_name, where_part = where_part)
            if res1:
              self.required_metadata_update[dataset][field_id_name] = int(res1[0][1])
        except:
          raise

    print "self.required_metadata_update"
    print self.required_metadata_update
    # {'4312': {'illumina_index': 83, 'domain': 3, 'run': 47, 'collection_date': '2007-06-01', 'longitude': '-17.51', 'env_material': 1280, 'latitude': '64.49', 'dna_region': 5, 'dataset_id': '4312', 'target_gene': 1}, 

class Metadata():
  # parse csv
  # separate required from custom
  # find ids by value
  # find and print errors
  
  def __init__(self):
    self.csv_file_fields = []
    self.csv_file_content_list = []
    self.csv_file_content_dict = []
    
    self.get_data_from_csv()
    #TODO: convert csv_file_content into dict
    
    print "csv_file_fields = "
    print self.csv_file_fields
    # ['NPOC', 'access_point_type', 'adapter_sequence', 'alkalinity', 'ammonium', 'bicarbonate', 'env_biome', 'biome_secondary', 'calcium', 'calcium_carbonate', 'chloride', 'clone_library_results', 'collection_date', 'conductivity', 'dataset', 'dataset_id', 'del18O_water', 'depth_in_core', 'depth_subseafloor', 'depth_subterrestrial', 'diss_hydrogen', 'diss_inorg_carb', 'diss_inorg_carbon_del13C', 'diss_org_carb', 'diss_oxygen', 'dna_extraction_meth', 'dna_quantitation', 'dna_region', 'domain', 'elevation', 'env_package', 'enzyme_activities', 'env_feature', 'feature_secondary', 'formation_name', 'forward_primer', 'functional_gene_assays', 'geo_loc_name_continental', 'geo_loc_name_marine', 'illumina_index', 'investigation_type', 'iron', 'iron_II', 'iron_III', 'isol_growth_cond', 'latitude', 'longitude', 'magnesium', 'manganese', 'env_material', 'material_secondary', 'methane', 'methane_del13C', 'microbial_biomass_FISH', 'microbial_biomass_avg_cell_number', 'microbial_biomass_intactpolarlipid', 'microbial_biomass_microscopic', 'microbial_biomass_platecounts', 'microbial_biomass_qPCR', 'nitrate', 'nitrite', 'nitrogen_tot', 'noble_gas_chemistry', 'org_carb_nitro_ratio', 'pH', 'part_org_carbon_del13C', 'phosphate', 'pi_email', 'pi_name', 'plate_counts', 'porosity', 'potassium', 'pressure', 'project', 'project_abstract', 'project_title', 'redox_potential', 'redox_state', 'references', 'resistivity', 'reverse_primer', 'rock_age', 'run', 'salinity', 'samp_store_dur', 'samp_store_temp', 'sample_name', 'sample_size_mass', 'sample_size_vol', 'sample_type', 'sequencing_meth', 'sodium', 'sulfate', 'sulfide', 'sulfur_tot', 'target_gene', 'temperature', 'tot_carb', 'tot_depth_water_col', 'tot_inorg_carb', 'tot_org_carb', 'trace_element_geochem', 'water_age', 'first_name', 'institution', 'last_name', 'public', 'username']
    #
    # print "csv_file_content_list = "
    # print self.csv_file_content_list
    
    
  def get_data_from_csv(self):
    # TODO: get from args
    file_name = "/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_AnnaSh_1501274966258.csv"
    self.csv_file_fields, self.csv_file_content_list = utils.read_csv_into_list(file_name)
    self.csv_file_content_dict = utils.read_csv_into_dict(file_name)

  def get_field_names(self, table_name):
    query = """
      SELECT COLUMN_NAME 
      FROM INFORMATION_SCHEMA.COLUMNS 
      WHERE TABLE_SCHEMA='vamps2' 
          AND TABLE_NAME='%s'; 
    """ % table_name
    # print query
    return mysql_utils.execute_fetch_select(query)

    
  def get_custom_field_names(self):
    pass

class Upload():
  # check if all custom fields are in custom_metadata_fields and custom_metadata_##
  # upload custom data
  # upload required data
  
  def __init__(self):
    pass

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  metadata = Metadata()
  
  metadata.required_metadata = RequiredMetadata(metadata.csv_file_fields, metadata.csv_file_content_list, metadata.csv_file_content_dict)
  
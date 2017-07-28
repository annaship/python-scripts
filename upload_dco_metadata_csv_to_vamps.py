#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import MySQLdb
import csv
import sys
from collections import defaultdict

class Metadata():
  # parse csv
  # separate required from custom
  # find ids by value
  # find and print errors
  
  def __init__(self):
    csv_file_fields, csv_file_content = self.get_data_from_csv()
    #TODO: convert csv_file_content into dict
    
    self.get_required_fields(csv_file_fields)
    # print "csv_file_fields = "
    # print csv_file_fields
    #
    #
    # print "csv_file_content = "
    # print csv_file_content
    
  def get_data_from_csv(self):
    # TODO: get from args
    file_name = "/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_AnnaSh_1501274966258.csv"
    vv = utils.read_csv_into_dict(file_name)
    print "vv"
    print vv
    return utils.read_csv_into_list(file_name)

    
  def get_field_names(self, table_name):
    query = """
      SELECT COLUMN_NAME 
      FROM INFORMATION_SCHEMA.COLUMNS 
      WHERE TABLE_SCHEMA='vamps2' 
          AND TABLE_NAME='%s'; 
    """ % table_name
    # print query
    return mysql_utils.execute_fetch_select(query)
    
  def get_required_fields(self, csv_file_fields):
    #required_metadata_info
    # pass
    req_field_names_t = self.get_field_names("required_metadata_info")
    # print req_field_names_t
    
    # for tup in req_field_names[0]:
      
      
    #   print field
    # print "type(req_field_names)"
    # print type(req_field_names)
# <type 'tuple'>
    # print list(req_field_names)
    
    req_field_names = zip(*req_field_names_t[0])
    # print req_field_names

    # print "type(csv_file_fields)"
    # print type(csv_file_fields)
# <type 'list'>

    intersection = list(set(req_field_names[0]) & set(csv_file_fields))
    # print "\nintersection == "
    # print intersection
    # ['collection_date', 'latitude', 'dataset_id', 'longitude']
    
    needed_req = list(set(req_field_names[0]) - set(csv_file_fields))
    # print "\nneeded_req == "
    # print needed_req
    # ['adapter_sequence_id', 'required_metadata_id', 'geo_loc_name_id', 'run_id', 'created_at', 'dna_region_id', 'updated_at', 'domain_id', 'target_gene_id', 'env_feature_id', 'env_package_id', 'illumina_index_id', 'env_biome_id', 'sequencing_platform_id', 'primer_suite_id', 'env_material_id']
    
    list_of_fields_rm_id = [field_name.rstrip("_id") for field_name in needed_req]
    # for field_name in needed_req:
    #   no_id_field = field_name.rstrip("_id")
    #   print "field_name = %s, no_id_field = %s" % (field_name, no_id_field)
    print list_of_fields_rm_id
    
    intersection_no_id = list(set(list_of_fields_rm_id) & set(csv_file_fields))
    print "intersection_no_id ="
    print intersection_no_id
    # ['illumina_index', 'env_feature', 'domain', 'run', 'adapter_sequence', 'env_package', 'env_biome', 'env_material', 'dna_region', 'target_gene']
    
    rr = mysql_utils.get_all_name_id("illumina_index")
    print rr
    #(('AACATC', 45), ('AAGCCT', 71), ...
    
    
  # def find_id_by_value(self):
    
    
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
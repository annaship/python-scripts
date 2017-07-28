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
    self.csv_file_fields = []
    self.csv_file_content_list = []
    self.csv_file_content_dict = []
    self.required_metadata_update = defaultdict(dict)

    
    self.get_data_from_csv()
    #TODO: convert csv_file_content into dict
    
    self.get_required_fields()
    # print "csv_file_fields = "
    # print csv_file_fields
    #
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
    
  def get_required_fields(self):
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

    intersection = list(set(req_field_names[0]) & set(self.csv_file_fields))
    # print "\nintersection == "
    # print intersection
    # ['collection_date', 'latitude', 'dataset_id', 'longitude']
    
    for name in intersection:
      for d in self.csv_file_content_dict:
        dataset_id = d['dataset_id']
        # print "dataset_id"
        # print dataset_id
        for k, v in d.items():
          if k == name:
            # print "k = %s, v = %s" % (k, v)
            self.required_metadata_update[dataset_id][k] = v
            
                
    needed_req = list(set(req_field_names[0]) - set(self.csv_file_fields))
    # print "\nneeded_req == "
    # print needed_req
    # ['adapter_sequence_id', 'required_metadata_id', 'geo_loc_name_id', 'run_id', 'created_at', 'dna_region_id', 'updated_at', 'domain_id', 'target_gene_id', 'env_feature_id', 'env_package_id', 'illumina_index_id', 'env_biome_id', 'sequencing_platform_id', 'primer_suite_id', 'env_material_id']
    
    list_of_fields_rm_id = [field_name.rstrip("_id") for field_name in needed_req]
    # for field_name in needed_req:
    #   no_id_field = field_name.rstrip("_id")
    #   print "field_name = %s, no_id_field = %s" % (field_name, no_id_field)
    print "list_of_fields_rm_id"
    print list_of_fields_rm_id
    
    intersection_no_id = list(set(list_of_fields_rm_id) & set(self.csv_file_fields))
    print "intersection_no_id ="
    print intersection_no_id
    # ['illumina_index', 'env_feature', 'domain', 'run', 'adapter_sequence', 'env_package', 'env_biome', 'env_material', 'dna_region', 'target_gene']
    
    req_metadata_from_csv_no_id = defaultdict(dict)
    for name in intersection_no_id:
      for d in self.csv_file_content_dict:
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
    # rr = mysql_utils.get_all_name_id("domain", where_part = "WHERE domain = 'Bacteria'")
    # print "rr"
    # print rr
    # (('Bacteria', 3L),)
    
    
  def find_id_by_value(self, req_metadata_from_csv_no_id):
    for dataset, inner_d in req_metadata_from_csv_no_id.items():   
      print "dataset = %s, inner_d = %s" % (dataset, inner_d)
      for field, val in inner_d.items():    
        print "field = %s, val = %s" % (field, val)
        where_part = "WHERE %s = '%s'" % (field, val)
        try:
          res = mysql_utils.get_all_name_id(field, where_part = where_part)
          print "res"
          print res
          if res:
            self.required_metadata_update[dataset][field] = int(res[0][1])
        except MySQLdb.Error, e:
          utils.print_both("Error %d: %s" % (e.args[0], e.args[1]))
          # def get_all_name_id(self, table_name, id_name = "", field_name = "", where_part = ""):

          if field in ['env_feature', 'env_biome', 'env_material']:
            field_name = "term_name"
            where_part = "WHERE %s = '%s'" % (field_name, val)
            res1 = mysql_utils.get_all_name_id("term", field_name = field_name, where_part = where_part)
            if res1:
              self.required_metadata_update[dataset][field] = int(res1[0][1])
        except:
          raise

    print "self.required_metadata_update"
    print self.required_metadata_update
    #{'illumina_index': 83, 'domain': 3, 'dna_region': 5, 'env_material': 1280, 'run': 47, 'target_gene': 1}

    
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
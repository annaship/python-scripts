#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import MySQLdb
import csv
import sys
import argparse
from collections import defaultdict

    
class Metadata():
  # parse csv
  # separate required from custom
  # find ids by value
  # find and print errors
  
  required_metadata_fields_to_update = ['collection_date',
    'env_biome_id',
    'env_feature_id',
    'env_material_id',
    'env_package_id',
    'latitude',
    'longitude']
    
  req_fields_from_csv = ['adapter_sequence',
    'collection_date',
    'dataset',
    'dna_region',
    'domain',
    'env_biome',
    'env_feature',
    'env_material',
    'env_package',
    'forward_primer',
    'illumina_index',
    'latitude',
    'longitude',
    'project',
    'reverse_primer',
    'run',
    'target_gene']
    
  required_fields_to_update_project = ['first_name',
    'institution',
    'last_name',
    'pi_email',
    'pi_name',
    'project_title',
    'public',
    'references',
    'username']
    
  empty_equivalents = ['None', 'undefined', 'Please choose one', '']
  
  field_names_equivalents_csv_db = {'biome_secondary':'env_biome_sec', 
  'feature_secondary':'env_feature_sec', 
  'material_secondary':'env_material_sec',
  'geo_loc_name_continental':'geo_loc_name',
  'dna_extraction_meth': 'DNA_extraction_method'}
    
  not_req_fields_from_csv = []
  csv_file_fields = []
  csv_file_content_list = []
  csv_file_content_dict = []

  def __init__(self, input_file):
    self.get_data_from_csv(input_file)
    Metadata.csv_file_content_dict = self.change_keys_in_csv_content_dict(Metadata.csv_file_content_dict, Metadata.field_names_equivalents_csv_db)

    Metadata.not_req_fields_from_csv = list(set(Metadata.csv_file_fields) - set(Metadata.req_fields_from_csv) - set(Metadata.required_fields_to_update_project))
    print 'Metadata.not_req_fields_from_csv'
    print Metadata.not_req_fields_from_csv
    
    # print 'csv_file_fields = '
    # print Metadata.csv_file_fields
    # ['NPOC', 'access_point_type', 'adapter_sequence', 'alkalinity', 'ammonium', 'bicarbonate', 'env_biome', 'biome_secondary', 'calcium', 'calcium_carbonate', 'chloride', 'clone_library_results', 'collection_date', 'conductivity', 'dataset', 'dataset_id', 'del18O_water', 'depth_in_core', 'depth_subseafloor', 'depth_subterrestrial', 'diss_hydrogen', 'diss_inorg_carb', 'diss_inorg_carbon_del13C', 'diss_org_carb', 'diss_oxygen', 'dna_extraction_meth', 'dna_quantitation', 'dna_region', 'domain', 'elevation', 'env_package', 'enzyme_activities', 'env_feature', 'feature_secondary', 'formation_name', 'forward_primer', 'functional_gene_assays', 'geo_loc_name_continental', 'geo_loc_name_marine', 'illumina_index', 'investigation_type', 'iron', 'iron_II', 'iron_III', 'isol_growth_cond', 'latitude', 'longitude', 'magnesium', 'manganese', 'env_material', 'material_secondary', 'methane', 'methane_del13C', 'microbial_biomass_FISH', 'microbial_biomass_avg_cell_number', 'microbial_biomass_intactpolarlipid', 'microbial_biomass_microscopic', 'microbial_biomass_platecounts', 'microbial_biomass_qPCR', 'nitrate', 'nitrite', 'nitrogen_tot', 'noble_gas_chemistry', 'org_carb_nitro_ratio', 'pH', 'part_org_carbon_del13C', 'phosphate', 'pi_email', 'pi_name', 'plate_counts', 'porosity', 'potassium', 'pressure', 'project', 'project_abstract', 'project_title', 'redox_potential', 'redox_state', 'references', 'resistivity', 'reverse_primer', 'rock_age', 'run', 'salinity', 'samp_store_dur', 'samp_store_temp', 'sample_name', 'sample_size_mass', 'sample_size_vol', 'sample_type', 'sequencing_meth', 'sodium', 'sulfate', 'sulfide', 'sulfur_tot', 'target_gene', 'temperature', 'tot_carb', 'tot_depth_water_col', 'tot_inorg_carb', 'tot_org_carb', 'trace_element_geochem', 'water_age', 'first_name', 'institution', 'last_name', 'public', 'username']
    #
    # print 'csv_file_content_list = '
    # print self.csv_file_content_list
    
    
  def get_data_from_csv(self, input_file):
    # TODO: get from args
    # file_name = '/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_ashipunova_1501347586182.csv'
    Metadata.csv_file_fields, Metadata.csv_file_content_list = utils.read_csv_into_list(input_file)
    Metadata.csv_file_content_dict = utils.read_csv_into_dict(input_file)
    
  def change_keys_in_csv_content_dict(self, arr_of_dictis, key_dict):
    new_format = []
    for old_key, new_key in key_dict.items():
      for dictionary in arr_of_dictis:
        dictionary[new_key] = dictionary[old_key]
        del dictionary[old_key]
        new_format.append(dictionary)        
    return new_format
    

   
class RequiredMetadata(Metadata):
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

  def __init__(self):
    self.fields = Metadata.csv_file_fields
    self.content_list = Metadata.csv_file_content_list
    self.content_dict = Metadata.csv_file_content_dict
    self.required_metadata_update = defaultdict(dict)
    # self.req_field_names_from_db = []
    
    self.get_required_fields()
    
  def put_required_field_names_in_dict(self, dataset_id):
    for f_name in self.required_metadata_fields_to_update:
      self.required_metadata_update[dataset_id][f_name] = ''
    
  def get_required_fields(self):
    #required_metadata_info
    # pass
    # req_field_names_t = metadata.get_field_names('required_metadata_info')
    # print req_field_names_t
      
    
    #   print field
    # print 'type(req_field_names_from_db)'
    # print type(req_field_names_from_db)
    # <type 'tuple'>
    # print list(req_field_names_from_db)
  
    # req_field_names_from_db = zip(*req_field_names_t[0])
    # print 'req_field_names_from_db'
    # print req_field_names_from_db

    for d in self.content_dict:
      dataset_id = d['dataset_id']
      self.put_required_field_names_in_dict(dataset_id)

    # print 'type(csv_file_fields)'
    # print type(csv_file_fields)
    # <type 'list'>

    intersection = list(set(self.required_metadata_fields_to_update) & set(self.fields))
    # print '\nintersection == '
    # print intersection
    # ['collection_date', 'latitude', 'dataset_id', 'longitude']
  
    for name in intersection:
      for d in self.content_dict:
        dataset_id = d['dataset_id']
        # print 'dataset_id'
        # print dataset_id
        for k, v in d.items():
          if k == name:
            # print 'k = %s, v = %s' % (k, v)
            self.required_metadata_update[dataset_id][k] = v
          
              
    needed_req_all = list(set(self.required_metadata_fields_to_update) - set(self.fields))
    # print '\nneeded_req_all == '
    # print needed_req_all
    # ['adapter_sequence_id', 'required_metadata_id', 'geo_loc_name_id', 'run_id', 'created_at', 'dna_region_id', 'updated_at', 'domain_id', 'target_gene_id', 'env_feature_id', 'env_package_id', 'illumina_index_id', 'env_biome_id', 'sequencing_platform_id', 'primer_suite_id', 'env_material_id']

    list_of_fields_rm_id = [field_name.rstrip('_id') for field_name in needed_req_all]
    # for field_name in needed_req_all:
    #   no_id_field = field_name.rstrip('_id')
    #   print 'field_name = %s, no_id_field = %s' % (field_name, no_id_field)
    # print 'list_of_fields_rm_id'
    # print list_of_fields_rm_id
  
    intersection_no_id = list(set(list_of_fields_rm_id) & set(self.fields))
    # print 'intersection_no_id ='
    # print intersection_no_id
    # ['illumina_index', 'env_feature', 'domain', 'run', 'adapter_sequence', 'env_package', 'env_biome', 'env_material', 'dna_region', 'target_gene']
  
    req_metadata_from_csv_no_id = defaultdict(dict)
    for name in intersection_no_id:
      for d in self.content_dict:
        dataset_id = d['dataset_id']
        # print 'dataset_id'
        # print dataset_id
      
        for k, v in d.items():
          if k == name:
            # print 'k = %s, v = %s' % (k, v)
            req_metadata_from_csv_no_id[dataset_id][k] = v
            # k = illumina_index, v = unknown
            # k = env_feature, v = aquifer

    # print 'req_metadata_from_csv_no_id'
    # print req_metadata_from_csv_no_id
    #{'illumina_index': 'unknown', 'env_feature': 'aquifer', 'domain': 'Bacteria', 'run': '20080709', 'adapter_sequence': 'TGTCA', 'env_package': 'Please choose one', 'env_biome': 'Please choose one', 'env_material': 'water', 'dna_region': 'v3v5', 'target_gene': '16s'}

    # rr = mysql_utils.get_all_name_id('illumina_index')
    # print rr
    #(('AACATC', 45), ('AAGCCT', 71), ...
  
    self.find_id_by_value(req_metadata_from_csv_no_id)

  def find_id_by_value(self, req_metadata_from_csv_no_id):
    for dataset, inner_d in req_metadata_from_csv_no_id.items():   
      # print 'dataset = %s, inner_d = %s' % (dataset, inner_d)
      for field, val in inner_d.items():    
        # print 'field = %s, val = %s' % (field, val)
        where_part = 'WHERE %s = "%s"' % (field, val)
        field_id_name = field + '_id'
        try:
          res = mysql_utils.get_all_name_id(field, where_part = where_part)
          # print 'res'
          # print res
          if res:
            self.required_metadata_update[dataset][field_id_name] = int(res[0][1])
        except MySQLdb.Error, e:
          # utils.print_both('Error %d: %s' % (e.args[0], e.args[1]))
          # def get_all_name_id(self, table_name, id_name = '', field_name = '', where_part = ''):

          if field in ['env_feature', 'env_biome', 'env_material', 'env_package']:
            field_name = 'term_name'
            where_part = 'WHERE %s = "%s" or %s = "%s %s"' % (field_name, val, field_name, val, field.lstrip('env_'))
            res1 = mysql_utils.get_all_name_id('term', field_name = field_name, where_part = where_part)
            if res1:
              self.required_metadata_update[dataset][field_id_name] = int(res1[0][1])
        except:
          raise

    print 'self.required_metadata_update'
    print self.required_metadata_update
    # {'4312': {'illumina_index': 83, 'domain': 3, 'run': 47, 'collection_date': '2007-06-01', 'longitude': '-17.51', 'env_material': 1280, 'latitude': '64.49', 'dna_region': 5, 'dataset_id': '4312', 'target_gene': 1}, 

class CustomMetadata(Metadata):
  # get project_id
  # get intersecton of csv and db field names
  # missing column names for custom_metadata_fields
  # missing column names for custom_metadata_#
  # prepare info to update in custom_metadata_#

  def __init__(self):
    self.fields_w_sec = [f if f not in Metadata.field_names_equivalents_csv_db else Metadata.field_names_equivalents_csv_db[f] for f in Metadata.csv_file_fields]

    #   
    # return {k: v for k, v in my_dict.items() if k in key_list}
    # if key in Metadata.field_names_equivalents_csv_db:
    #   key = Metadata.field_names_equivalents_csv_db[key]
    
    self.content_list = Metadata.csv_file_content_list
    self.custom_metadata_update = defaultdict(dict)
    self.fields_to_add_to_db = set()
    

    # self.not_req_fields =
    self.project_id = self.get_project_id()
    # print self.project_id
    self.custom_metadata_table_name = 'custom_metadata_%s' % (str(self.project_id))
    # print 'self.custom_metadata_table_name'
    # print self.custom_metadata_table_name

    self.custom_fields_from_db = self.get_custom_fields_from_db()[0]
    # print 'self.custom_fields_from_db'
    # print self.custom_fields_from_db[0]
    # [0]
    self.custom_fields_from_csv = set(self.fields_w_sec) - set(Metadata.req_fields_from_csv) - set(Metadata.required_fields_to_update_project)
    print 'self.custom_fields_from_csv'
    print self.custom_fields_from_csv
    
    self.diff_db_csv = set(self.custom_fields_from_db) - self.custom_fields_from_csv
    print 'diff_db_csv: set(self.custom_fields_from_db) - self.custom_fields_from_csv'
    print self.diff_db_csv


    # print "type(self.custom_fields_from_csv)"
    # print type(self.custom_fields_from_csv)
    # 
    # print "type(self.custom_fields_from_db)"
    # print type(self.custom_fields_from_db)

    self.diff_csv_db = self.custom_fields_from_csv - set(self.custom_fields_from_db)
    print 'diff_csv_db: set(self.custom_fields_from_csv) - set (self.custom_fields_from_db)'
    print self.diff_csv_db
    
        
    self.get_not_empty_csv_only_fields()

    # self.new_custom_fields = 
    self.populate_custom_data_from_csv()
    
  def get_not_empty_csv_only_fields(self):
    # fields_to_add_to_db = set()
    for d in Metadata.csv_file_content_dict:
      current_dict1 = utils.slicedict(d, self.diff_csv_db)
      for key, val in current_dict1.items():
        if val not in Metadata.empty_equivalents:
          # print 'MMM key = %s, val = %s' % (key, val)
          self.fields_to_add_to_db.add(key)
    print "EEE self.fields_to_add_to_db = "
    print self.fields_to_add_to_db
        
      
    
  def populate_custom_data_from_csv(self):
    
    # print 'type(Metadata.csv_file_content_dict)' list
    # print 'Metadata.csv_file_content_dict'
    # print len(Metadata.csv_file_content_dict) 8
    
    # !!!should be custom_fields_from_db + new fields
    
    for d in Metadata.csv_file_content_dict:
      current_dict = utils.slicedict(d, self.custom_fields_from_db)
      dataset_id = current_dict['dataset_id']
      print 'DDD dataset_id'
      print dataset_id
      
      for key, val in current_dict.items():
        for cust_field in self.custom_fields_from_db:
          # if (cust_field != key) and (val not in Metadata.empty_equivalents):
          #   # print "if (cust_field != key) and (val not in Metadata.empty_equivalents)"
          #   # print 'key = %s, val = %s' % (key, val)
          #   fields_to_add_to_db.add(key) # wrong
          # should be only set(['column_name_1_units_in_row_1', 'project_abstract', 'dna_quantitation'])
          
          if (cust_field == key) and (val not in Metadata.empty_equivalents):
            # print "else"
            # print 'key = %s, val = %s' % (key, val)
            # 
            self.custom_metadata_update[dataset_id][key] = val
          

    print "CCC custom_metadata_update = "
    print self.custom_metadata_update

      # print "fields_to_add_to_db = "
      # print fields_to_add_to_db
      # set(['formation_name', 'env_biome', 'microbial_biomass_FISH', 'pH', 'investigation_type', 'dataset_id', 'target_gene', 'env_feature', 'sample_size_vol', 'samp_store_temp', 'sodium', 'sulfate', 'samp_store_dur', 'sample_name', 'chloride', 'elevation', 'temperature', 'depth_subseafloor', 'depth_subterrestrial', 'isol_growth_cond', 'manganese', 'calcium', 'iron'])
      # TODO: env_feature is not in term?
      
    
    
  # def get_custom_field_names(self):
  #   pass
  def get_project_id(self):
    projects = [d['project'] for d in Metadata.csv_file_content_dict]
    project  = list(set(projects))[0]
    print 'project ='
    print project
    where_part = ('WHERE project = "%s"') % (project)
    project_id = mysql_utils.get_all_name_id('project', where_part = where_part)
    return int(project_id[0][1])
    
  def get_custom_fields_from_db(self):
    custom_metadata_fields_t = mysql_utils.get_field_names('vamps2', self.custom_metadata_table_name)
    return zip(*custom_metadata_fields_t[0])
 

class Upload():
  # check if all custom fields are in custom_metadata_fields and custom_metadata_##
  # upload custom data
  # upload required data
  
  def __init__(self):
    pass

if __name__ == '__main__':
  # ~/BPC/python-scripts$ python upload_dco_metadata_csv_to_vamps.py -f /Users/ashipunova/BPC/vamps-node.js/user_data/vamps2/AnnaSh/metadata-project_DCO_GAI_Bv3v5_AnnaSh_1500930353039.csv 
  
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = 'localhost', db = 'vamps2', read_default_group = 'clienthome')
  else:
    mysql_utils = util.Mysql_util(host = 'vampsdb', db = 'vamps2', read_default_group = 'client')

  parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
      required = True, action = 'store', dest = 'input_file',
      help = '''Input file name''')

  args = parser.parse_args()
  print 'args = '
  print args

  metadata = Metadata(args.input_file)
  required_metadata = RequiredMetadata()
  custom_metadata = CustomMetadata()
  # metadata.required_metadata = RequiredMetadata(metadata.csv_file_fields, metadata.csv_file_content_list, metadata.csv_file_content_dict)
  #
  # metadata.custom_metadata = CustomMetadata(metadata.csv_file_fields, metadata.csv_file_content_list, metadata.csv_file_content_dict)
  
  
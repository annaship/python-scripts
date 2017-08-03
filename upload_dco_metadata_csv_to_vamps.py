#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import MySQLdb
import csv
import sys
import argparse
from collections import defaultdict
# try:
#     # Python 2.6-2.7
#     from HTMLParser import HTMLParser
# except ImportError:
#     # Python 3
#     from html.parser import HTMLParser


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

  csv_fields_with_units = {"FISH_probe_name":"",
    "FISH_probe_seq":"",
    "NPOC":"percent",
    "adapter_sequence":"",
    "alkalinity":"meq/L",
    "ammonium":"µmol/kg",
    "bicarbonate":"µmol/kg",
    "biomass_dry_weight":"gram",
    "biomass_wet_weight":"gram",
    "biome_secondary":"",
    "calcium":"µmol/kg",
    "calcium_carbonate":"percent",
    "chloride":"µmol/kg",
    "clone_library_results":"",
    "collection_date":"YYYY-MM-DD",
    "conductivity":"mS/cm",
    "dataset":"",
    "del18O_water":"parts per mil",
    "depth_subseafloor":"mbsf",
    "depth_subterrestrial":"meter",
    "diss_hydrogen":"µmol/kg",
    "diss_inorg_carb":"µmol/kg",
    "diss_inorg_carbon_del13C":"parts per mil",
    "diss_org_carb":"µmol/kg",
    "diss_oxygen":"µmol/kg",
    "dna_extraction_meth":"",
    "dna_quantitation":"",
    "dna_region":"",
    "domain":"",
    "elevation":"meter",
    "env_biome":"",
    "env_feature":"",
    "env_material":"",
    "env_package":"",
    "enzyme_activities":"",
    "feature_secondary":"",
    "formation_name":"",
    "forward_primer":"",
    "functional_gene_assays":"",
    "geo_loc_name_continental":"",
    "geo_loc_name_marine":"",
    "illumina_index":"",
    "intact_polar_lipid":"pg/g",
    "investigation_type":"",
    "iron":"µmol/kg",
    "iron_II":"µmol/kg",
    "iron_III":"µmol/kg",
    "isol_growth_cond":"PMID:DOI or URL",
    "latitude":"decimal degrees ±90°",
    "longitude":"decimal degrees ±180°",
    "magnesium":"µmol/kg",
    "manganese":"µmol/kg",
    "material_secondary":"",
    "methane":"µmol/kg",
    "methane_del13C":"parts per mil",
    "microbial_biomass_FISH":"cells/g",
    "microbial_biomass_microscopic":"cells/g",
    "microbial_biomass_qPCR":"gene copies",
    "n_acid_for_cell_cnt":"",
    "nitrate":"µmol/kg",
    "nitrite":"µmol/kg",
    "nitrogen_tot":"µmol/kg",
    "noble_gas_chemistry":"",
    "org_carb_nitro_ratio":"",
    "pH":"",
    "part_org_carbon_del13C":"parts per mil",
    "phosphate":"µmol/kg",
    "plate_counts":"CFU/ml",
    "porosity":"percent",
    "potassium":"µmol/kg",
    "pressure":"decibar",
    "project_abstract":"",
    "redox_potential":"millivolt",
    "redox_state":"",
    "resistivity":"ohm-meter",
    "reverse_primer":"",
    "rock_age":"millions of years (Ma)",
    "run":"YYYY-MM-DD",
    "salinity":"PSS-78",
    "samp_store_dur":"days",
    "samp_store_temp":"degrees celsius",
    "sample_collection_device":"",
    "sample_name":"",
    "sample_size_mass":"gram",
    "sample_size_vol":"liter",
    "sample_type":"",
    "sequencing_meth":"",
    "sodium":"µmol/kg",
    "structured comment name":"",
    "sulfate":"µmol/kg",
    "sulfide":"µmol/kg",
    "sulfur_tot":"µmol/kg",
    "target_gene":"",
    "temperature":"degrees celsius",
    "tot_carb":"percent",
    "tot_depth_water_col":"meter",
    "tot_inorg_carb":"percent",
    "tot_org_carb":"percent",
    "trace_element_geochem":"",
    "water_age":"thousands of years (ka)"
    }

  term_equivalents = {'abyssal zone biome':'marine abyssal zone biome',
    'anaerobic':'anaerobic sediment',
    'bathyal biome':'marine bathyal zone biome',
    'benthic biome':'marine benthic biome',
    'biogenous':'biogenous sediment',
    'carbon dioxide-reducing':'carbon dioxide-reducing sediment',
    'colloidal':'colloidal sediment',
    'contaminated':'contaminated sediment',
    'granular':'granular sediment',
    'groundwater':'ground water',
    'hadal zone biome':'marine hadal zone biome',
    'holomictic - fully mixed lake':'holomictic lake',
    'hydrogenous':'hydrogenous sediment',
    'hyperthermophilic':'hyperthermophilic sediment',
    'inorganically contaminated':'inorganically contaminated sediment',
    'iron-reducing':'iron-reducing sediment',
    'manganese-reducing':'manganese-reducing sediment',
    'marine':'marine biome',
    'meromictic - non-mixing lake':'meromictic lake',
    'mesophilic':'mesophilic sediment',
    'misc environment':'miscellaneous_natural_or_artificial_environment',
    'nitrate-reducing':'nitrate-reducing sediment',
    'organically contaminated':'organically contaminated sediment',
    'pelagic biome':'marine pelagic biome',
    'petroleum contaminated':'petroleum contaminated sediment',
    'radioactive':'radioactive sediment',
    'sulphate-reducing':'sulphate-reducing sediment',
    'terrestrial':'terrestrial biome',
    'terrigenous':'terrigenous sediment',
    'vent':'marine hydrothermal vent'}

  empty_equivalents = ['none', 'undefined', 'please choose one', '']

  env_fields = ['env_feature', 'env_biome', 'env_material']

  field_names_equivalents_csv_db = {'biome_secondary':'env_biome_sec',
    'feature_secondary':'env_feature_sec',
    'material_secondary':'env_material_sec',
    'geo_loc_name_continental':'geo_loc_name',
    'dna_extraction_meth': 'DNA_extraction_method'}

  not_req_fields_from_csv = []
  csv_file_fields         = []
  csv_file_content_list   = []
  csv_file_content_dict   = []

  def __init__(self, input_file):
    self.get_data_from_csv(input_file)

    for field in Metadata.csv_file_fields:
      self.get_new_fields_units(field)
      
    # print "MMM0 Metadata.csv_file_fields"
    # print Metadata.csv_file_fields
    #
    # print "MMM1 Metadata.field_names_equivalents_csv_db"
    # print Metadata.field_names_equivalents_csv_db
    #
    # print "MMM2 Metadata.csv_fields_with_units"
    # print Metadata.csv_fields_with_units
    
    Metadata.csv_file_content_dict = self.change_keys_in_csv_content_dict(Metadata.csv_file_content_dict, Metadata.field_names_equivalents_csv_db)
    
    # print "MMM3 Metadata.csv_file_content_dict"
    # print Metadata.csv_file_content_dict

    Metadata.not_req_fields_from_csv = list(set(Metadata.csv_file_fields) - set(Metadata.req_fields_from_csv) - set(Metadata.required_fields_to_update_project))
    # print 'Metadata.not_req_fields_from_csv'
    # print Metadata.not_req_fields_from_csv

    # print 'csv_file_fields = '
    # print Metadata.csv_file_fields
    # ['NPOC', 'access_point_type', 'adapter_sequence', 'alkalinity', 'ammonium', 'bicarbonate', 'env_biome', 'biome_secondary', 'calcium', 'calcium_carbonate', 'chloride', 'clone_library_results', 'collection_date', 'conductivity', 'dataset', 'dataset_id', 'del18O_water', 'depth_in_core', 'depth_subseafloor', 'depth_subterrestrial', 'diss_hydrogen', 'diss_inorg_carb', 'diss_inorg_carbon_del13C', 'diss_org_carb', 'diss_oxygen', 'dna_extraction_meth', 'dna_quantitation', 'dna_region', 'domain', 'elevation', 'env_package', 'enzyme_activities', 'env_feature', 'feature_secondary', 'formation_name', 'forward_primer', 'functional_gene_assays', 'geo_loc_name_continental', 'geo_loc_name_marine', 'illumina_index', 'investigation_type', 'iron', 'iron_II', 'iron_III', 'isol_growth_cond', 'latitude', 'longitude', 'magnesium', 'manganese', 'env_material', 'material_secondary', 'methane', 'methane_del13C', 'microbial_biomass_FISH', 'microbial_biomass_avg_cell_number', 'microbial_biomass_intactpolarlipid', 'microbial_biomass_microscopic', 'microbial_biomass_platecounts', 'microbial_biomass_qPCR', 'nitrate', 'nitrite', 'nitrogen_tot', 'noble_gas_chemistry', 'org_carb_nitro_ratio', 'pH', 'part_org_carbon_del13C', 'phosphate', 'pi_email', 'pi_name', 'plate_counts', 'porosity', 'potassium', 'pressure', 'project', 'project_abstract', 'project_title', 'redox_potential', 'redox_state', 'references', 'resistivity', 'reverse_primer', 'rock_age', 'run', 'salinity', 'samp_store_dur', 'samp_store_temp', 'sample_name', 'sample_size_mass', 'sample_size_vol', 'sample_type', 'sequencing_meth', 'sodium', 'sulfate', 'sulfide', 'sulfur_tot', 'target_gene', 'temperature', 'tot_carb', 'tot_depth_water_col', 'tot_inorg_carb', 'tot_org_carb', 'trace_element_geochem', 'water_age', 'first_name', 'institution', 'last_name', 'public', 'username']
    #
    # print 'csv_file_content_list = '
    # print self.csv_file_content_list
    
  def get_new_fields_units(self, field):
    # print "field"
    # print field
    # field_names_equivalents_csv_db = {'biome_secondary':'env_biome_sec',
    try:
      new_col = field.split('--UNITS--')
      if field != new_col[0]:
        Metadata.field_names_equivalents_csv_db[field] = new_col[0]
        Metadata.csv_fields_with_units[new_col[0]] = new_col[1]
      #TODO: change field to new_col[0] in Metadata.csv_file_fields
    except IndexError:
      pass
    #   new_col = [field, csv_fields_with_units[field]]
    except:
      raise


  def get_data_from_csv(self, input_file):
    # TODO: get from args
    # file_name = '/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_ashipunova_1501347586182.csv'
    Metadata.csv_file_fields, Metadata.csv_file_content_list = utils.read_csv_into_list(input_file)
    Metadata.csv_file_content_dict = utils.read_csv_into_dict(input_file)

  def change_keys_in_csv_content_dict(self, arr_of_dictis, key_dict):
    new_format = []
    for old_key, new_key in key_dict.items():
      if old_key != new_key:
        for dictionary in arr_of_dictis:
          # print 'dictionary = %s' % (dictionary)
        
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

  # check terms
  # UPDATE required_metadata_info_new_view_temp AS base JOIN
  # term AS t2 on(env_biome = term_name)
  # SET base.env_biome_id = t2.term_id
  # query = """UPDATE refids_per_dataset_temp
  #     JOIN new_dataset using(dataset)
  #     SET refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
  # """
  # print query
  # return mysql_utils.execute_no_fetch(query)


  # UPDATE required_metadata_info
  # JOIN dataset USING(dataset_id)
  # JOIN project USING(project_id)
  # SET required_metadata_info.env_biome_id = (SELECT term_id FROM term
  # WHERE term_name = "terrestrial biome")
  # WHERE project = "DCO_TCO_Bv6";
  #

  # update required_metadata_info
  # join env_package using(env_package_id)
  # join dataset using(dataset_id)
  # join project using(project_id)
  # set required_metadata_info.env_package_id = (select env_package_id from env_package where env_package = "water")
  # where env_package = "extreme_habitat"
  # and project in ("DCO_GRA_Bv6v4",
  # "DCO_SYL_Bv6v4",
  # "DCO_BOM_Bv6",
  # "DCO_BOM_Av6");

  # join term on (geo_loc_name_id = term_id)
  # set required_metadata_info.geo_loc_name_id = (select term_id from term where term_name = "CCAL" and ontology_id = 3)


  def __init__(self):
    self.fields = Metadata.csv_file_fields
    self.content_list = Metadata.csv_file_content_list
    self.content_dict = Metadata.csv_file_content_dict
    self.required_metadata_update = defaultdict(dict)
    # self.req_field_names_from_db = []

    self.get_required_fields()

  # def put_required_field_names_in_dict(self, dataset_id):
  #   for f_name in self.required_metadata_fields_to_update:
  #     self.required_metadata_update[dataset_id][f_name] = ''
  #
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
      # self.put_required_field_names_in_dict(dataset_id)

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
          if (k == name) and (v not in Metadata.empty_equivalents):
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

  # TODO: simplify
  def find_id_by_value(self, req_metadata_from_csv_no_id):
    for dataset, inner_d in req_metadata_from_csv_no_id.items():
      # print 'dataset = %s, inner_d = %s' % (dataset, inner_d)
      for field, val in inner_d.items():
        if val.lower() not in Metadata.empty_equivalents:
          try:
            clean_val = Metadata.term_equivalents[val]
          except KeyError:
            clean_val = val
          except:
            raise
            #empty_equivalents
          # print 'FFF field = %s, val = %s, clean_val = %s' % (field, val, clean_val)
          where_part = 'WHERE %s = "%s"' % (field, clean_val)
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
            # if field == 'env_package':
            
            if field in Metadata.env_fields:
              field_name = 'term_name'
              try:
                where_part = 'WHERE %s in ("%s", "%s")' % (field_name, val, clean_val)
              except KeyError:
                where_part = 'WHERE %s = "%s"' % (field_name, clean_val)
              except:
                raise

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
    self.fields_to_add_to_db = defaultdict(dict)

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

    self.diff_csv_db = self.custom_fields_from_csv - set(self.custom_fields_from_db)
    print 'diff_csv_db: set(self.custom_fields_from_csv) - set (self.custom_fields_from_db)'
    print self.diff_csv_db


    self.get_not_empty_csv_only_fields()

    # self.new_custom_fields =
    self.populate_custom_data_from_csv()

  def get_not_empty_csv_only_fields(self):
    for d in Metadata.csv_file_content_dict:
      current_dict1 = utils.slicedict(d, self.diff_csv_db)
      for key, val in current_dict1.items():
        if val.lower() not in Metadata.empty_equivalents:
          self.fields_to_add_to_db[key] = val

  # def get_new_fields_units(self, field):
  #   try:
  #     new_col = field.split('--UNITS--')
  #   except IndexError:
  #     new_col = [field, csv_fields_with_units[field]]
  #   except:
  #     raise
  #   return new_col
    # column_name_1--UNITS--row_1_units1

  # TODO: simplify
  def populate_custom_data_from_csv(self):

    # print 'type(Metadata.csv_file_content_dict)' list
    # print 'Metadata.csv_file_content_dict'
    # print len(Metadata.csv_file_content_dict) 8
    
    all_custom_fields = list(self.custom_fields_from_db) + list(self.fields_to_add_to_db.keys())
    print "AAA all_custom_fields"
    print all_custom_fields
    # html_pars = HTMLParser()

    # print "FFF2 self.fields_to_add_to_db = "
    # print self.fields_to_add_to_db
    for d in Metadata.csv_file_content_dict:
      current_dict = utils.slicedict(d, all_custom_fields)
      dataset_id = current_dict['dataset_id']
      # print 'DDD dataset_id'
      # print dataset_id

      for key, val in current_dict.items():
        for cust_field in all_custom_fields:
          # print 'YYY key = %s, val = %s, cust_field = %s' % (key, val, cust_field)
          if (cust_field == key) and (val.lower() not in Metadata.empty_equivalents):
            # column_name = key
            self.custom_metadata_update[dataset_id][key] = val
            # html_pars.unescape(val)

    # print "CCC custom_metadata_update = "
    # print self.custom_metadata_update
      # set(['formation_name', 'env_biome', 'microbial_biomass_FISH', 'pH', 'investigation_type', 'dataset_id', 'target_gene', 'env_feature', 'sample_size_vol', 'samp_store_temp', 'sodium', 'sulfate', 'samp_store_dur', 'sample_name', 'chloride', 'elevation', 'temperature', 'depth_subseafloor', 'depth_subterrestrial', 'isol_growth_cond', 'manganese', 'calcium', 'iron'])
      # TODO: env_feature is not in term?

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
  # upload required data
  # check if all custom fields are in custom_metadata_fields and custom_metadata_##
  # upload custom data
  # custom 1: alter table custom_metadata_##
  # custom 2: add custom_metadata_fields
  # custom 3: UPDATE custom_metadata_##

  def __init__(self):
    # print "EEE required_metadata_update"
    # print required_metadata_update

    self.update_required_metadata()
    # custom 1
    self.add_fields_to_custom_metadata_table()
    # custom 2
    self.add_fields_to_custom_metadata_fields()
    # custom 3
    self.update_custom_metadata()

  def update_required_metadata(self):
    for dataset_id in required_metadata_update.keys():
      query   = ""
      set_str = ""
      for field_name, field_value in required_metadata_update[dataset_id].items():
        set_str += """required_metadata_info.%s = '%s', """ % (field_name, field_value)
        # print 'field_name = %s, field_value = %s' % (field_name, str(field_value))
      query = """ UPDATE required_metadata_info
                  SET %s
                      updated_at = Now()
                  where dataset_id = '%s'
              """ % (set_str, dataset_id)
      # print "UUU query"
      # print query
      res = mysql_utils.execute_no_fetch(query)
      # print "RRR res"
      # print res

  def add_fields_to_custom_metadata_table(self):
    # QQQ2 = add_fields_to_db_dict
    # {'dna_quantitation': 'PicoGreen', 'project_abstract': 'DCO_GAI_CoDL_Gaidos_15_06_01.pdf,DCO_GAI_Gaidos_CoDL_11_03_03.pdf', 'column_name_1': 'row1 cell 2'})


    for k, v in add_fields_to_db_dict.items():
      query = """ALTER TABLE custom_metadata_%s
                ADD COLUMN `%s` varchar(128) DEFAULT NULL
            """ % (project_id, k)
      print "UUU query"
      print query
      res = mysql_utils.execute_no_fetch(query)
      print "res"
      print res

  def add_fields_to_custom_metadata_fields(self):
    # add_fields_to_db_dict:
    # {'dna_quantitation': 'PicoGreen', 'project_abstract': 'DCO_GAI_CoDL_Gaidos_15_06_01.pdf,DCO_GAI_Gaidos_CoDL_11_03_03.pdf', 'column_name_1': 'row1 cell 2'})

    for k, v in add_fields_to_db_dict.items():
      #96717	307	potassium	nanogram_per_liter	125000
      query = """REPLACE INTO custom_metadata_fields (project_id, field_name, field_units, example) VALUES ('%s', '%s', '%s', '%s')""" % (project_id, k, Metadata.csv_fields_with_units[k].decode('utf-8'), v)
      print "UUU5 query"
      print query
      res = mysql_utils.execute_no_fetch(query)
      print "res"
      print res

  # TODO: combine with update_required_metadata
  def update_custom_metadata(self):
    for dataset_id in custom_metadata_update.keys():    
      table_name = "custom_metadata_" + str(project_id)
      set_str = []
      for field_name, field_value in custom_metadata_update[dataset_id].items():
        set_str.append("%s.%s = '%s'" % (table_name, field_name, field_value))
        # print 'field_name = %s, field_value = %s' % (field_name, str(field_value))
      query = """ UPDATE %s
                  SET %s
                  where dataset_id = '%s'
              """ % (table_name, ', '.join(set_str), dataset_id)
      print "UUU00 query"
      print query
      res = mysql_utils.execute_no_fetch(query)
      print "res"
      print res

  # TODO:
  # custom 1
  # alter table custom_metadata_##
  # add column `env_biome_sec` varchar(128) DEFAULT NULL,

  # custom 2
  # INSERT INTO custom_metadata_fields (project_id, field_name, field_units, example) VALUES ()
  ## UPDATE custom_metadata_fields SET field_name = "temperature" WHERE field_name = "temp" AND project_id = "$1";

  # custom 3
  # UPDATE custom_metadata_110
  # SET env_biome_sec = "subseafloor aquatic biome";



if __name__ == '__main__':
  # ~/BPC/python-scripts$ python upload_dco_metadata_csv_to_vamps.py -f /Users/ashipunova/BPC/vamps-node.js/user_data/vamps2/AnnaSh/metadata-project_DCO_GAI_Bv3v5_AnnaSh_1500930353039.csv

  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = 'localhost', db = 'vamps2', read_default_group = 'clienthome')
  else:
    # mysql_utils = util.Mysql_util(host = 'vampsdb', db = 'vamps2', read_default_group = 'client')
    mysql_utils = util.Mysql_util(host = 'vampsdev', db = 'vamps2', read_default_group = 'client')

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

  required_metadata_update = required_metadata.required_metadata_update

  # add as data to custom_metadata_fields for project_id = ## and as columns to custom_metadata_##
  add_fields_to_db_dict = custom_metadata.fields_to_add_to_db
  # print "FFF6 custom_metadata.fields_to_add_to_db = "
  # print custom_metadata.fields_to_add_to_db
  
  custom_metadata_update = custom_metadata.custom_metadata_update
  project_id = custom_metadata.project_id

  print 'QQQ1 = required_metadata_update'
  print required_metadata_update

  print 'QQQ2 = add_fields_to_db_dict'
  print add_fields_to_db_dict

  print 'QQQ3 = custom_metadata_update'
  print custom_metadata_update

  upload_metadata = Upload()

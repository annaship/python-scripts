#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
try:
    import mysqlclient as mysql
except ImportError:
    try:
        import pymysql as mysql
    except ImportError:
        import MySQLdb as mysql

import argparse
import time
from collections import defaultdict
import re
# try:
#     # Python 2.6-2.7
#     from HTMLParser import HTMLParser
# except ImportError:
#     # Python 3
#     from html.parser import HTMLParser


class Metadata:
  # parse csv
  # separate required from custom
  # find ids by value
  # find and print(errors)

  required_metadata_fields_to_update = ['collection_date',
    'env_biome_id',
    'env_feature_id',
    'env_material_id',
    'env_package_id',
    'geo_loc_name_id',
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

  csv_fields_with_units = {"fish_probe_name":"",
    "fish_probe_seq":"",
    "npoc":"percent",
    "adapt_3letter":"",
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
    "del180_water":"parts per mil",
    "depth_subseafloor":"mbsf",
    "depth_subterrestrial":"meter",
    "diss_hydrogen":"µmol/kg",
    "diss_inorg_carb":"µmol/kg",
    "diss_inorg_carbon_del13c":"parts per mil",
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
    "iron_ii":"µmol/kg",
    "iron_iii":"µmol/kg",
    "isol_growth_cond":"PMID:DOI or URL",
    "latitude":"decimal degrees ±90°",
    "longitude":"decimal degrees ±180°",
    "magnesium":"µmol/kg",
    "manganese":"µmol/kg",
    "material_secondary":"",
    "methane":"µmol/kg",
    "methane_del13c":"parts per mil",
    "microbial_biomass_fish":"cells/g",
    "microbial_biomass_microscopic":"cells/g",
    "microbial_biomass_qpcr":"gene copies",
    "n_acid_for_cell_cnt":"",
    "nitrate":"µmol/kg",
    "nitrite":"µmol/kg",
    "nitrogen_tot":"µmol/kg",
    "noble_gas_chemistry":"",
    "org_carb_nitro_ratio":"",
    "ph":"",
    "part_org_carbon_del13c":"parts per mil",
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

  """
  secondary?
  Hege <> term
  'abyssal zone':'marine abyssal zone biome',
  'bathyal biome':'marine bathyal zone biome',
  'benthic biome':'marine benthic biome',
  'hadal zone biome':'marine hadal zone biome',
  'clastic sedimentary':'clastic sedimentary rock',
  'continental margin biome':'continental margin',
  'pelagic biome':'marine pelagic biome',

  """

# to correct term or to what we have in the form
  # 'abyssal zone biome':'marine abyssal zone biome',
  term_equivalents = {
    'abyssal zone biome':'abyssal zone',
    'anaerobic':'anaerobic sediment',
    'bathyal biome':'bathyal',
    'benthic biome':'benthic',
    'biogenous sedimentary rock':'biogenous sedimentary',
    'biogenous':'biogenous sediment',
    'carbon dioxide-reducing':'carbon dioxide-reducing sediment',
    'clastic sedimentary rock':'clastic sedimentary',
    'colloidal':'colloidal sediment',
    'contaminated':'contaminated sediment',
    'continental margin biome':'continental margin',
    'desert biome':'desert',
    'endolithic biome':'endolithic',
    'estuarine biome':'estuarine',
    'forest biome':'forest',
    'granular':'granular sediment',
    'grassland biome':'grassland',
    'groundwater':'ground water',
    'hadal zone biome':'hadal zone',
    'holomictic - fully mixed lake':'holomictic lake',
    'hydrogenous':'hydrogenous sediment',
    'hyperthermophilic':'hyperthermophilic sediment',
    'igneous rock':'igneous',
    'inorganically contaminated':'inorganically contaminated sediment',
    'iron-reducing':'iron-reducing sediment',
    'manganese-reducing':'manganese-reducing sediment',
    'marine aquatic biome':'marine aquatic',
    'marine':'marine biome',
    'meromictic - non-mixing lake':'meromictic lake',
    'mesophilic':'mesophilic sediment',
    'metamorphic rock':'metamorphic',
    'misc environment':'miscellaneous_natural_or_artificial_environment',
    'montane biome':'montane',
    'neritic zone biome':'neritic zone',
    'nitrate-reducing':'nitrate-reducing sediment',
    'organically contaminated':'organically contaminated sediment',
    'pelagic biome':'pelagic',
    'permafrost biome':'permafrost',
    'petroleum contaminated':'petroleum contaminated sediment',
    'plutonic rock':'plutonic',
    'polar biome':'polar',
    'radioactive':'radioactive sediment',
    'sedimentary rock':'sedimentary',
    'subglacial lake':'subglacial',
    'subseafloor aquatic biome':'subseafloor aquatic',
    'subseafloor biome':'subseafloor',
    'subterrestrial aquatic biome':'subterrestrial aquatic',
    'subterrestrial biome':'subterrestrial',
    'sulphate-reducing':'sulphate-reducing sediment',
    'temperate biome':'temperate',
    'terrestrial aquatic biome':'terrestrial aquatic',
    'terrestrial':'terrestrial biome',
    'terrigenous':'terrigenous sediment',
    'tropical biome':'tropical',
    'tundra biome':'tundra',
    'volcanic rock':'volcanic',
    'vent':'marine hydrothermal vent'}

  empty_equivalents = ['none', 'undefined', 'please choose one', 'unknown', 'null', 'unidentified', 'select...', '']

  term_fields = ['env_feature', 'env_biome', 'env_material', 'geo_loc_name']

  field_names_equivalents_csv_db = {'biome_secondary':'biome_secondary',
    'feature_secondary':'feature_secondary',
    'material_secondary':'material_secondary',
    'geo_loc_name_continental':'geo_loc_name'
    # ,
    # 'dna_extraction_meth': 'DNA_extraction_method'
  }

  not_req_fields_from_csv = []
  csv_file_fields         = []
  csv_file_content_list   = []
  csv_file_content_dict   = []
  not_empty_csv_content_dict = {}

  def __init__(self, input_file):
    self.get_data_from_csv(input_file)

    Metadata.csv_file_fields = Metadata.csv_file_content_list[0]
    for field in Metadata.csv_file_fields:
      if '--UNITS--' in field:
        self.get_new_fields_units(field)

    Metadata.csv_file_fields = self.clean_csv_file_field_names()

    Metadata.not_empty_csv_content_dict = self.check_for_empty_fields()

    self.change_keys_in_csv_content_dict_to_const()
    Metadata.not_empty_csv_content_dict = self.change_keys_in_csv_content_dict_clean_custom(Metadata.not_empty_csv_content_dict)
    Metadata.csv_file_fields = list(Metadata.not_empty_csv_content_dict.keys())
    # check for duplicate field names
    Metadata.not_req_fields_from_csv = list(set(Metadata.csv_file_fields) - set(Metadata.req_fields_from_csv) - set(Metadata.required_fields_to_update_project))

    Metadata.csv_file_content_dict = self.format_not_empty_dict()

  def get_data_from_csv(self, input_file):
    # TODO: get from args
    # file_name = '/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_ashipunova_1501347586182.csv'
    Metadata.csv_file_content_list = utils.read_csv_into_list(input_file)
    Metadata.csv_file_content_dict = utils.read_csv_into_dict(input_file)

  def clean_csv_file_field_names(self):
    res_l = []
    for f in Metadata.csv_file_fields:
        f1 = ''.join([i.lower() if ord(i) < 128 else '_' for i in f])
        f2 = re.sub(r'\W', r'_', f1)
        res_l.append(f2)
    return res_l

  def format_not_empty_dict(self):
      temp_list_of_dict = []
      keys = list(Metadata.not_empty_csv_content_dict.keys())
      transposed_values = list(map(list, zip(*Metadata.not_empty_csv_content_dict.values())))
      for l in transposed_values:
        temp_dict = {}
        for idx, v in enumerate(l):
          key = keys[idx]
          temp_dict[key] = v
        temp_list_of_dict.append(temp_dict)
      return temp_list_of_dict

  def check_for_empty_fields(self):
    removed_fields = []
    clean_matrix = []
    good_fields = []
    transposed_vals = list(map(list, zip(*Metadata.csv_file_content_list[1])))
    for idx, vals_l in enumerate(transposed_vals):
      all_val_for1_field = set(vals_l)
      field_name = Metadata.csv_file_fields[idx]
      if (len(all_val_for1_field) == 1) and list(all_val_for1_field)[0].lower() in Metadata.empty_equivalents:
        removed_fields.append(field_name)
      else:
        good_fields.append(field_name)
        clean_matrix.append(vals_l)
    not_empty_csv_content_dict = dict(zip(good_fields, clean_matrix)) or {}

    return not_empty_csv_content_dict

  # def check_for_duplicate_field_names(self):
  #   all_names_cnt = defaultdict(int)
  #   all_names_dup = defaultdict(list)
  #   for field_name in Metadata.csv_file_fields:
  #     new_name = field_name.replace(".", "_").replace(" ", "_").lower()
  #     all_names_cnt[new_name] += 1
  #     all_names_dup[new_name].append(field_name)
  #   duplicates = [k for k, v in all_names_cnt.items() if v > 1]
  #
  #   return all_names_cnt

  def get_new_fields_units(self, field):
    try:
      new_col = field.split('--UNITS--')
      if field != new_col[0]:
        Metadata.field_names_equivalents_csv_db[field] = new_col[0]
        Metadata.csv_fields_with_units[new_col[0]] = new_col[1]
      #TODO: change field to new_col[0] in Metadata.csv_file_fields
    except IndexError:
      pass

  def change_keys_in_csv_content_dict_to_const(self):
    dictionary = Metadata.not_empty_csv_content_dict
    for old_key, new_key in Metadata.field_names_equivalents_csv_db.items():
      if old_key != new_key:
        try:
          dictionary[new_key] = dictionary[old_key]
          del dictionary[old_key]
        except KeyError:
          pass

  def change_keys_in_csv_content_dict_clean_custom(self, my_dict):
    return {field_name.replace(".", "_").replace(" ", "_").lower(): val
            for field_name, val in my_dict.items()}


class RequiredMetadata(Metadata):
  # find ids by value
  # find and print(errors)
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
  # print(query)
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
    # super().__init__(input_file)
    self.fields = Metadata.csv_file_fields
    # self.content_list = Metadata.csv_file_content_list
    # self.content_dict = Metadata.csv_file_content_dict
    self.required_metadata_update = defaultdict(dict)
    self.fill_required_metadata_update()
    self.get_required_fields()

  def fill_required_metadata_update(self):
    intersection = list(set(self.required_metadata_fields_to_update) & set(self.fields))
    # print(intersection)
    # ['collection_date', 'latitude', 'dataset_id', 'longitude']
    # Metadata.not_empty_csv_content_dict
    for d in Metadata.csv_file_content_dict:
      temp_dict = {}
      dataset_id = d['dataset_id']
      temp_dict = {your_key: d[your_key]
                   for your_key in intersection
                   if d[your_key].lower() not in Metadata.empty_equivalents}
      if any(temp_dict.values()):
        self.required_metadata_update[dataset_id] = temp_dict
    # t2 = time.time()
    # print("Time elapsed 2 = ")
    # print(t2 - t1)

  def get_required_fields(self):
    needed_req_all = list(set(self.required_metadata_fields_to_update) - set(self.fields))
    # print(needed_req_all)
    # ['adapter_sequence_id', 'required_metadata_id', 'geo_loc_name_id', 'run_id', 'created_at', 'dna_region_id', 'updated_at', 'domain_id', 'target_gene_id', 'env_feature_id', 'env_package_id', 'illumina_index_id', 'env_biome_id', 'sequencing_platform_id', 'primer_suite_id', 'env_material_id']

    list_of_fields_rm_id = [field_name.rstrip('_id') for field_name in needed_req_all]

    intersection_no_id = list(set(list_of_fields_rm_id) & set(self.fields))
    # print(intersection_no_id)
    # ['illumina_index', 'env_feature', 'domain', 'run', 'adapter_sequence', 'env_package', 'env_biome', 'env_material', 'dna_region', 'target_gene']

    req_metadata_from_csv_no_id = defaultdict(dict)
    for d in Metadata.csv_file_content_dict:
      dataset_id = d['dataset_id']
      req_metadata_from_csv_no_id[dataset_id] = {your_key: d[your_key]
                                                 for your_key in intersection_no_id}

    # t2 = time.time()
    # print("Time elapsed 2 = ")
    # print(t2 - t1)

    # rr = mysql_utils.get_all_name_id('illumina_index')
    # print(rr)
    #(('AACATC', 45), ('AAGCCT', 71), ...

    self.find_id_by_value(req_metadata_from_csv_no_id)

  # TODO: simplify
  # TODO: use cash, safe _id and look it up
  def find_id_by_value(self, req_metadata_from_csv_no_id):
    for dataset, inner_d in req_metadata_from_csv_no_id.items():
      # print('dataset = %s, inner_d = %s' % (dataset, inner_d))
      for field, val in inner_d.items():
        if val.lower() not in Metadata.empty_equivalents:
          try:
            clean_val = Metadata.term_equivalents[val]
          except KeyError:
            clean_val = val

          where_part = 'WHERE %s = "%s"' % (field, clean_val)
          field_id_name = field + '_id'
          try:
            res = mysql_utils.get_all_name_id(field, where_part = where_part)
            # print('res')
            # print(res)
            if res:
              self.required_metadata_update[dataset][field_id_name] = int(res[0][1])
          except mysql.Error as e:
            # utils.print_both('Error %d: %s' % (e.args[0], e.args[1]))

            if field in Metadata.term_fields:
              field_name = 'term_name'
              try:
                where_part = 'WHERE %s in ("%s", "%s")' % (field_name, val, clean_val)
              except KeyError:
                where_part = 'WHERE %s = "%s"' % (field_name, clean_val)

              res1 = mysql_utils.get_all_name_id('term', field_name = field_name, where_part = where_part)
              if res1:
                self.required_metadata_update[dataset][field_id_name] = int(res1[0][1])
        # else:
        #   self.required_metadata_update[dataset_id][field_id_name] = "None"

    if (is_verbatim):
      print('self.required_metadata_update')
      print(self.required_metadata_update)
    # {'4312': {'illumina_index': 83, 'domain': 3, 'run': 47, 'collection_date': '2007-06-01', 'longitude': '-17.51', 'env_material': 1280, 'latitude': '64.49', 'dna_region': 5, 'dataset_id': '4312', 'target_gene': 1},

class CustomMetadata(Metadata):
  # get project_id
  # get intersecton of csv and db field names
  # missing column names for custom_metadata_fields
  # missing column names for custom_metadata_#
  # prepare info to update in custom_metadata_#

  def __init__(self):
    # super().__init__(input_file)
    self.fields_w_sec = [f if f not in Metadata.field_names_equivalents_csv_db
                         else Metadata.field_names_equivalents_csv_db[f]
                         for f in Metadata.csv_file_fields]

    self.custom_metadata_update = defaultdict(dict)
    self.fields_to_add_to_db = defaultdict(dict)

    self.project_id = self.get_project_id()
    self.custom_metadata_table_name = 'custom_metadata_%s' % (str(self.project_id))

    try:
      self.custom_fields_from_db = self.get_custom_fields_from_db()[0]
    except IndexError:
      self.custom_fields_from_db = []
    self.custom_fields_from_csv = set(self.fields_w_sec) - set(Metadata.req_fields_from_csv) - set(Metadata.required_fields_to_update_project)
    if (is_verbatim):
      print('self.custom_fields_from_csv')
      print(self.custom_fields_from_csv)

    self.diff_db_csv = set(self.custom_fields_from_db) - self.custom_fields_from_csv
    if (is_verbatim):
      print('diff_db_csv: set(self.custom_fields_from_db) - self.custom_fields_from_csv')
      print(self.diff_db_csv)

    self.diff_csv_db = self.custom_fields_from_csv - set(self.custom_fields_from_db)
    if (is_verbatim):
      print('diff_csv_db: set(self.custom_fields_from_csv) - set (self.custom_fields_from_db)')
      print(self.diff_csv_db)

    self.get_not_empty_csv_only_fields()
    self.fields_to_add_to_db = self.change_keys_in_csv_content_dict_clean_custom(self.fields_to_add_to_db)
    self.populate_custom_data_from_csv()

  def get_not_empty_csv_only_fields(self):
    for d in Metadata.csv_file_content_dict:
      current_dict1 = utils.slicedict(d, self.diff_csv_db)
      for key, val in current_dict1.items():
        if val.lower() not in Metadata.empty_equivalents:
          self.fields_to_add_to_db[key] = val

  def clean_users_csv_field_names(self):
    self.fields_to_add_to_db = {field_name.replace(".", "_").replace(" ", "_").lower(): val
                                for field_name, val in self.fields_to_add_to_db.items()}

  def populate_custom_data_from_csv(self):

    # print('type(Metadata.csv_file_content_dict)' list)
    # print('Metadata.csv_file_content_dict')
    # print(len(Metadata.csv_file_content_dict) 8)
    
    all_custom_fields = list(set(list(self.custom_fields_from_db) + list(self.fields_to_add_to_db.keys())))
    if (is_verbatim):
      print("AAA all_custom_fields")
      print(all_custom_fields)

    # print("FFF2 self.fields_to_add_to_db = ")
    # print(self.fields_to_add_to_db)

    for d in Metadata.csv_file_content_dict:
      dataset_id = d['dataset_id']
      temp_keys = list(set(d.keys()) & set(all_custom_fields))
      self.custom_metadata_update[dataset_id] = {your_key: (d[your_key]
                                                            if (d[your_key].lower() not in Metadata.empty_equivalents)
                                                            else "None")
                                                for your_key in temp_keys
      }

    # print("CCC custom_metadata_update  = ")
    # print(self.custom_metadata_update)


      # set(['formation_name', 'env_biome', 'microbial_biomass_FISH', 'pH', 'investigation_type', 'dataset_id', 'target_gene', 'env_feature', 'sample_size_vol', 'samp_store_temp', 'sodium', 'sulfate', 'samp_store_dur', 'sample_name', 'chloride', 'elevation', 'temperature', 'depth_subseafloor', 'depth_subterrestrial', 'isol_growth_cond', 'manganese', 'calcium', 'iron'])
      # TODO: env_feature is not in term?

  def get_project_id(self):
    projects = [d['project'] for d in Metadata.csv_file_content_dict]
    project  = list(set(projects))[0]
    print('project =')
    print(project)
    where_part = 'WHERE project = "%s"' % project
    project_id = mysql_utils.get_all_name_id('project', where_part = where_part)
    return int(project_id[0][1])

  def get_custom_fields_from_db(self):
    custom_metadata_fields_t = mysql_utils.get_field_names('vamps2', self.custom_metadata_table_name)
    return list(zip(*custom_metadata_fields_t[0]))


class Upload:
  # upload required data
  # check if all custom fields are in custom_metadata_fields and custom_metadata_##
  # upload custom data
  # custom 1: alter table custom_metadata_##
  # custom 2: add custom_metadata_fields
  # custom 3: UPDATE custom_metadata_##

  def __init__(self):
    # print("EEE required_metadata_update")
    # print(required_metadata_update)

    self.update_required_metadata()
    # custom 1
    self.add_fields_to_custom_metadata_table()
    # custom 2
    self.add_fields_to_custom_metadata_fields()
    # custom 3
    # insert dataset_id if ot there
    self.insert_dataset_id_custom_metadata()
    # custom 4
    self.update_custom_metadata()

  def update_required_metadata(self):
    for dataset_id in required_metadata_update.keys():
      set_str = ""
      for field_name, field_value in required_metadata_update[dataset_id].items():
        set_str += """required_metadata_info.%s = '%s', """ % (field_name, field_value)
        # print('field_name = %s, field_value = %s' % (field_name, str(field_value)))
      query = """ UPDATE required_metadata_info
                  SET %s
                      updated_at = Now()
                  where dataset_id = '%s'
              """ % (set_str, dataset_id)
      if (is_verbatim):
        print("UUU000 query")
        print(query)
      res = mysql_utils.execute_no_fetch(query)
      if (is_verbatim):
        print("RRR000 res")
        print(res)

  def add_fields_to_custom_metadata_table(self):
    # QQQ2 = add_fields_to_db_dict
    # {'dna_quantitation': 'PicoGreen', 'project_abstract': 'DCO_GAI_CoDL_Gaidos_15_06_01.pdf,DCO_GAI_Gaidos_CoDL_11_03_03.pdf', 'column_name_1': 'row1 cell 2'})

    long_fieds = ["reference", "project_abstract", "project_description"]
    for f in long_fieds:
      query = """ALTER TABLE custom_metadata_%s
                ADD COLUMN `%s` text DEFAULT NULL
            """ % (project_id, f)
      if (is_verbatim):
        print("UUU query")
        print(query)
      res = mysql_utils.execute_no_fetch(query)
      if (is_verbatim):
        print("res")
        print(res)

    for k, v in add_fields_to_db_dict.items():
      query = """ALTER TABLE custom_metadata_%s
                ADD COLUMN `%s` varchar(128) DEFAULT NULL
            """ % (project_id, k)
      if (is_verbatim):
        print("UUU query")
        print(query)
      try:
        res = mysql_utils.execute_no_fetch(query)
      except mysql.InternalError as e:
        print(e)
        continue

        # pymysql.err.InternalError: (1060, "Duplicate column name 'project_abstract'")

      if (is_verbatim):
        print("res")
        print(res)

  def add_fields_to_custom_metadata_fields(self):
    # add_fields_to_db_dict:
    # {'dna_quantitation': 'PicoGreen', 'project_abstract': 'DCO_GAI_CoDL_Gaidos_15_06_01.pdf,DCO_GAI_Gaidos_CoDL_11_03_03.pdf', 'column_name_1': 'row1 cell 2'})

    for k, v in add_fields_to_db_dict.items():
      #96717	307	potassium	nanogram_per_liter	125000
      try:
        field_units = Metadata.csv_fields_with_units[k]
      except KeyError:
        field_units = ""

      notes = ""
      short_value = v
      example_varchar = 128
      if len(v) >= example_varchar:
        short_value = v[:124] + "...";
        notes = "Example was shortened"

      query = """REPLACE INTO custom_metadata_fields (project_id, field_name, field_units, example, notes) VALUES (%s, %s, %s, %s, %s)"""

      values = [project_id, k, field_units, short_value, notes]
      # print("UUU5 query.decode('utf-8')")
      # print(query.decode('utf-8'))
      res = mysql_utils.execute_no_fetch_w_values(query, values)
      if (is_verbatim):
        print("res")
        print(res)

  # TODO: combine with update_required_metadata
  def update_custom_metadata(self):
    for dataset_id in custom_metadata_update.keys():    
      table_name = "custom_metadata_" + str(project_id)
      for field_name, field_value in custom_metadata_update[dataset_id].items():
        query1 = """ UPDATE {}
                    SET {}.{} = %s
                    where dataset_id = %s
                """.format(table_name, table_name, field_name)
        values = [field_value, dataset_id]
        if (is_verbatim):
          print("UUU001 query1")
          print(query1)
          print("UUU001 values")
          print(values)
        res1 = mysql_utils.execute_no_fetch_w_values(query1, values)
        if (is_verbatim):
          print("UUU001 res1")
          print(res1)


  def insert_dataset_id_custom_metadata(self):
    query = "INSERT IGNORE INTO custom_metadata_{} (dataset_id) SELECT dataset_id FROM dataset WHERE project_id = %s;".format(project_id)
    if (is_verbatim):
      print("UUU7 query from insert_dataset_id_custom_metadata")
      print(query)
      print(project_id)
    res = mysql_utils.execute_no_fetch_w_values(query, project_id)
    if (is_verbatim):
      print("res")
      print(res)
    

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

  if utils.is_local() == True:
    mysql_utils = util.Mysql_util(host = 'localhost', db = 'vamps2', read_default_group = 'clienthome')
    print("host = 'localhost', db = 'vamps2'")
  else:
    mysql_utils = util.Mysql_util(host = 'vampsdb', db = 'vamps2', read_default_group = 'client')
    # mysql_utils = util.Mysql_util(host = 'vampsdev', db = 'vamps2', read_default_group = 'client')
    # print("host = 'vampsdev', db = 'vamps2'")
    
  parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
      required = True, action = 'store', dest = 'input_file',
      help = '''Input file name''')
  parser.add_argument("-ve","--verbatim",
    required = False, action = "store_true", dest = "is_verbatim",
    help = """Print an additional inforamtion""")

  args = parser.parse_args()
  print('args = ')
  print(args)

  is_verbatim = args.is_verbatim

  metadata = Metadata(args.input_file)
  required_metadata = RequiredMetadata()
  custom_metadata = CustomMetadata()

  required_metadata_update = required_metadata.required_metadata_update

  # add as data to custom_metadata_fields for project_id = ## and as columns to custom_metadata_##
  add_fields_to_db_dict = custom_metadata.fields_to_add_to_db
  # print("FFF6 custom_metadata.fields_to_add_to_db = ")
  # print(custom_metadata.fields_to_add_to_db)
  
  custom_metadata_update = custom_metadata.custom_metadata_update
  project_id = custom_metadata.project_id

  if (is_verbatim):
    print('QQQ1 = required_metadata_update')
    print(required_metadata_update)

    print('QQQ2 = add_fields_to_db_dict')
    print(add_fields_to_db_dict)

    print('QQQ3 = custom_metadata_update')
    print(custom_metadata_update)

  upload_metadata = Upload()

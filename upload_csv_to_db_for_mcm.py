#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
TODO: add type as a required parameter (photo etc)
"""

import util

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql

import argparse
from collections import defaultdict
import re


class Metadata:
  # parse csv

  metadata_to_field = {
    "Identifier"                 : "identifier",
    "Title"                      : "title",
    "Content"                    : "content",
    "Content URL"                : "content_url",
    "Creator"                    : "creator",
    "Creator.Other"              : "creator_other",
    "Subject.Place"              : "subject_place",
    "Coverage.Lat"               : "coverage_lat",
    "Coverage.Long"              : "coverage_long",
    "Subject.Associated.Places"  : "subject_associated_places",
    "Subject.People"             : "subject_people",
    "Subject.Academic.Field"     : "subject_academic_field",
    "Subject.Other"              : "subject_other",
    "Subject.Season"             : "subject_season",
    "Date.Season"                : "date_season",
    "Date.Season (YYYY)"         : "date_season__yyyy_",
    "Date.Exact"                 : "date_exact",
    "Date.Digital"               : "date_digital",
    "Description"                : "description",
    "Format"                     : "format",
    "Digitization Specifications": "digitization_specifications",
    "Contributor"                : "contributor",
    "Type"                       : "type",
    "Country"                    : "country",
    "Language"                   : "language",
    "Relation"                   : "relation",
    "Source"                     : "source",
    "Publisher"                  : "publisher",
    "Publisher Location"         : "publisher_location",
    "Bibliographic Citation"     : "bibliographic_citation",
    "Rights"                     : "rights"
  }

  # empty_equivalents = ['none', 'undefined', 'please choose one', 'unknown', 'null', 'unidentified', 'select...', '']
  #TODO: mv to init with self
  not_req_fields_from_csv = []
  csv_file_fields = []
  csv_file_content_list = []
  csv_file_content_dict = []
  not_empty_csv_content_dict = {}

  def __init__(self, input_file):
    self.get_data_from_csv(input_file)

    Metadata.csv_file_fields = Metadata.csv_file_content_list[0]
    Metadata.not_empty_csv_content_dict = self.check_for_empty_fields()

    Metadata.not_empty_csv_content_dict = self.change_keys_in_csv_content_dict_clean_custom(
      Metadata.not_empty_csv_content_dict)
    Metadata.csv_file_fields = list(Metadata.not_empty_csv_content_dict.keys())

    Metadata.csv_file_content_dict = self.format_not_empty_dict()
    self.transposed_values = []

  def get_data_from_csv(self, input_file):
    Metadata.csv_file_content_list = utils.read_csv_into_list(input_file, "\t")
    Metadata.csv_file_content_dict = utils.read_csv_into_dict(input_file, "\t")

  def format_not_empty_dict(self):
    temp_list_of_dict = []
    keys = list(Metadata.not_empty_csv_content_dict.keys())
    self.transposed_values = list(map(list, zip(*Metadata.not_empty_csv_content_dict.values())))
    for line in self.transposed_values:
      temp_dict = {}
      for idx, v in enumerate(line):
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
      if len(all_val_for1_field) == 1:
        removed_fields.append(field_name)
      else:
        good_fields.append(field_name)
        clean_matrix.append(vals_l)
    not_empty_csv_content_dict = dict(zip(good_fields, clean_matrix)) or {}

    return not_empty_csv_content_dict

  def change_keys_in_csv_content_dict_clean_custom(self, my_dict):
    return {field_name.replace(".", "_").replace(" ", "_").replace("(", "_").replace(")", "_").lower(): val
            for field_name, val in my_dict.items()}


class Upload:
  table_names_simple = ["subject_academic_field", "country", "data_type", "digitization_specifications", "format",
                        "identifier", "language", "role"]
  table_names_no_f_keys = ["content", "person", "season", "source", "place"]
  table_names_w_ids = ["entry_subject", "entry"]

  tables_comb = {
    "content"      : ["title", "content", "content_url", "description"],
    "entry"        : ["content_id", "country_id", "creator_id", "creator_other_id",
                      "data_type_id", "digitization_specifications_id", "entry_subject_id", "format_id",
                      "language_id", "manual_identifier_ref_id", "person_id", "season_id", "source_id"],
    "entry_subject": ["subject_place_id", "subject_associated_places_id", "subject_people_id",
                      "subject_academic_field_id", "subject_other", "subject_season_id"],
    "person"       : ["first_name", "last_name"],
    # "person_role_ref": ["person_id", "role_id"],
    # "ref": ["role"],
    "season"       : ["date_season", "date_season__yyyy_", "date_exact", "date_digital"], #TODO: rm date_season__yyyy_, use "season"
    "source"       : ["source", "publisher", "publisher_location", "bibliographic_citation", "rights"],
    "place": ["place", "coverage_lat", "coverage_long"],
  }

  where_to_look = {
    "subject_place_id"            : "place",
    "subject_associated_places_id": "place",
    "subject_people_id"           : "person",
    "subject_season_id"           : "season",
    "creator_id"                  : "person",
    "creator_other_id"            : "person",
  }

  foreign_key_tables = defaultdict(dict)

  def __init__(self):
    # print("EEE metadata_update")
    # print(metadata_update)
    self.query_simple_dict = defaultdict()
    self.query_comb_dict = defaultdict()
    self.str_field_by_table_comb = []
    self.data_by_row = []
      # defaultdict()

    self.get_table_foreign_key_names("entry_subject")
    self.get_table_foreign_key_names("entry")
    # self.update_metadata()
    # 0) from transpose upload all data, except ids
    # 1) upload simple tables (table_names_simple)
    # 2) upload combine tables no foreign keys (content, person, place, season, source)
    # 3) get ids
    # 4) upload tables with ids

    self.upload_all_but_ids()
    self.populate_all_simple_tables()
    self.simple_names_present = utils.intersection(Upload.table_names_simple, Metadata.not_empty_csv_content_dict.keys())
    self.update_data_by_row()
    self.upload_simple_tables()
    self.get_info_combine_tables()
    self.upload_combine_tables_no_foreign_keys()
    self.get_ids()
    self.upload_combine_tables_all()
    print("here")

  def get_table_foreign_key_names(self, table_name_to_strip):
    for table_id_name in Upload.tables_comb[table_name_to_strip]:
      if table_id_name.endswith("_id"):
        table_name = re.sub("_id", "", table_id_name)
        try:
          Upload.foreign_key_tables[table_name_to_strip][table_name] = table_id_name
        except:
          table_name = Upload.where_to_look[table_id_name]
          id_name = table_name + "_id"
          where_txt = Metadata.csv_file_content_dict
          id = mysql_utils.get_id(id_name, table_name, where_txt)
          raise

  def upload_all_but_ids(self):

  def populate_all_simple_tables(self):
    for table_name in Upload.table_names_simple:
      val_list = "''"
      mysql_utils.execute_insert(table_name, table_name, val_list, ignore = "IGNORE")

  def upload_simple_tables(self):
    for table_name in self.simple_names_present:
      try:
        val_list = ', '.join('("{0}")'.format(w) for w in set(Metadata.not_empty_csv_content_dict[table_name]))
        insert_query = "INSERT %s INTO %s (%s) VALUES %s" % ('IGNORE', table_name, table_name, val_list)

        mysql_utils.execute_insert(table_name, table_name, val_list, ignore = "IGNORE", sql = insert_query)
      except KeyError:
        pass

  def update_data_by_row(self):
    all_table_names = list(Upload.tables_comb.keys()) + Upload.table_names_simple
    for row_entry_d in Metadata.csv_file_content_dict:
      temp_dict_arr = defaultdict()
      for table_name in all_table_names:
        values = self.get_values(row_entry_d, table_name)
        field_names_for_table = self.get_field_names_per_table(table_name)
        try:
          temp_dict_arr[table_name] = dict(zip(field_names_for_table, values))
        except KeyError:
          table_name = Upload.where_to_look[table_name]
          id_name = table_name + "_id"
          where_txt = Metadata.csv_file_content_dict
          # id = mysql_utils.get_id(id_name, table_name, where_txt)
          temp_dict_arr[table_name] = {}

      self.data_by_row.append(temp_dict_arr)

  def get_field_names_per_table(self, table_name):
    try:
      field_names_for_table = Upload.tables_comb[table_name]
    except KeyError:
      field_names_for_table = [table_name]
    return field_names_for_table

  def get_values(self, d, table_name):
    values = []
    field_names_for_table = self.get_field_names_per_table(table_name)

    for field_name in field_names_for_table:
      try:
        values.append(d[field_name])
      except KeyError:
        values.append("")
    return values

  def get_info_combine_tables(self):
    for d in Metadata.csv_file_content_dict:
      temp_dict_str = defaultdict()
      # temp_dict_arr = defaultdict()
      for table_name in Upload.tables_comb.keys():
        values = self.get_values(d, table_name)
        field_names_for_table = self.get_field_names_per_table(table_name)

        # temp_dict_arr[table_name] = [field_names_for_table, values]

        field_names = ', '.join('{0}'.format(w) for w in field_names_for_table)
        val_list = ', '.join('"{0}"'.format(w) for w in values)
        temp_dict_str[table_name] = (field_names, val_list)

      self.str_field_by_table_comb.append(temp_dict_str)

  def upload_combine_tables_no_foreign_keys(self):
    for ent in self.str_field_by_table_comb:
      for table_name, info in ent.items():
        if table_name in Upload.table_names_no_f_keys:
          field_names = info[0]
          val_list = info[1]
          mysql_utils.execute_insert(table_name, field_names, val_list)

  def get_id_by_csv_val(self):
    where_to_look = {"subject_place_id": "place",
          "subject_associated_places_id": "place",
          "subject_people_id": "person",
          "subject_season_id": "season"}

    # for idx, ent in enumerate(self.data_by_row):
    #   for table_name in table_names_to_get_ids:
    #     id_name = table_name + "_id"
    #     where_parts = []
    #     current_data = ent[table_name]
    #     for field_name, val in current_data.items():
    #       where_parts.append(" {} = '{}' ".format(field_name, val))
    #     where_txt = "WHERE "
    #     where_txt += ' AND '.join(where_parts)
    #     # q = "SELECT {0}_id FROM {0} WHERE {1}".format(table_name, where_txt)
    #     id = mysql_utils.get_id(id_name, table_name, where_txt)
    #     self.data_by_row[idx][table_name][id_name] = id



  def upload_combine_tables_all(self):
    # ["entry_subject", "entry"]
    for idx, ent in enumerate(self.data_by_row):
      for table_name_w_ids, in_dict in Upload.foreign_key_tables.items():
        for field_name_to_fill, id_name_to_fill in in_dict.items():
          """
          get ids by csv val
          "subject_place_id"
          "subject_associated_places_id"
          "subject_people_id"
          "subject_season_id"
          """
          # self.get_id_by_csv_val()
          try:
            current_id = ent[field_name_to_fill][id_name_to_fill]
          except KeyError:
            table_name = Upload.where_to_look[id_name_to_fill]
            field_name = table_name + "_id"

            subject_place_id_value = Metadata.csv_file_content_dict[idx][field_name_to_fill]
            # field_name = "place_id"
            # table_name = "place"
            val_list = "'{}'".format(subject_place_id_value)
            res = mysql_utils.execute_insert(table_name, field_name, val_list)

            if res[0] == 1:
              current_id = res[1]
            else:
              where_part = "WHERE {} = '{}'".format(field_name, subject_place_id_value)
              current_id = mysql_utils.get_id(field_name, table_name, where_part)
              print(current_id)
            # raise
          self.data_by_row[idx][table_name_w_ids][id_name_to_fill] = current_id

        # fields_to_fill = Upload.tables_comb[table_name_w_ids]
        # for table_name, info in ent.items():
        #   # if table_name in Upload.table_names_w_ids:
        #   for field_name in fields_to_fill:
        #     entry_field_names = info[0]
        #     val_list = info[1]
        #     mysql_utils.execute_insert(table_name, entry_field_names, val_list)

  # def print_out_err(self, ):
    # q = 0
    # if table_name == "subject_academic_field":
    #   print("EEE1")
    # q += 1
    # if q == 10:
    #   print("HERE!!!")

  def get_ids(self):
    table_names_to_get_ids = Upload.table_names_no_f_keys + Upload.table_names_simple
    for idx, ent in enumerate(self.data_by_row):
      for table_name in table_names_to_get_ids:
        id_name = table_name + "_id"
        where_parts = []
        current_data = ent[table_name]
        for field_name, val in current_data.items():
          where_parts.append(" {} = '{}' ".format(field_name, val))
        where_txt = "WHERE "
        where_txt += ' AND '.join(where_parts)
        # q = "SELECT {0}_id FROM {0} WHERE {1}".format(table_name, where_txt)
        id = mysql_utils.get_id(id_name, table_name, where_txt)
        self.data_by_row[idx][table_name][id_name] = id


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  utils = util.Utils()

  if utils.is_local() == True:
    mysql_utils = util.Mysql_util(host = 'localhost', db = 'mcm_history', read_default_group = 'clienthome')
    print("host = 'localhost', db = 'mcm_history'")
  else:
    mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = 'mcm_history', read_default_group = 'client')
    print("host = 'taylor.unm.edu', db = 'mcm_history'")

  parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
                      required = True, action = 'store', dest = 'input_file',
                      help = '''Input file name''')
  parser.add_argument("-ve", "--verbatim",
                      required = False, action = "store_true", dest = "is_verbatim",
                      help = """Print an additional inforamtion""")

  args = parser.parse_args()
  print('args = ')
  print(args)

  is_verbatim = args.is_verbatim

  metadata = Metadata(args.input_file)
  upload_metadata = Upload()

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
from itertools import chain


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


  def __init__(self, input_file):
    self.get_data_from_csv(input_file)
    # self.not_req_fields_from_csv = []
    # self.csv_file_fields = []
    # self.csv_file_content_list = []
    # self.csv_file_content_dict = []
    # self.not_empty_csv_content_dict = {}
    self.csv_file_fields = self.csv_file_content_list[0]
    self.not_empty_csv_content_dict = self.check_for_empty_fields()

    self.not_empty_csv_content_dict = self.change_keys_in_csv_content_dict_clean_custom(
      self.not_empty_csv_content_dict)
    self.csv_file_fields = list(self.not_empty_csv_content_dict.keys())

    self.csv_file_content_dict = self.format_not_empty_dict()

  def get_data_from_csv(self, input_file):
    self.csv_file_content_list = utils.read_csv_into_list(input_file, "\t")
    self.csv_file_content_dict = utils.read_csv_into_dict(input_file, "\t")

  def format_not_empty_dict(self):
    temp_list_of_dict = []
    keys = list(self.not_empty_csv_content_dict.keys())
    transposed_values = list(map(list, zip(*self.not_empty_csv_content_dict.values())))
    for line in transposed_values:
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
    transposed_vals = list(map(list, zip(*self.csv_file_content_list[1])))
    for idx, vals_l in enumerate(transposed_vals):
      all_val_for1_field = set(vals_l)
      field_name = self.csv_file_fields[idx]
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
  """
  4 table types (intersect is possible):
  *) table_name equal field_name ("identifier"), see table_names_simple
  *) many field_names correspond to one table_name = field_name ("place": ["subject_associated_places", "subject_place"]}), see many_values_to_one_field
  *) tables with many columns, no foreign keys ("content")
  *) tables with foreign keys, see table_names_w_ids
  """

  csv_field_to_db_field_if_not_the_same = {
    "identifier"                 : "identifier",
    "title"                      : "title",
    "content"                    : "content",
    "content_url"                : "content_url",
    "creator"                    : "person",
    "creator_other"              : "person",
    "subject_place"              : "subject_place",
    "coverage_lat"               : "coverage_lat",
    "coverage_long"              : "coverage_long",
    "subject_associated_places"  : "subject_associated_places",
    "subject_people"             : "person",
    "subject_academic_field"     : "subject_academic_field",
    "subject_other"              : "subject_other",
    "subject_season"             : "season",
    "date_season"                : "season",
    "date_season__yyyy_"         : "season",
    "date_exact"                 : "season",
    "date_digital"               : "season",
    "description"                : "description",
    "format"                     : "format",
    "digitization_specifications": "digitization_specifications",
    "contributor"                : "person",
    "type"                       : "type",
    "country"                    : "country",
    "language"                   : "language",
    "relation"                   : "relation",
    "source"                     : "source",
    "publisher"                  : "publisher",
    "publisher_location"         : "publisher_location",
    "bibliographic_citation"     : "bibliographic_citation",
    "rights"                     : "rights",
  }

  table_names_simple = ["subject_academic_field", "country", "data_type", "digitization_specifications", "format",
                        "identifier", "language", "role"]
  table_names_no_f_keys = ["content", "place"]
  # table_names_no_f_keys = ["content", "person", "season", "source", "place"]
  table_names_w_ids = ["entry", "entry_subject", "source"]
  many_values_to_one_field = {
    "season": ["date_season", "date_season__yyyy_", "date_exact", "date_digital"],
    "person": ["contributor", "creator_other", "subject_people"],
    "place":  ["subject_associated_places", "subject_place"]
  }

  tables_comb = {
    "content"      : ["title", "content", "content_url", "description"],
    "entry"        : ["content_id", "country_id", "creator_id", "creator_other_id",
                      "data_type_id", "digitization_specifications_id", "entry_subject_id", "format_id",
                      "language_id", "manual_identifier_ref_id", "person_id", "season_id", "source_id"],
    "entry_subject": ["subject_place_id", "subject_associated_places_id", "subject_people_id",
                      "subject_academic_field_id", "subject_other", "subject_season_id"],
    # "person"       : ["first_name", "last_name"],
    # "person_role_ref": ["person_id", "role_id"],
    # "ref": ["role"],
    "source"       : ["source", "publisher_id", #person_id
                      "publisher_location_id", #place_id
                      "bibliographic_citation", "rights"],
    "place"        : ["place", "coverage_lat", "coverage_long"],
  }

  where_to_look_if_not_the_same = {
    "bibliographic_citation"   : "source.bibliographic_citation",
    "content_url"              : "content.content_url",
    "contributor"              : "person",
    "creator"                  : "person",
    "creator_other"            : "person",
    "date_digital"             : "season",
    "date_exact"               : "season",
    "date_season"              : "season",
    "date_season__yyyy_"       : "season",
    "description"              : "content.description",
    "publisher_location"       : "place",
    "rights"                   : "source.rights",
    "subject_associated_places": "place",
    "subject_people"           : "person",
    "subject_place"            : "place",
    "subject_season"           : "season",
    "title"                    : "content.title",
    # "content": "content",
    # "country": "country",
    # "coverage_lat": "coverage_lat",
    # "coverage_long": "coverage_long",
    # "digitization_specifications": "digitization_specifications",
    # "format": "format",
    # "identifier": "identifier",
    # "language": "language",
    # "publisher"                : "publisher",
    # "relation": "relation",
    # "source": "source",
    # "subject_academic_field": "subject_academic_field",
    # "subject_other": "subject_other",
    # "type": "type",
  }

  where_to_look_for_id = {
    "subject_place_id"            : "place",
    "subject_associated_places_id": "place",
    "subject_people_id"           : "person",
    "subject_season_id"           : "season",
    "creator_id"                  : "person",
    "creator_other_id"            : "person",
  }

  foreign_key_tables = defaultdict(dict)

  def __init__(self):
    """
        1) upload simple tables (table_names_simple)
        2) upload combine tables no foreign keys (content, person, place, season, source)
        3) get ids
        4) upload tables with ids
    """
    # self.query_simple_dict = defaultdict()
    # self.query_comb_dict = defaultdict()
    # self.data_by_row = []

    # self.get_table_foreign_key_names("entry_subject")
    # self.get_table_foreign_key_names("entry")

    self.upload_all_from_csv_but_id()
    self.make_data_matrix_dict()
    self.get_ids()
    self.update_data_matrix_dict_with_ids()
    self.upload_combine_tables_all()
    print("here")

  # def fill_special_table(self, field_name):
  #   """
  #   Get all info for each row in the table
  #   :return:
  #   """
  #   pass
  #   # try:
  #   #   full_name = self.where_to_look_if_not_the_same[field_name]
  #   #   table_name, field_name = full_name.split(".")
  #   # except:
  #   #   raise

  def upload_all_from_csv_but_id(self):
    self.upload_simple_tables()
    self.upload_many_values_to_one_field()
    self.upload_combine_tables_no_foreign_keys()

  def upload_combine_tables_no_foreign_keys(self):
    str_field_by_table_comb = self.get_info_combine_tables()
    for ent in str_field_by_table_comb:
      for table_name, info in ent.items():
        if table_name in Upload.table_names_no_f_keys:
          field_names = info[0]
          val_list = info[1]
          mysql_utils.execute_insert(table_name, field_names, val_list)

  def simple_mass_upload(self, table_name, field_name, val_str = ""):
    try:
      if val_str == "":
        val_str = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_csv_content_dict[field_name]))
      insert_query = "INSERT %s INTO %s (%s) VALUES %s" % ('IGNORE', table_name, field_name, val_str)

      mysql_utils.execute_insert(table_name, field_name, val_str, ignore = "IGNORE", sql = insert_query)
      print(table_name)
    except KeyError:
      pass

  def upload_simple_tables(self):
    simple_names_present = utils.intersection(Upload.table_names_simple, metadata.not_empty_csv_content_dict.keys())
    for table_name in simple_names_present:
      self.simple_mass_upload(table_name, table_name)

  def upload_many_values_to_one_field(self):
    csv_field_names_to_upload = utils.flatten_2d_list(self.many_values_to_one_field.values())
    value_present = utils.intersection(csv_field_names_to_upload, metadata.not_empty_csv_content_dict.keys())

    for table_name, csv_field_names in self.many_values_to_one_field.items():
      for csv_field_name in csv_field_names:
        if csv_field_name in value_present:
          val_list = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_csv_content_dict[csv_field_name]))
          self.simple_mass_upload(table_name, table_name, val_list)

  def get_db_names_by_csv_field_name(self, csv_field_name):
    if csv_field_name in self.where_to_look_if_not_the_same.keys():
      try:
        (table_name, field_name) = self.where_to_look_if_not_the_same[csv_field_name].split(".") #like "content.content_url"
      except ValueError: # like "person" same name
        table_name = self.where_to_look_if_not_the_same[csv_field_name]
        field_name = table_name
    else:
      table_name = csv_field_name
      field_name = table_name
    return (field_name, table_name)


  def make_data_matrix_dict(self):
    data_matrix = []
    for current_dict in metadata.csv_file_content_dict:
      row = defaultdict()
      for csv_field_name, current_value in current_dict.items():
        (field_name, table_name) = self.get_db_names_by_csv_field_name(csv_field_name)
        where_part = 'WHERE {} = "{}"'.format(field_name, current_value)
        field_name_id = table_name + "_id"
        current_value_id = mysql_utils.get_id(field_name_id, table_name, where_part)
        row[csv_field_name] = current_value_id
    """
        str_field_by_table_comb = []

    for d in metadata.csv_file_content_dict:
      temp_dict_str = defaultdict()
      for table_name in Upload.tables_comb.keys():
        values = self.get_values(d, table_name)
        field_names_for_table = self.get_field_names_per_table(table_name)

        field_names = ', '.join('{0}'.format(w) for w in field_names_for_table)
        val_list = ', '.join('"{0}"'.format(w) for w in values)
        temp_dict_str[table_name] = (field_names, val_list)

      str_field_by_table_comb.append(temp_dict_str)
    return str_field_by_table_comb
    :return:
    """

  def update_data_matrix_dict_with_ids(self):
    pass

  # def update_data_by_row(self):
  #   all_table_names = list(Upload.tables_comb.keys()) + Upload.table_names_simple
  #   for row_entry_d in metadata.csv_file_content_dict:
  #     temp_dict_arr = defaultdict()
  #     for table_name in all_table_names:
  #       values = self.get_values(row_entry_d, table_name)
  #       field_names_for_table = self.get_field_names_per_table(table_name)
  #       try:
  #         temp_dict_arr[table_name] = dict(zip(field_names_for_table, values))
  #       except KeyError:
  #         table_name = Upload.where_to_look[table_name]
  #         id_name = table_name + "_id"
  #         where_txt = metadata.csv_file_content_dict
  #         # id = mysql_utils.get_id(id_name, table_name, where_txt)
  #         temp_dict_arr[table_name] = {}
  #
  #     self.data_by_row.append(temp_dict_arr)

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
    # TODO: check if all got into the dict, even with a "wrong" name
    str_field_by_table_comb = []

    for d in metadata.csv_file_content_dict:
      temp_dict_str = defaultdict()
      for table_name in Upload.tables_comb.keys():
        values = self.get_values(d, table_name)
        field_names_for_table = self.get_field_names_per_table(table_name)

        field_names = ', '.join('{0}'.format(w) for w in field_names_for_table)
        val_list = ', '.join('"{0}"'.format(w) for w in values)
        temp_dict_str[table_name] = (field_names, val_list)

      str_field_by_table_comb.append(temp_dict_str)
    return str_field_by_table_comb

  # def get_id_by_csv_val(self):
  #   where_to_look = {"subject_place_id": "place",
  #         "subject_associated_places_id": "place",
  #         "subject_people_id": "person",
  #         "subject_season_id": "season"}
  #
  #   def get_table_foreign_key_names(self, table_name_to_strip):
  #     for table_id_name in Upload.tables_comb[table_name_to_strip]:
  #       if table_id_name.endswith("_id"):
  #         table_name = re.sub("_id", "", table_id_name)
  #         try:
  #           Upload.foreign_key_tables[table_name_to_strip][table_name] = table_id_name
  #         except:
  #           table_name = Upload.where_to_look[table_id_name]
  #           id_name = table_name + "_id"
  #           where_txt = metadata.csv_file_content_dict
  #           id = mysql_utils.get_id(id_name, table_name, where_txt)
  #           raise
  #   # for idx, ent in enumerate(self.data_by_row):
  #   #   for table_name in table_names_to_get_ids:
  #   #     id_name = table_name + "_id"
  #   #     where_parts = []
  #   #     current_data = ent[table_name]
  #   #     for field_name, val in current_data.items():
  #   #       where_parts.append(" {} = '{}' ".format(field_name, val))
  #   #     where_txt = "WHERE "
  #   #     where_txt += ' AND '.join(where_parts)
  #   #     # q = "SELECT {0}_id FROM {0} WHERE {1}".format(table_name, where_txt)
  #   #     id = mysql_utils.get_id(id_name, table_name, where_txt)
  #   #     self.data_by_row[idx][table_name][id_name] = id

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

            subject_place_id_value = metadata.csv_file_content_dict[idx][field_name_to_fill]
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
        #     val_str = info[1]
        #     mysql_utils.execute_insert(table_name, entry_field_names, val_str)

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

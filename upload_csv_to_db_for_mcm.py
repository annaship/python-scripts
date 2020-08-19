#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
TODO: add type as a required parameter (photo etc)
*) upload the whole csv into one table, separate, add ids
*) whole_tsv_dump should be temporary, clear after each upload
"""
import sys
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
    "Date.Season (YYYY)"         : "date_season_yyyy",
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
    self.tsv_file_fields = self.tsv_file_content_list[0]
    self.transposed_vals = list(map(list, zip(*self.tsv_file_content_list[1])))

    self.not_empty_tsv_content_dict = self.check_for_empty_fields()

    self.not_empty_tsv_content_dict = self.change_keys_in_tsv_content_dict_clean_custom(
      self.not_empty_tsv_content_dict)
    self.tsv_file_fields = list(self.not_empty_tsv_content_dict.keys())

    self.tsv_file_content_dict_no_empty = self.format_not_empty_dict()
    self.check_for_empty_keys()

    self.tsv_file_content_dict_clean_keys = self.clean_keys_in_tsv_file_content_dict()

  def clean_keys_in_tsv_file_content_dict(self):
    res_d = []
    for curr_d in self.tsv_file_content_dict:
      clean_d = self.change_keys_in_tsv_content_dict_clean_custom(curr_d)
      res_d.append(clean_d)
    return res_d

  def check_for_empty_keys(self):
    all_fields = self.tsv_file_content_list[0]
    if "" in all_fields:
      print("ERROR: Column (field names) shouldn't be empty!")
      sys.exit()

  def get_data_from_csv(self, input_file):
    self.tsv_file_content_list = utils.read_csv_into_list(input_file, "\t")
    self.tsv_file_content_dict = utils.read_csv_into_dict(input_file, "\t")

  def format_not_empty_dict(self):
    temp_list_of_dict = []
    keys = list(self.not_empty_tsv_content_dict.keys())
    transposed_values = list(map(list, zip(*self.not_empty_tsv_content_dict.values())))
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
    for idx, vals_l in enumerate(self.transposed_vals):
      all_val_for1_field = set(vals_l)
      field_name = self.tsv_file_fields[idx]
      if any(all_val_for1_field):
        good_fields.append(field_name)
        clean_matrix.append(vals_l)
      else:
        removed_fields.append(field_name)
    not_empty_tsv_content_dict = dict(zip(good_fields, clean_matrix)) or {}

    return not_empty_tsv_content_dict

  def change_keys_in_tsv_content_dict_clean_custom(self, my_dict):
    return {field_name.replace(".", "_").replace(" ", "_").replace("(", "").replace(")", "").lower(): val
            for field_name, val in my_dict.items()}


class Upload:
  """
  table types (intersect is possible):
  *) table_name equal field_name ("identifier")
  *) many field_names correspond to one table_name = field_name ("place": ["subject_associated_places", "subject_place"]}), see many_values_to_one_field
  *) tables with foreign keys, see table_names_w_ids
  """

  # table_names_simple = ["subject_academic_field", "type", "digitization_specifications", "format",
  #                       "identifier", "language", "relation"]
  table_names_w_ids = ["entry"]
  table_name_temp_dump = "whole_tsv_dump"
  many_values_to_one_field = {
    "season": ["date_season", "date_season_yyyy", "date_exact", "date_digital"],
    "person": ["creator", "contributor", "creator_other", "subject_people"],
    "place":  ["subject_associated_places", "subject_place", "country", "publisher_location"]
  }

  where_to_look_if_not_the_same = {
    # "bibliographic_citation"   : "source.bibliographic_citation",
    # "content": "content",
    # "content_url"              : "content.content_url",
    "contributor"                 : "person",
    "country"                     : "place",
    # "coverage_lat": "coverage_lat",
    # "coverage_long": "coverage_long",
    "creator"                     : "person",
    "creator_other"               : "person",
    "date_digital"                : "season",
    "date_exact"                  : "season",
    "date_season"                 : "season",
    "date_season_yyyy"            : "season",
    # "description"              : "content.description",
    # "digitization_specifications": "digitization_specifications",
    # "format": "format",
    # "identifier": "identifier",
    # "language": "language",
    # "publisher"                : "publisher",
    "publisher_location"          : "place",
    # "relation": "relation",
    # "rights"                   : "source.rights",
    # "source": "source",
    "subject_academic_field"      : "subject_academic_field",
    "subject_associated_places"   : "place",
    # "subject_other": "subject_other",
    "subject_people"              : "person",
    "subject_place"               : "place",
    "subject_season"              : "season",
    # "title"                    : "content.title",
    # "type": "type",
  }

  foreign_key_tables = defaultdict(dict)

  def __init__(self):
    """
        1) upload simple tables (table_names_simple)
        2) upload combine tables no foreign keys (content, person, place, season, source)
        3) get ids
        4) upload tables with ids
    """
    self.special_tables = self.get_special_tables()
    self.simple_tables = list(all_tables_set - set(self.special_tables))
    # self.simple_names_present = utils.intersection(self.table_names_simple, metadata.not_empty_tsv_content_dict.keys())

    self.upload_empty()
    self.upload_simple_tables()
    self.upload_all_from_tsv_into_temp_table()
    self.update_simple_ids()

    self.upload_many_values_to_one_field()
    self.update_many_values_to_one_field_ids()

    self.upload_other_tables()
    self.update_other_ids()

    # self.upload_all_from_tsv_but_id()
    # self.make_data_matrix_dict()
    # self.get_ids()
    # self.update_data_matrix_dict_with_ids()
    # self.upload_combine_tables_all()
    print("here")

  def get_special_tables(self):
    special_tables = []
    special_tables.append(self.table_name_temp_dump)
    return special_tables + self.table_names_w_ids + list(self.many_values_to_one_field.keys())
    # ["entry", "person", "place", "season", "whole_tsv_dump"]

  def upload_empty(self):
    for table_name in list(all_tables_set):
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")
      mysql_utils.execute_insert(table_name, table_name, "", sql = insert_query)

  def upload_simple_tables(self):
    for table_name in self.simple_tables:
      self.simple_mass_upload(table_name, table_name)

  def simple_mass_upload(self, table_name, field_name, val_str = ""):
    try:
      if val_str == "":
        val_str = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_tsv_content_dict[field_name]))
      insert_query = "INSERT IGNORE INTO {} ({}) VALUES {}".format(table_name, field_name, val_str)
    except KeyError:
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")

    mysql_utils.execute_insert(table_name, field_name, val_str, ignore = "IGNORE", sql = insert_query)

    # print(table_name)

  def make_field_val_couple_where(self, field_names_arr, values_arr):
    # TODO: confirm that a "title" is unique and use just it to get an id
    couples_arr = ['{} = "{}"'.format(t[0], t[1]) for t in zip(field_names_arr, values_arr)]
    return 'WHERE ' + ' AND '.join(couples_arr)

  def insert_row(self, table_name, field_names_arr, values_arr):
    field_names_str = ', '.join(field_names_arr)
    values_str = ', '.join(['"{}"'.format(e) for e in values_arr])
    mysql_utils.execute_insert(table_name, field_names_str, values_str)


  # def add_id_back(self):

  def upload_all_from_tsv_into_temp_table(self):
    table_name = self.table_name_temp_dump
    table_name_id = table_name + "_id"
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      field_names_arr = list(current_row_d.keys())
      values_arr = list(current_row_d.values())

      # separate as insert_row
      self.insert_row(table_name, field_names_arr, values_arr)

      # separate as add_id_back
      where_part_for_id = self.make_field_val_couple_where(field_names_arr, values_arr)
      current_id = mysql_utils.get_id(table_name_id, table_name, where_part_for_id)
      current_row_d[table_name_id] = current_id

  def update_simple_ids(self):
    table_name_to_update = self.table_name_temp_dump
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      for field_name in self.simple_tables:
        table_name_w_id = field_name
        field_name_id = field_name + "_id"
        where_part = 'WHERE {} = "{}"'.format(field_name, current_row_d[field_name])
        current_id = mysql_utils.get_id(field_name_id, table_name_w_id, where_part)

        table_name_to_update_current_id = current_row_d[table_name_to_update + '_id']
        update_q = "UPDATE {} SET {} = {} WHERE {}_id = {}".format(table_name_to_update, field_name_id, current_id, table_name_to_update, table_name_to_update_current_id)
        mysql_utils.execute_no_fetch(update_q)
      # print("ttt")

  def upload_many_values_to_one_field(self):
    tsv_field_names_to_upload = utils.flatten_2d_list(self.many_values_to_one_field.values())
    value_present = utils.intersection(tsv_field_names_to_upload, metadata.not_empty_tsv_content_dict.keys())

    for table_name, tsv_field_names in self.many_values_to_one_field.items():
      for tsv_field_name in tsv_field_names:
        if tsv_field_name in value_present:
          val_list = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_tsv_content_dict[tsv_field_name]))
          self.simple_mass_upload(table_name, table_name, val_list)

  def update_many_values_to_one_field_ids(self):
    table_name_to_update = self.table_name_temp_dump
    tsv_field_names_to_upload = utils.flatten_2d_list(self.many_values_to_one_field.values())
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      """TODO: go over each table values instead?     
      for table_name, tsv_field_names in self.many_values_to_one_field.items():"""
      for tsv_field_name in tsv_field_names_to_upload:
        try:
          current_value = current_row_d[tsv_field_name]
        except KeyError:
          continue
        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
        where_part = 'WHERE {} = "{}"'.format(table_name_w_id, current_value)
        current_id = mysql_utils.get_id(table_name_w_id + '_id', table_name_w_id, where_part)
        # TODO: update these in columns rather then in rows (all data_exact where == 1976 etc.)
        update_q = 'UPDATE {} SET {} = {} WHERE {} = "{}"'.format(table_name_to_update, tsv_field_name + '_id', current_id, tsv_field_name, current_value)
        mysql_utils.execute_no_fetch(update_q)

  def make_arr_even_if_empty_val(self, field_names_arr, data_dictionary):
    res_arr = []
    for field_name in field_names_arr:
      try:
        val = data_dictionary[field_name]
      except KeyError:
        val = ""
      res_arr.append(val)
    return res_arr

  def upload_other_tables_part_0(self, table_names, current_row_d):
    for table_name in table_names: #ordered_tables_comb_names[0]:
      field_names_arr = self.tables_comb[table_name]
      values_arr = self.make_arr_even_if_empty_val(field_names_arr, current_row_d)
      self.insert_row(table_name, field_names_arr, values_arr)

      # TODO: get_id here and add to temp
      uniq_index_column_name_arr = mysql_utils.get_uniq_index_columns(db_schema, table_name)
      uniq_index_column_val = current_row_d[uniq_index_column_name_arr[0]]
      where_txt_0 = '{} = "{}"'.format(uniq_index_column_name_arr, uniq_index_column_val)
      #self.make_field_val_couple_where(field_names_arr, values_arr)
      new_id = mysql_utils.get_id(table_name + "_id", table_name, where_txt_0)

      #  TODO: update temp table's id

      # field_names_arr_from_temp = []
      # for f in field_names_arr:
      #   if f == uniq_index_column:
      #     res = '{0}.{0}'.format(table_name)
      #   else:
      #     res = f
      #   field_names_arr_from_temp.append(res)
        # [f for f in field_names_arr] # [x if x % 2 else None for x in items]

      # where_txt_1 = "WHERE {} = {}".format(uniq_index_column, current_row_d[uniq_index_column[0]])
      update_q = """UPDATE {}
      SET {} = {} {}""".format(self.table_name_temp_dump, table_name + "_id", new_id, where_txt_0)
      # no "place" 'UPDATE whole_tsv_dump SET place_id = 1 WHERE place = "" AND coverage_lat = "" AND coverage_long = ""'
      mysql_utils.execute_no_fetch(update_q)

  def upload_other_tables_part_1(self, table_names, current_row_d):
    for table_name in table_names:
      field_names_arr = self.tables_comb[table_name]
      values_arr = self.make_arr_even_if_empty_val(field_names_arr, current_row_d)
      for idx, field_name in enumerate(field_names_arr):
        if field_name.endswith("_id"):
          db_field_name_no_id = field_name[:-3]
          table_name_for_id = self.where_to_look_if_not_the_same[db_field_name_no_id]
          val = current_row_d[db_field_name_no_id] or ""
          where_part = 'WHERE {} = "{}"'.format(table_name_for_id, val)
          current_field_id = mysql_utils.get_id(table_name_for_id + "_id", table_name_for_id, where_part)
          values_arr[idx] = current_field_id
      self.insert_row(table_name, field_names_arr, values_arr)

      #       TODO: get id from entry_subject right away?

      # TODO: get_id here and add to temp
      where_txt = self.make_field_val_couple_where(field_names_arr, values_arr)
      new_id = mysql_utils.get_id(table_name + "_id", table_name, where_txt)

      #  TODO: update temp table's id
      update_q = "UPDATE {} SET {} = {} {}".format(self.table_name_temp_dump, table_name + "_id", new_id, where_txt)
      mysql_utils.execute_no_fetch(update_q)

  # def update_temp_table_ids(self):


  def upload_other_tables(self):
    table_name_to_update = self.table_name_temp_dump
    ordered_tables_comb_names = [['content', 'place'], ['source', 'entry_subject'], ['entry']]
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      self.upload_other_tables_part_0(ordered_tables_comb_names[0], current_row_d)
      self.upload_other_tables_part_1(ordered_tables_comb_names[1], current_row_d)
      # self.update_temp_table_ids()
      self.upload_other_tables_part_2(ordered_tables_comb_names[2], current_row_d)

  # def update_id_or_other_tables(self):
  #   ordered_tables_comb_names = [['content', 'source', 'place'], ['entry_subject', 'entry']]
  #   for current_row_d in metadata.tsv_file_content_dict:
  #     where_parts = []
  #     for table_name in ordered_tables_comb_names[0]:
  #       field_names_arr = self.tables_comb[table_name]
  #
  #       for field_name in field_names_arr:
  #         try:
  #           val = current_row_d[field_name]
  #         except KeyError:
  #           val = ""
  #         where_parts.append(" {} = '{}' ".format(field_name, val))
  #       where_txt = "WHERE "
  #       where_txt += ' AND '.join(where_parts)
  #       val_str = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_tsv_content_dict[field_name]))
  #       insert_query = "INSERT %s INTO %s (%s) VALUES %s" % ('IGNORE', table_name, field_name, val_str)


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  utils = util.Utils()

  db_schema = 'mcm_history'

  if utils.is_local() == True:
    mysql_utils = util.Mysql_util(host = 'localhost', db = db_schema, read_default_group = 'clienthome')
    print("host = 'localhost', db = {}".format(db_schema))
  else:
    mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = db_schema, read_default_group = 'client')
    print("host = 'taylor.unm.edu', db {}".format(db_schema))

  all_tables_sql_res = mysql_utils.get_table_names(db_schema)
  all_tables_set = set(utils.extract(all_tables_sql_res[0]))

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

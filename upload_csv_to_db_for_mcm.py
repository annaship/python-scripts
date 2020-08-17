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
  4 table types (intersect is possible):
  *) table_name equal field_name ("identifier"), see table_names_simple
  *) many field_names correspond to one table_name = field_name ("place": ["subject_associated_places", "subject_place"]}), see many_values_to_one_field
  *) tables with many columns, no foreign keys ("content")
  *) tables with foreign keys, see table_names_w_ids
  """

  table_names_simple = ["subject_academic_field", "country", "type", "digitization_specifications", "format",
                        "identifier", "language", "relation"] #, "role"
  table_names_no_f_keys = ["content", "place"]
  # table_names_no_f_keys = ["content", "person", "season", "source", "place"]
  table_names_w_ids = ["entry", "entry_subject", "source"]
  many_values_to_one_field = {
    "season": ["date_season", "date_season_yyyy", "date_exact", "date_digital"],
    "person": ["creator", "contributor", "creator_other", "subject_people"],
    "place":  ["subject_associated_places", "subject_place", "country", "publisher_location"]
  }

  tables_comb = {
    "content"      : ["title", "content", "content_url", "description"],
    "entry"        : ["content_id", "country_id", "creator_id", "creator_other_id",
                      "type_id", "digitization_specifications_id", "entry_subject_id", "format_id",
                      "language_id", "manual_identifier_ref_id", "source_id", "date_season_id", "date_season_yyyy_id", "date_exact_id", "date_digital_id", "contributor_id"],
    "entry_subject": ["subject_place_id", "subject_associated_places_id", "subject_people_id",
                      "subject_academic_field_id", "subject_other", "subject_season_id"],
    # "person"       : ["first_name", "last_name"],
    # "person_role_ref": ["person_id", "role_id"],
    # "ref": ["role"],
    "source"       : ["source", "publisher", #person_id
                      "publisher_location_id", #place_id
                      "bibliographic_citation", "rights"],
    "place"        : ["place", "coverage_lat", "coverage_long"],
  }

  where_to_look_if_not_the_same = {
    # "bibliographic_citation"   : "source.bibliographic_citation",
    # "content_url"              : "content.content_url",
    "contributor"              : "person",
    "creator"                  : "person",
    "creator_other"            : "person",
    "date_digital"             : "season",
    "date_exact"               : "season",
    "date_season"              : "season",
    "date_season_yyyy"         : "season",
    # "description"              : "content.description",
    "publisher_location"       : "place",
    # "rights"                   : "source.rights",
    "subject_associated_places": "place",
    "subject_people"           : "person",
    "subject_place"            : "place",
    "subject_season"           : "season",
    # "title"                    : "content.title",
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
    "subject_academic_field": "subject_academic_field",
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
    self.table_name_temp_dump = "whole_tsv_dump"
    self.simple_names_present = utils.intersection(self.table_names_simple, metadata.not_empty_tsv_content_dict.keys())

    self.upload_simple_tables()
    self.upload_all_from_tsv_into_temp_table()
    self.update_simple_ids()

    self.upload_many_values_to_one_field()
    # self.update_many_values_to_one_field_ids()

    self.upload_other_tables()
    self.update_other_ids()

    # self.upload_all_from_tsv_but_id()
    # self.make_data_matrix_dict()
    # self.get_ids()
    # self.update_data_matrix_dict_with_ids()
    # self.upload_combine_tables_all()
    print("here")

  def upload_simple_tables(self):
    for table_name in self.simple_names_present:
      self.simple_mass_upload(table_name, table_name)

  def simple_mass_upload(self, table_name, field_name, val_str = ""):
    try:
      if val_str == "":
        val_str = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_tsv_content_dict[field_name]))
      insert_query = "INSERT %s INTO %s (%s) VALUES %s" % ('IGNORE', table_name, field_name, val_str)

      mysql_utils.execute_insert(table_name, field_name, val_str, ignore = "IGNORE", sql = insert_query)
      print(table_name)
    except KeyError:
      pass

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
    for current_row_d in metadata.tsv_file_content_dict_no_empty:
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
    for current_row_d in metadata.tsv_file_content_dict_no_empty:
      for field_name in self.simple_names_present:
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
      table_name_to_update_current_id = current_row_d[table_name_to_update + '_id']

      for tsv_field_name in tsv_field_names_to_upload:
        try:
          current_value = current_row_d[tsv_field_name]
        except KeyError:
          continue
        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
        where_part = 'WHERE {} = "{}"'.format(table_name_w_id, current_value)
        current_id = mysql_utils.get_id(table_name_w_id + "_id", table_name_w_id, where_part)
        # TODO: update these in columns rather then in rows (all data_exact where == 1976 etc.)
        update_q = "UPDATE {} SET {} = {} WHERE {}_id = {}".format(table_name_to_update, tsv_field_name + "_id", current_id, table_name_to_update, table_name_to_update_current_id)
        mysql_utils.execute_no_fetch(update_q)

      print("ttt")

  def make_arr_even_if_empty_val(self, field_names_arr, data_dictionary):
    res_arr = []
    for field_name in field_names_arr:
      try:
        val = data_dictionary[field_name]
      except KeyError:
        val = ""
      res_arr.append(val)
    return res_arr

  def upload_other_tables_1(self, table_names, current_row_d):
    for table_name in table_names: #ordered_tables_comb_names[0]:
      field_names_arr = self.tables_comb[table_name]
      values_arr = self.make_arr_even_if_empty_val(field_names_arr, current_row_d)
      self.insert_row(table_name, field_names_arr, values_arr)

      # TODO: get_id here and add to temp
      where_txt = self.make_field_val_couple_where(field_names_arr, values_arr)
      new_id = mysql_utils.get_id(table_name + "_id", table_name, where_txt)

      #  TODO: update temp table sid
      update_q = "UPDATE {} SET {} = {} {}".format(self.table_name_temp_dump, table_name + "_id", new_id, where_txt)
      mysql_utils.execute_no_fetch(update_q)

  def upload_other_tables(self):
    table_name_to_update = self.table_name_temp_dump
    ordered_tables_comb_names = [['content', 'place'], ['source', 'entry_subject'], ['entry']]
    for current_row_d in metadata.tsv_file_content_dict_clean_keys:
      self.upload_other_tables_1(ordered_tables_comb_names[0], current_row_d)
      for table_name in ordered_tables_comb_names[1]:
        field_names_arr = self.tables_comb[table_name]
        values_arr = self.make_arr_even_if_empty_val(field_names_arr, current_row_d)
        for idx, field_name in enumerate(field_names_arr):
          if field_name.endswith("_id"):
            db_field_name_no_id = field_name[:-3]
            table_name_for_id = self.where_to_look_if_not_the_same[db_field_name_no_id]
            if db_field_name_no_id == "subject_academic_field":
              print("EEE")
            val = current_row_d[db_field_name_no_id] or ""
            # KeyError: 'subject_people'
            where_part = 'WHERE {} = "{}"'.format(table_name_for_id, val)
            # 'SELECT publisher_location_id FROM source WHERE place = "US"'
            current_field_id = mysql_utils.get_id(table_name_for_id + "_id", table_name_for_id, where_part)
            values_arr[idx] = current_field_id
        self.insert_row(table_name, field_names_arr, values_arr)

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


# def upload_all_from_tsv_but_id(self):
  #   self.upload_simple_tables()
  #   self.upload_many_values_to_one_field()
  #   self.upload_combine_tables_no_foreign_keys()

  # def upload_combine_tables_no_foreign_keys(self):
  #   str_field_by_table_comb = self.get_info_combine_tables()
  #   for ent in str_field_by_table_comb:
  #     for table_name, info in ent.items():
  #       if table_name in Upload.table_names_no_f_keys:
  #         field_names = info[0]
  #         val_list = info[1]
  #         mysql_utils.execute_insert(table_name, field_names, val_list)

  # def add_data_toCOmb_tables(self):
  #
  # def update_other_ids(self):
  #   ordered_tables_comb_names = ['content', 'source', 'place', 'entry_subject', 'entry']
  #   table_name_to_update = self.table_name_temp_dump
  #   for current_row_d in metadata.tsv_file_content_dict:
  #     for table_comb_name in ordered_tables_comb_names:
  #       field_names = self.tables_comb[table_comb_name]
  #       # for field_name in field_names:
  #       self.make_where_and_query(current_row_d)
  #       #   {k:d[k] for k in l if k in d}
  #
  #
  # def make_where_and_query(self, current_data_dict):
  #   where_parts = []
  #   for field_name, val in current_data_dict.items():
  #     if field_name in
  #     where_parts.append(" {} = '{}' ".format(field_name, val))
  #   where_txt = "WHERE "
  #   where_txt += ' AND '.join(where_parts)
  #   # q = "SELECT {0}_id FROM {0} WHERE {1}".format(table_name, where_txt)
  #   # id = mysql_utils.get_id(id_name, table_name, where_txt)
  # #   {k:d[k] for k in current_data_dict.keys() if k in d}
  #


  # def upload_many_values_to_one_field(self):
  #   tsv_field_names_to_upload = utils.flatten_2d_list(self.many_values_to_one_field.values())
  #   value_present = utils.intersection(tsv_field_names_to_upload, metadata.not_empty_tsv_content_dict.keys())
  #
  #   for table_name, tsv_field_names in self.many_values_to_one_field.items():
  #     for tsv_field_name in tsv_field_names:
  #       if tsv_field_name in value_present:
  #         val_list = ', '.join('("{0}")'.format(w) for w in set(metadata.not_empty_tsv_content_dict[tsv_field_name]))
  #         self.simple_mass_upload(table_name, table_name, val_list)

  # def get_db_names_by_tsv_field_name(self, tsv_field_name):
  #   if tsv_field_name in self.where_to_look_if_not_the_same.keys():
  #     try:
  #       (table_name, field_name) = self.where_to_look_if_not_the_same[tsv_field_name].split(".") #like "content.content_url"
  #     except ValueError: # like "person" same name
  #       table_name = self.where_to_look_if_not_the_same[tsv_field_name]
  #       field_name = table_name
  #   else:
  #     table_name = tsv_field_name
  #     field_name = table_name
  #   return (field_name, table_name)

  # def get_all_sql_queries_for_ids(self):
  #   # TODO: deal with it:
  #   db_only_field_names = ["manual_identifier_ref_id", "entry_subject_id"]
  #   """ 1) through combined tables
  #       # TODO: WHERE should be by table, i.e "where publisher = 'American Geophysical Union Transactions' AND 'publisher_location' = US"
  #
  #       2) the rest
  #       3) "entry" with all the ids
  #   """
  #   all_sql_queries_for_ids = []
  #   for idx, current_dict in enumerate(metadata.tsv_file_content_dict):
  #     all_sql_queries_for_ids_for_row = defaultdict(lambda : defaultdict(list))
  #     row = defaultdict()
  #     tsv_field_name = ""
  #     where_part_arr = []
  #     # 1) through combined tables, except "entry"
  #     #  then do it again for "entry" with ids
  #     for table_name, field_names in self.tables_comb.items():
  #       use_names = list(set(field_names) - set(db_only_field_names)) + self.table_names_simple
  #       for field_name in use_names:
  #         tsv_field_name = field_name
  #         if field_name.endswith("_id"):
  #           tsv_field_name = field_name[:-3]
  #           """TODO: look up foreign key instead of just stripping"""
  #         #   KeyError: 'date_season_yyyy'
  #         try:
  #           current_value = current_dict[tsv_field_name]
  #         except KeyError:
  #           # temp:
  #           if tsv_field_name in ["subject_associated_places", "place", "identifier"]:
  #             pass
  #           else:
  #             raise
  #         where_part = '{} = "{}"'.format(field_name, current_value)
  #         where_part_arr.append(where_part)
  #       where_part_and = " AND ".join(where_part_arr)
  #       q = "SELECT {}_id FROM {} WHERE {}".format(table_name, table_name, where_part_and)
  #       print("QQQ")
  #       print(q)
  #       all_sql_queries_for_ids_for_row[idx][table_name].append(q)
  #     all_sql_queries_for_ids.append(all_sql_queries_for_ids_for_row)
  #
  #     # for tsv_field_name, current_value in current_dict.items():
  #     #   (field_name, table_name) = self.get_db_names_by_tsv_field_name(tsv_field_name)
  #     #   where_part = 'WHERE {} = "{}"'.format(field_name, current_value)
  #     #   field_name_id = table_name + "_id"
  #     #   current_value_id = mysql_utils.get_id(field_name_id, table_name, where_part)
  #     #   row[tsv_field_name].append(current_value_id)

  # def make_data_matrix_dict(self):
  #   self.get_all_sql_queries_for_ids()
  #   data_matrix = []
  #   for current_dict in metadata.tsv_file_content_dict:
  #     row = defaultdict()
  #     self.combine_fields_by_table()
  #     # 1) throw combined tables
  #     #
  #     for tsv_field_name, current_value in current_dict.items():
  #       (field_name, table_name) = self.get_db_names_by_tsv_field_name(tsv_field_name)
  #       where_part = 'WHERE {} = "{}"'.format(field_name, current_value)
  #       # TODO: WHERE should be by table, i.e "where publisher = 'American Geophysical Union Transactions' AND 'publisher_location' = US"
  #       field_name_id = table_name + "_id"
  #       current_value_id = mysql_utils.get_id(field_name_id, table_name, where_part)
  #       row[tsv_field_name] = current_value_id
  #   """
  #       str_field_by_table_comb = []
  #
  #   for d in metadata.tsv_file_content_dict:
  #     temp_dict_str = defaultdict()
  #     for table_name in Upload.tables_comb.keys():
  #       values = self.get_values(d, table_name)
  #       field_names_for_table = self.get_field_names_per_table(table_name)
  #
  #       field_names = ', '.join('{0}'.format(w) for w in field_names_for_table)
  #       val_list = ', '.join('"{0}"'.format(w) for w in values)
  #       temp_dict_str[table_name] = (field_names, val_list)
  #
  #     str_field_by_table_comb.append(temp_dict_str)
  #   return str_field_by_table_comb
  #   :return:
  #   """

  # def update_data_matrix_dict_with_ids(self):
  #   pass

  # def update_data_by_row(self):
  #   all_table_names = list(Upload.tables_comb.keys()) + Upload.table_names_simple
  #   for row_entry_d in metadata.tsv_file_content_dict:
  #     temp_dict_arr = defaultdict()
  #     for table_name in all_table_names:
  #       values = self.get_values(row_entry_d, table_name)
  #       field_names_for_table = self.get_field_names_per_table(table_name)
  #       try:
  #         temp_dict_arr[table_name] = dict(zip(field_names_for_table, values))
  #       except KeyError:
  #         table_name = Upload.where_to_look[table_name]
  #         id_name = table_name + "_id"
  #         where_txt = metadata.tsv_file_content_dict
  #         # id = mysql_utils.get_id(id_name, table_name, where_txt)
  #         temp_dict_arr[table_name] = {}
  #
  #     self.data_by_row.append(temp_dict_arr)

  # def get_field_names_per_table(self, table_name):
  #   try:
  #     field_names_for_table = Upload.tables_comb[table_name]
  #   except KeyError:
  #     field_names_for_table = [table_name]
  #   return field_names_for_table

  # def get_values(self, d, table_name):
  #   values = []
  #   field_names_for_table = self.get_field_names_per_table(table_name)
  #
  #   for field_name in field_names_for_table:
  #     try:
  #       values.append(d[field_name])
  #     except KeyError:
  #       values.append("")
  #   return values

  # def get_info_combine_tables(self):
  #   # TODO: check if all got into the dict, even with a "wrong" name
  #   str_field_by_table_comb = []
  #
  #   for d in metadata.tsv_file_content_dict:
  #     temp_dict_str = defaultdict()
  #     for table_name in Upload.tables_comb.keys():
  #       values = self.get_values(d, table_name)
  #       field_names_for_table = self.get_field_names_per_table(table_name)
  #
  #       field_names = ', '.join('{0}'.format(w) for w in field_names_for_table)
  #       val_list = ', '.join('"{0}"'.format(w) for w in values)
  #       temp_dict_str[table_name] = (field_names, val_list)
  #
  #     str_field_by_table_comb.append(temp_dict_str)
  #   return str_field_by_table_comb

  # def get_id_by_tsv_val(self):
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
  #           where_txt = metadata.tsv_file_content_dict
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

  # def upload_combine_tables_all(self):
  #   # ["entry_subject", "entry"]
  #   for idx, ent in enumerate(self.data_by_row):
  #     for table_name_w_ids, in_dict in Upload.foreign_key_tables.items():
  #       for field_name_to_fill, id_name_to_fill in in_dict.items():
  #         """
  #         get ids by csv val
  #         "subject_place_id"
  #         "subject_associated_places_id"
  #         "subject_people_id"
  #         "subject_season_id"
  #         """
  #         # self.get_id_by_tsv_val()
  #         try:
  #           current_id = ent[field_name_to_fill][id_name_to_fill]
  #         except KeyError:
  #           table_name = Upload.where_to_look[id_name_to_fill]
  #           field_name = table_name + "_id"
  #
  #           subject_place_id_value = metadata.tsv_file_content_dict[idx][field_name_to_fill]
  #           # field_name = "place_id"
  #           # table_name = "place"
  #           val_list = "'{}'".format(subject_place_id_value)
  #           res = mysql_utils.execute_insert(table_name, field_name, val_list)
  #
  #           if res[0] == 1:
  #             current_id = res[1]
  #           else:
  #             where_part = "WHERE {} = '{}'".format(field_name, subject_place_id_value)
  #             current_id = mysql_utils.get_id(field_name, table_name, where_part)
  #             print(current_id)
  #           # raise
  #         self.data_by_row[idx][table_name_w_ids][id_name_to_fill] = current_id
  #
  #       # fields_to_fill = Upload.tables_comb[table_name_w_ids]
  #       # for table_name, info in ent.items():
  #       #   # if table_name in Upload.table_names_w_ids:
  #       #   for field_name in fields_to_fill:
  #       #     entry_field_names = info[0]
  #       #     val_str = info[1]
  #       #     mysql_utils.execute_insert(table_name, entry_field_names, val_str)

  # def print_out_err(self, ):
    # q = 0
    # if table_name == "subject_academic_field":
    #   print("EEE1")
    # q += 1
    # if q == 10:
    #   print("HERE!!!")

  # def get_ids(self):
  #   table_names_to_get_ids = Upload.table_names_no_f_keys + Upload.table_names_simple
  #   for idx, ent in enumerate(self.data_by_row):
  #     for table_name in table_names_to_get_ids:
  #       id_name = table_name + "_id"
  #       where_parts = []
  #       current_data = ent[table_name]
  #       for field_name, val in current_data.items():
  #         where_parts.append(" {} = '{}' ".format(field_name, val))
  #       where_txt = "WHERE "
  #       where_txt += ' AND '.join(where_parts)
  #       # q = "SELECT {0}_id FROM {0} WHERE {1}".format(table_name, where_txt)
  #       id = mysql_utils.get_id(id_name, table_name, where_txt)
  #       self.data_by_row[idx][table_name][id_name] = id


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

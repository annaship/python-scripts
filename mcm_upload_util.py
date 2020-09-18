#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a common part for tsv to db and zotero to db scripts
from collections import defaultdict
import util
import sys

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql


class Upload:
  """
  table types (intersect is possible):
  *) table_name equal field_name ("identifier")
  *) many field_names correspond to one table_name = field_name ("place": ["subject_associated_places", "subject_place"]}), see many_values_to_one_field
  *) tables with foreign keys, see table_names_w_ids
  """

  table_names_w_ids = ["entry"]
  table_names_to_ignore = ["entry_view"]
  table_name_temp_dump = "whole_tsv_dump"
  many_values_to_one_field = {
    "content_url": ["content_url", "content_url_audio", "content_url_transcript"],
    "season": ["date_digital", "date_exact", "date_season", "date_season_yyyy", "subject_season"],
    "person": ["contributor", "creator", "creator_other", "subject_people"],
    "place":  ["country", "publisher_location", "subject_associated_places", "subject_place"]
  }

  where_to_look_if_not_the_same = {
    # "bibliographic_citation"   : "source.bibliographic_citation",
    # "content": "content",
    "content_url"                 : "content_url",
    "content_url_audio"           : "content_url",
    "content_url_transcript"      : "content_url",
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

  def __init__(self, metadata = None):
    """
        1) upload simple tables (table_names_simple)
        2) upload combine tables no foreign keys (content, person, place, season, source)
        3) get ids
        4) upload tables with ids
    """
    self.utils = util.Utils()
    self.metadata = metadata

    if self.utils.is_local():
      self.db_schema = 'mcm_history'
      self.mysql_utils = util.Mysql_util(host = 'localhost', db = self.db_schema, read_default_group = 'clienthome')
      print("host = 'localhost', db = {}".format(self.db_schema))
    else:
      self.db_schema = 'mcmurdohistory_metadata'
      host = '127.0.0.1'
      self.mysql_utils = util.Mysql_util(host = host, db = self.db_schema, read_default_group = 'client')
      # self.mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = self.db_schema, read_default_group = 'client')
      print("host = {}, db {}".format(host, self.db_schema))

    self.entry_table_name = self.table_names_w_ids[0]
    all_tables_sql_res = self.mysql_utils.get_table_names(self.db_schema)
    self.all_tables_set = set(self.utils.extract(all_tables_sql_res[0]))

    self.many_values_to_one_field_column_names = self.utils.flatten_2d_list(self.many_values_to_one_field.values())
    self.special_tables = self.get_special_tables()
    self.simple_tables = list(self.all_tables_set - set(self.special_tables))

    # self.drop_temp_table()
    # self.create_temp_table()
    #
    # self.upload_empty()
    # self.upload_simple_tables()
    # self.upload_all_from_tsv_into_temp_table()
    # self.mass_update_simple_ids()
    #
    # self.upload_many_values_to_one_field()
    # self.update_many_values_to_one_field_ids()
    #
    # self.upload_other_tables()

    print("here")

  def drop_temp_table(self):
    drop_query = "DROP TABLE IF EXISTS {}".format(self.table_name_temp_dump)
    self.mysql_utils.execute_no_fetch(drop_query)

  def create_temp_table(self):
    create_table_q = """
    CREATE TABLE IF NOT EXISTS `{0}` (
      `{0}_id` int(11) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
      `created` datetime DEFAULT current_timestamp(),
      `updated` datetime DEFAULT NULL
    ) ENGINE=InnoDB;
    """.format(self.table_name_temp_dump)
    self.mysql_utils.execute_no_fetch(create_table_q)

    all_fields = self.metadata.metadata_to_field.values()
    column_names_w_ids = [x + "_id" for x in all_fields]
    #           ADD COLUMN `ping_status` INT(1) NOT NULL AFTER
    #   `bibliographic_citation` varchar(512) DEFAULT '',
    #   `bibliographic_citation_id` int(11) unsigned NOT NULL,
    column_names_arr = []
    column_names_str_begin = "ALTER TABLE {}".format(self.table_name_temp_dump)
    for c_name_w_id in column_names_w_ids:
      add_col_str_w_id = " ADD COLUMN {} int(11) UNSIGNED NOT NULL\n".format(c_name_w_id)
      column_names_arr.append(add_col_str_w_id)
    for c_name in all_fields:
      # add_col_str = ' ADD COLUMN {} varchar(1024) DEFAULT ""'.format(c_name)
      add_col_str = ' ADD COLUMN {} TEXT DEFAULT ""\n'.format(c_name)
      # add_col_str = ' ADD COLUMN {} TEXT\n'.format(c_name)
      column_names_arr.append(add_col_str)

    # column_names_str_end = """ ADD UNIQUE KEY `all_id` (metadata_type(16), identifier(16), title(512), content(16), content_url(16), creator(16), creator_other(16), subject_place(16), coverage_lat(16), coverage_long(16), subject_associated_places(16), subject_people(16), subject_academic_field(16), subject_other(16), subject_season(16), date_season(16), date_season_yyyy(16), date_exact(16), date_digital(16), description(512), format(16), digitization_specifications(16), contributor(16), type(16), country(16), language(16), relation(16), source(512), publisher(512), publisher_location(16), bibliographic_citation(512), rights(16)) """
    # column_names_str_end = ""
    # column_names_arr.append(column_names_str_end)

    column_names_str = ", ".join(column_names_arr)
    add_columns_q = column_names_str_begin + column_names_str
    # print(add_columns_q)
    self.mysql_utils.execute_no_fetch(add_columns_q)

    # print("QQ")

  def get_special_tables(self):
    special_tables = [self.table_name_temp_dump]
    return special_tables + self.table_names_to_ignore + self.table_names_w_ids + list(self.many_values_to_one_field.keys())
    # ["entry", "person", "place", "season", "whole_tsv_dump"]

  def upload_empty(self):
    self.all_tables_set.discard(self.entry_table_name)
    self.all_tables_set.discard(self.table_names_to_ignore[0])
    for table_name in list(self.all_tables_set):
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")
      self.mysql_utils.execute_no_fetch(insert_query)

  def upload_simple_tables(self):
    for table_name in self.simple_tables:
      self.simple_mass_upload(table_name, table_name)

  def simple_mass_upload(self, table_name, field_name, val_arr = None):
    """Default argument values are evaluated only once at function definition time, which means that modifying the default value of the argument will affect all subsequent calls of the function.Jan 17, 2017
    """
    try:
      if not val_arr:
        val_arr = list(set(self.metadata.not_empty_tsv_content_dict[field_name]))
      self.mysql_utils.execute_insert_many(table_name, field_name, val_arr)

    except KeyError:
      insert_query = "INSERT IGNORE INTO `{}` (`{}`) VALUES (NULL)".format(table_name, table_name + "_id")
      self.mysql_utils.execute_no_fetch(insert_query)

  def upload_all_from_tsv_into_temp_table(self):
    table_name = self.table_name_temp_dump
    table_name_id = table_name + "_id"
    for current_row_d in self.metadata.tsv_file_content_dict_clean_keys:
      field_names_arr = list(current_row_d.keys())
      values_arr      = list(current_row_d.values())

      self.mysql_utils.execute_many_fields_one_record(table_name, field_names_arr, tuple(values_arr))

      # separate as add_id_back
      current_id = self.mysql_utils.get_id_esc(table_name_id, table_name, field_names_arr, values_arr)
      current_row_d[table_name_id] = current_id

  def mass_update_simple_ids(self):
    for table_name in self.simple_tables:
      try:
        current_vals = list(set(self.metadata.not_empty_tsv_content_dict[table_name]))
      except KeyError:
        # is empty
        continue
      field_name = table_name
      field_name_id = field_name + '_id'
      templ_arr = ['%s'] * len(current_vals)
      templ = ", ".join(templ_arr)
      select_q = """SELECT {}, {} FROM {} WHERE {} in ({});
      """.format(field_name, field_name_id, table_name, field_name, templ)
      sql_res = self.mysql_utils.execute_fetch_select(select_q, current_vals)

      for (val, val_id) in sql_res[0]:
        update_q = '''UPDATE {}
          SET {} = {} 
          WHERE {} = %s'''.format(self.table_name_temp_dump, field_name_id, val_id, field_name)
        self.mysql_utils.execute_no_fetch(update_q, val)

  def upload_many_values_to_one_field(self):
    tsv_field_names_to_upload = self.many_values_to_one_field_column_names
    value_present = self.utils.intersection(tsv_field_names_to_upload, self.metadata.not_empty_tsv_content_dict.keys())

    for table_name, tsv_field_names in self.many_values_to_one_field.items():
      for tsv_field_name in tsv_field_names:
        if tsv_field_name in value_present:
          val_arr = list(set(self.metadata.not_empty_tsv_content_dict[tsv_field_name]))
          self.simple_mass_upload(table_name, table_name, val_arr)

  def update_many_values_to_one_field_ids(self):
    table_name_to_update = self.table_name_temp_dump
    tsv_field_names_to_upload = self.utils.flatten_2d_list(self.many_values_to_one_field.values())
    for current_row_d in self.metadata.tsv_file_content_dict_clean_keys:
      """TODO: go over each table values instead?     
      for table_name, tsv_field_names in self.many_values_to_one_field.items():"""
      for tsv_field_name in tsv_field_names_to_upload:
        try:
          current_value = current_row_d[tsv_field_name]
        except KeyError:
          continue
        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
        current_id = self.mysql_utils.get_id_esc(table_name_w_id + '_id', table_name_w_id, table_name_w_id, current_value)

        # TODO: update these in columns rather then in rows (all data_exact where == 1976 etc.)
        update_q = 'UPDATE {} SET {} = {} WHERE {} = %s'.format(table_name_to_update, tsv_field_name + '_id', current_id, tsv_field_name)
        self.mysql_utils.execute_no_fetch(update_q, current_value)

  def get_entry_table_field_names(self):
    entry_field_names_q = """
    SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = %s 
      AND table_schema = %s 
      AND column_name <> %s
    """
    vals = (self.entry_table_name, self.db_schema, self.entry_table_name + "_id")
    return self.mysql_utils.execute_fetch_select(entry_field_names_q, vals)

  def get_empty_field_names(self, current_row_dict):
    except_fields = ["created", "updated"]
    entry_field_names_sql_res = self.get_entry_table_field_names()
    have_field_names = [k for k, v in current_row_dict.items() if v > 0]
    # TODO: seems slow, benchmark and try with utils.subtraction
    res = list(set(self.utils.extract(entry_field_names_sql_res[0])) - set(have_field_names) - set(except_fields))
    return res

  def find_empty_ids(self, current_row_dict):
    """ TODO: DRY with upload script
    """
    # TODO: seems slow, benchmark and try with utils.subtraction
    empty_field_names = self.get_empty_field_names(current_row_dict)
    for field in empty_field_names:
      name_no_id = field[:-3]
      # '''select identifier_id from identifier where identifier = ""'''
      # select_q = 'SELECT {} FROM {} WHERE {} = ""'.format(field, name_no_id, name_no_id)
      try:
        table_name_w_id = self.where_to_look_if_not_the_same[name_no_id]
        #
        # empty_id = self.mysql_utils.execute_fetch_select(select_q)
        # current_row_dict[field] = list (self.utils.extract(empty_id))[0]
      except KeyError:
        table_name_w_id = name_no_id

      select_q = 'SELECT {} FROM {} WHERE {} = ""'.format(table_name_w_id + "_id", table_name_w_id, table_name_w_id)
      empty_id = self.mysql_utils.execute_fetch_select(select_q)
      current_row_dict[field] = list (self.utils.extract(empty_id))[0]

    return current_row_dict

  def upload_other_tables(self):
    table_name_to_update = self.entry_table_name # ["entry"]
    where_to_look_for_ids = self.table_name_temp_dump
    for current_row_d in self.metadata.tsv_file_content_dict_clean_keys:
      tsv_field_names_to_upload = current_row_d.keys()
      tsv_field_names_to_upload_ids = [x+"_id" for x in tsv_field_names_to_upload if not x.endswith("_id")]
      tsv_field_names_to_upload_ids_str = ', '.join(tsv_field_names_to_upload_ids)

      unique_keys = current_row_d.keys()
      where_part0 = self.mysql_utils.make_where_part_template(unique_keys)

      select_q = '''SELECT {} FROM {} 
        WHERE {}'''.format(tsv_field_names_to_upload_ids_str, where_to_look_for_ids, where_part0)
      sql_res = self.mysql_utils.execute_fetch_select_to_dict(select_q, current_row_d.values())
      dict_w_all_ids = self.find_empty_ids(sql_res[0])
      # IF empty and no id - get it
      self.mysql_utils.execute_many_fields_one_record(table_name_to_update, list(dict_w_all_ids.keys()), tuple(dict_w_all_ids.values()))


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  pass
  # upload = upload_tsv_to_db_for_mcm.Upload(utils)

  # c = Collections()
  # export = Export()
  # import_to_mysql = ToMysql()
  # export.()
  # export.print_items_info()
  # export.all_items_fields()
  # export.all_coll()
  # export.get_all()
  # export.get_all_collections()

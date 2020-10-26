#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a common part for tsv to db and zotero to db scripts
import sys
import os
from collections import defaultdict
import util
import requests
import time

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql


class DataManaging:
  """Clean data if needed"""

  def __init__(self):
    self.identifier_table_name = "identifier"

    self.utils = util.Utils()
    self.upload = Upload()  # assigns class1 to your first class

  def check_type(self, type):
    return type[0]

  def upload_all_identifiers(self, identifiers_from_tsv):
    val_arr = list(set(identifiers_from_tsv))
    self.upload.mysql_utils.execute_insert_many(self.identifier_table_name, self.identifier_table_name, val_arr)

  def get_last_identifier(self, type):
    # get the biggest one from db and compare with what's in csv
    first_char = self.check_type(type)
    first_part = "MCMEH-{}".format(first_char)
    get_last_id_q = """SELECT MAX({0}) FROM {0} WHERE {0} LIKE "{1}%";""".format(self.identifier_table_name, first_part)
    get_last_id_q_res = self.upload.mysql_utils.execute_fetch_select(get_last_id_q)
    last_num_res = list(self.utils.extract(get_last_id_q_res))[0]
    if not last_num_res:
      last_num_res = "{}000000".format(first_part)
    last_num_res_arr = last_num_res.split("-")
    last_num = int(last_num_res_arr[1][1:])
    num_part = str(last_num + 1).zfill(6)
    return first_part + num_part

  def check_or_create_identifier(self, type, identifiers_from_tsv):
    # 0) upload all ids. TODO: do it once
    self.upload_all_identifiers(identifiers_from_tsv)
    # 1) get_last_id
    curr_identifier = self.get_last_identifier(type)
    # 2) insert_identifier
    self.upload.mysql_utils.execute_insert_mariadb(self.identifier_table_name, self.identifier_table_name,
                                                   curr_identifier)
    # 3) get its id
    db_id = self.upload.mysql_utils.get_id_esc(self.identifier_table_name + "_id", self.identifier_table_name,
                                               self.identifier_table_name, curr_identifier)

    return (db_id, curr_identifier)


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
    "season"     : ["date_digital", "date_exact", "date_season", "date_season_yyyy", "subject_season"],
    "person"     : ["contributor", "creator", "creator_other", "subject_people"],
    "place"      : ["country", "publisher_location", "subject_associated_places", "subject_place"]
  }

  where_to_look_if_not_the_same = {
    # "bibliographic_citation"   : "source.bibliographic_citation",
    # "content": "content",
    "content_url"              : "content_url",
    "content_url_audio"        : "content_url",
    "content_url_transcript"   : "content_url",
    "contributor"              : "person",
    "country"                  : "place",
    # "coverage_lat": "coverage_lat",
    # "coverage_long": "coverage_long",
    "creator"                  : "person",
    "creator_other"            : "person",
    "date_digital"             : "season",
    "date_exact"               : "season",
    "date_season"              : "season",
    "date_season_yyyy"         : "season",
    # "description"              : "content.description",
    # "digitization_specifications": "digitization_specifications",
    # "format": "format",
    # "identifier": "identifier",
    # "language": "language",
    # "publisher"                : "publisher",
    "publisher_location"       : "place",
    # "relation": "relation",
    # "rights"                   : "source.rights",
    # "source": "source",
    "subject_academic_field"   : "subject_academic_field",
    "subject_associated_places": "place",
    # "subject_other": "subject_other",
    "subject_people"           : "person",
    "subject_place"            : "place",
    "subject_season"           : "season",
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
    self.is_local = self.utils.is_local()
    self.cnt_increment = 1000

    if self.is_local:
      self.db_schema = 'mcm_history'
      self.mysql_utils = util.Mysql_util(host = 'localhost', db = self.db_schema, read_default_group = 'clienthome')
      self.utils.print_both("host = 'localhost', db = {}".format(self.db_schema))
    else:
      self.db_schema = 'mcmurdohistory_metadata'
      host = '127.0.0.1'
      self.mysql_utils = util.Mysql_util(host = host, db = self.db_schema, read_default_group = 'client')
      # self.mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = self.db_schema, read_default_group = 'client')
      self.utils.print_both("host = {}, db {}".format(host, self.db_schema))

    self.entry_table_name = self.table_names_w_ids[0]
    all_tables_sql_res = self.mysql_utils.get_table_names(self.db_schema)
    self.all_tables_set = set(self.utils.extract(all_tables_sql_res[0]))

    self.many_values_to_one_field_column_names = self.utils.flatten_2d_list(self.many_values_to_one_field.values())
    self.special_tables = self.get_special_tables()
    self.simple_tables = list(self.all_tables_set - set(self.special_tables))

    self.upload_empty()

    self.utils.print_both("End of Upload superclass")

  def drop_temp_table(self):
    drop_query = "DROP TABLE IF EXISTS {}".format(self.table_name_temp_dump)
    self.mysql_utils.execute_no_fetch(drop_query)

  def create_temp_table(self):
    create_table_q = """
    CREATE TABLE IF NOT EXISTS `{0}` (
      `{0}_id` int(11) unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
      `updated` datetime DEFAULT CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP(),
      `created` datetime DEFAULT CURRENT_TIMESTAMP()

    ) ENGINE=InnoDB;
    """.format(self.table_name_temp_dump)
    self.mysql_utils.execute_no_fetch(create_table_q)

    all_fields = self.metadata.metadata_to_field.values()
    column_names_w_ids = [x + "_id" for x in all_fields]

    column_names_arr = []
    column_names_str_begin = "ALTER TABLE {}".format(self.table_name_temp_dump)
    for c_name_w_id in column_names_w_ids:
      add_col_str_w_id = " ADD COLUMN {} int(11) UNSIGNED NOT NULL DEFAULT 0\n".format(c_name_w_id)
      column_names_arr.append(add_col_str_w_id)
    for c_name in all_fields:
      add_col_str = ' ADD COLUMN {} TEXT DEFAULT ""\n'.format(c_name)
      column_names_arr.append(add_col_str)


    column_names_arr.append(' ADD COLUMN combined TEXT NOT NULL\n')
    column_names_arr.append(' ADD UNIQUE KEY all_tsv_fields (combined)\n')
    column_names_str = ", ".join(column_names_arr)
    add_columns_q = column_names_str_begin + column_names_str
    self.mysql_utils.execute_no_fetch(add_columns_q)

  def get_special_tables(self):
    special_tables = [self.table_name_temp_dump]
    return special_tables + self.table_names_to_ignore + self.table_names_w_ids + list(
      self.many_values_to_one_field.keys())
    # ["entry", "person", "place", "season", "whole_tsv_dump"]

  def upload_empty(self):
    self.all_tables_set.discard(self.entry_table_name)
    self.all_tables_set.discard(self.table_names_to_ignore[0])
    for table_name in list(self.all_tables_set):
      self.insert_null(table_name)

  def insert_null(self, table_name):
    insert_query = "INSERT IGNORE INTO `{0}` (`{1}`) VALUES (NULL) ON DUPLICATE KEY UPDATE {1} = NULL".format(
      table_name, table_name + "_id")
    self.mysql_utils.execute_no_fetch(insert_query)

  def upload_simple_tables(self):
    for table_name in self.simple_tables:
      self.simple_mass_upload(table_name, table_name)

  def simple_mass_upload(self, table_name, field_name, val_arr = None):
    """Default argument values are evaluated only once at function definition time, which means that modifying the default value of the argument will affect all subsequent calls of the function.
    """
    try:
      if not val_arr:
        val_arr = list(set(self.metadata.not_empty_tsv_content_dict[field_name]))
      self.mysql_utils.execute_insert_many(table_name, field_name, val_arr)

    except KeyError:
      self.insert_null(table_name)

  def upload_all_from_tsv_into_temp_table(self, quiet = False):
    table_name_id = self.table_name_temp_dump + "_id"
    for current_row_d in self.metadata.tsv_file_content_dict_ok:
      field_names_arr = list(current_row_d.keys())
      values_arr = list(current_row_d.values())

      # TODO: add on duplicate key... to avoid ~/opt/anaconda3/lib/python3.7/site-packages/pymysql/cursors.py:170: Warning: (1062, "Duplicate entry 'Cape Crozier' for key 'place'")
      #   result = self._query(query)
      try:
        self.mysql_utils.execute_many_fields_one_record(self.table_name_temp_dump, field_names_arr, tuple(values_arr))
      except mysql.OperationalError as e:
        self.utils.print_both(e)
        pass

      # separate as add_id_back
      current_id = self.mysql_utils.get_id_esc(table_name_id, self.table_name_temp_dump, field_names_arr, values_arr)
      current_row_d[table_name_id] = current_id
    # all_fields = list(set([tuple(d.keys()) for d in self.metadata.tsv_file_content_dict_ok]))
      self.update_temp_w_combine(field_names_arr)

  def update_temp_w_combine(self, field_names_arr):
      concat_str = "CONCAT({})".format(", ".join(field_names_arr))
      combine_query = """UPDATE {}
                          SET combined = {};
      """.format(self.table_name_temp_dump, concat_str)
      self.mysql_utils.execute_no_fetch(combine_query)

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

  def get_all_values_for_temp_update(self, tsv_field_names_to_upload, current_row_d):
    # (1,1,1),(2,2,3),(3,9,3),(4,10,12)
    all_vals = []
    for tsv_field_name in tsv_field_names_to_upload:
      row_vals = []

      try:
        current_value = current_row_d[tsv_field_name]
      except KeyError:
        continue

      table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
      current_id = self.mysql_utils.get_id_esc(table_name_w_id + '_id', table_name_w_id, table_name_w_id, current_value)

      # update_q = 'UPDATE {} SET {} = {} WHERE {} = %s'.format(self.table_name_temp_dump, tsv_field_name + '_id', current_id,
      #                                                         tsv_field_name)
      # print(update_q)
      """
      UPDATE whole_tsv_dump SET content_url_id = 2 WHERE content_url = %s
      UPDATE whole_tsv_dump SET content_url_audio_id = 0 WHERE content_url_audio = %s
      """

  # def make_list_of_dicts_w_ids(self, tsv_field_names_to_upload):
  #   tsv_file_content_list_dict_ok_w_ids = []
  #   # TODO: why not go over key, value and use key + '_id' as table_name_w_id?
  #   for current_row_d in self.metadata.tsv_file_content_dict_ok:
  #     temp_dict = current_row_d
  #     for tsv_field_name in tsv_field_names_to_upload:
  #
  #       try:
  #         current_value = current_row_d[tsv_field_name]
  #       except KeyError:
  #         continue
  #
  #       table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
  #       current_id = self.mysql_utils.get_id_esc(table_name_w_id + '_id', table_name_w_id, table_name_w_id,
  #                                                current_value)
  #
  #       temp_dict[tsv_field_name + '_id'] = current_id
  #
  #     tsv_file_content_list_dict_ok_w_ids.append(temp_dict)
  #   return tsv_file_content_list_dict_ok_w_ids

  def make_list_of_dicts_w_ids(self, tsv_field_names_to_upload):
    tsv_file_content_list_dict_ok_w_ids = []
    # TODO: why not go over key, value and use key + '_id' as table_name_w_id?
    for current_row_d in self.metadata.tsv_file_content_dict_ok:
      temp_dict = current_row_d
      for tsv_field_name in tsv_field_names_to_upload:

        try:
          current_value = current_row_d[tsv_field_name]
        except KeyError:
          continue

        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
        current_id = self.mysql_utils.get_id_esc(table_name_w_id + '_id', table_name_w_id, table_name_w_id,
                                                 current_value)

        temp_dict[tsv_field_name + '_id'] = current_id

      tsv_file_content_list_dict_ok_w_ids.append(temp_dict)
    return tsv_file_content_list_dict_ok_w_ids

  """
  TODO:
  In 500 chunks/rows do:
  INSERT INTO whole_tsv_dump
    (f1, f2, f3)
    VALUES 
        (%s, %s, %s),
        (%s, %s, %s),
        (%s, %s, %s),
    ON DUPLICATE KEY UPDATE 
        f1 = VALUES(f1),
        f2 = VALUES(f2)...
        
  """
  def update_many_values_to_one_field_ids(self):
    table_name_to_update = self.table_name_temp_dump
    tsv_field_names_to_upload = self.utils.flatten_2d_list(self.many_values_to_one_field.values())

    tsv_file_content_list_dict_ok_w_ids = self.make_list_of_dicts_w_ids(tsv_field_names_to_upload)

    # TODO: use format_update_duplicates() ?

    all_fields = list(set([tuple(d.keys()) for d in tsv_file_content_list_dict_ok_w_ids]))
    fields_to_update = ["{0} = VALUES({0})".format(field_name) for field_name in all_fields[0]]
    all_fields_no_id = [f for f in all_fields[0] if not f.endswith("_id")]
    concat_str = "combined = CONCAT({})".format(", ".join(all_fields_no_id))

    for d in tsv_file_content_list_dict_ok_w_ids:
      insert_array = []
      data = []
      for key, value in d.items():
        insert_array.append("%s = %%s" % key)  # results in key = %s
        data.append(value)
      insert_array.append(concat_str)
      insert_values = ", ".join(insert_array)
      query_insert = "INSERT INTO `%s` SET %s ON DUPLICATE KEY UPDATE %s" % (table_name_to_update, insert_values, insert_values)
      self.mysql_utils.cursor.execute(query_insert, data * 2)

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

  #   def update_many_values_to_one_field_ids(self, quiet = False):
  #     table_name_to_update = self.table_name_temp_dump
  #     tsv_field_names_to_upload = self.utils.flatten_2d_list(self.many_values_to_one_field.values())
  #     cnt = 0
  #     # t0 = time.time()
  #     t0 = self.utils.benchmark_w_return_1("for current_row_d in self.metadata.tsv_file_content_dict_ok")
  #
  #     for current_row_d in self.metadata.tsv_file_content_dict_ok:
  #       """TODO: go over each table values instead?
  #       for table_name, tsv_field_names in self.many_values_to_one_field.items():"""
  #       cnt += 1
  #       if (not quiet) and (cnt % self.cnt_increment == 0):
  #         print('update_many_values_to_one_field_ids: {}'.format(cnt))
  #         self.utils.benchmark_w_return_2(t0, "for current_row_d in self.metadata.tsv_file_content_dict_ok")
  #
  #       for tsv_field_name in tsv_field_names_to_upload:
  #         try:
  #           current_value = current_row_d[tsv_field_name]
  #         except KeyError:
  #           continue
  #         table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]
  #         current_id = self.mysql_utils.get_id_esc(table_name_w_id + '_id', table_name_w_id, table_name_w_id, current_value)
  #
  #         update_q = 'UPDATE {} SET {} = {} WHERE {} = %s'.format(table_name_to_update, tsv_field_name + '_id', current_id, tsv_field_name)
  #         self.mysql_utils.execute_no_fetch(update_q, current_value)

  def get_empty_field_names(self, current_row_dict):
    except_fields = ["created", "updated"]
    entry_field_names_sql_res = self.get_entry_table_field_names()
    try:
      have_field_names = [k for k, v in current_row_dict.items() if v > 0]
    except TypeError:
      self.utils.print_both("current_row_dict = {}".format(current_row_dict))
      raise

    res = list(set(self.utils.extract(entry_field_names_sql_res[0])) - set(have_field_names) - set(except_fields))
    return res

  def find_empty_ids(self, current_row_dict):
    empty_field_names = self.get_empty_field_names(current_row_dict)
    for field in empty_field_names:
      name_no_id = field[:-3]
      try:
        table_name_w_id = self.where_to_look_if_not_the_same[name_no_id]
      except KeyError:
        table_name_w_id = name_no_id

      select_q = 'SELECT {} FROM {} WHERE {} = ""'.format(table_name_w_id + "_id", table_name_w_id, table_name_w_id)
      empty_id = self.mysql_utils.execute_fetch_select(select_q)
      current_row_dict[field] = list(self.utils.extract(empty_id))[0]

    return current_row_dict

  def check_if_id_is_in_entry(self, current_id):
    """
    :param current_id:
    :return: boolean
    """
    identifier_table_name = self.metadata.data_managing.identifier_table_name
    query = """
    SELECT * FROM {0} JOIN {1} USING({1}_id)
WHERE {1} = %s
limit 1;""".format(self.entry_table_name, identifier_table_name)
    # print(query)
    res = self.mysql_utils.execute_fetch_select(query, current_id)
    id_is_in_entry = False
    if len(res[0]) > 0:
      id_is_in_entry = True
    return id_is_in_entry

  def upload_other_tables(self, quiet = False):
    table_name_to_update = self.entry_table_name  # ["entry"]
    where_to_look_for_ids = self.table_name_temp_dump
    # cnt = 0
    for current_row_d in self.metadata.tsv_file_content_dict_ok:
      # cnt += 1
      # if (not quiet) and (cnt % self.cnt_increment == 0):
      #   print('Uploading rows into "Entry" table: %s' % cnt)

      tsv_field_names_to_upload = current_row_d.keys()
      tsv_field_names_to_upload_ids = [x + "_id" for x in tsv_field_names_to_upload if not x.endswith("_id")]
      tsv_field_names_to_upload_ids_str = ', '.join(tsv_field_names_to_upload_ids)

      unique_keys = current_row_d.keys()
      where_part0 = self.mysql_utils.make_where_part_template(unique_keys)

      select_q = '''SELECT {} FROM {} 
        WHERE {}'''.format(tsv_field_names_to_upload_ids_str, where_to_look_for_ids, where_part0)
      sql_res = self.mysql_utils.execute_fetch_select_to_dict(select_q, current_row_d.values())
      # IF empty and no id - get it
      dict_w_all_ids = self.find_empty_ids(sql_res[0])

      # TODO: why diff from tsv_field_names_to_upload_ids?
      all_fields = list(dict_w_all_ids.keys())
      q_addition = self.format_update_duplicates(current_row_d, all_fields)
      self.mysql_utils.execute_many_fields_one_record(table_name_to_update, all_fields, tuple(dict_w_all_ids.values()),
                                                      ignore = "", addition = q_addition)

  # TODO: rm id_is_in_entry check and use for all
  def format_update_duplicates(self, current_row_d, all_fields):
    id_is_in_entry = self.check_if_id_is_in_entry(current_row_d[self.metadata.data_managing.identifier_table_name])

    fields_to_update = ["{0} = VALUES({0})".format(field_name) for field_name in all_fields]
    fields_to_update_str = ", ".join(fields_to_update)

    q_addition = ""
    if id_is_in_entry:
      q_addition = """ ON DUPLICATE KEY UPDATE {}""".format(fields_to_update_str)
    return q_addition


class FileRetrival:

  def __init__(self, metadata = None):
    self.utils = util.Utils()
    self.metadata = metadata
    self.is_local = self.utils.is_local()
    self.cnt_increment = 1000

  def get_files_path(self, end_dir = ''):
    home_dir = os.environ['HOME']
    if self.is_local:
      files_path = '{}/work/MCM/{}'.format(home_dir, end_dir)
    else:
      # files_path = '/home/ashipuno'
      # end_dir = 'zotero_attachments'
      files_path = '{}/mcmurdohistory/sites/default/files/{}'.format(home_dir, end_dir)
    # print("files_path = {}".format(files_path))
    return files_path

  def get_current_urls(self, entry_d):
    url_fields = ['content_url', 'content_url_audio', 'content_url_transcript']
    urls = []
    for url_field in url_fields:
      try:
        url = entry_d[url_field]
        if url and len(url) > 0:
          urls.append(url)
      except KeyError:
        pass
    return urls

  def change_dl(self, urls):
    return [url.replace('?dl=0', '?dl=1', 1) for url in urls]

  def download_all_from_content_url(self, quiet = False):
    url_fields = ['content_url', 'content_url_audio', 'content_url_transcript']
    cnt = 0
    for entry_d in self.metadata.tsv_file_content_dict_no_empty:
      urls = self.get_current_urls(entry_d)
      urls = self.change_dl(urls)
      for url in urls:
        file_name = self.download_file(url)
      cnt += 1
      if (not quiet) and (cnt % self.cnt_increment == 0):
        print('Downloading files from Dropbox: %s' % cnt)

  def get_file_name(self, r_headers):
    file_name = ""
    try:
      file_name = r_headers['Content-Disposition'].split(';')[1].rsplit('=', 1)[1]
      file_name = file_name.replace('"', '')
    except KeyError:
      print("Please provide a valid google spreadsheet url")
      sys.exit()

    if file_name == "":
      file_name = self.create_attachment_name_from_id()

    files_path = self.get_files_path()
    return os.path.join(files_path, file_name)

  def download_file(self, url, google_file_id = None):
    try:
      r = requests.get(url, allow_redirects = True)

      file_name = self.get_file_name(r.headers)

      open(file_name, 'wb').write(r.content)
      return file_name
    except requests.exceptions.MissingSchema:
      self.utils.print_both("Can't download a file, wrong URL: '{}'".format(url))
      pass
      # Invalid URL 'NOT IN DROPBOX': No schema supplied. Perhaps you meant http://NOT IN DROPBOX?

  def create_attachment_name_from_id(self):
    pass


if __name__ == '__main__':
  """Called from mcmPpy_zotero.py and upload_tsv_to_db_for_mcm.py"""
  pass

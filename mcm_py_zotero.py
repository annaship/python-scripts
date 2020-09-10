#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzotero import zotero
from collections import defaultdict
import util
# import upload_tsv_to_db_for_mcm

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql

"""
    [account_type] => group
    [account_id] => 1415490
    [start] => 
    [api_key] => U4CPfWiKzcs7iyJV9IdPnEZU
"""

library_id = "1415490"
library_type = "group"
api_key = "U4CPfWiKzcs7iyJV9IdPnEZU"

zot = zotero.Zotero(library_id, library_type, api_key)


class Collections:
  def __init__(self):
    self.collections = {}
    self.all_coll_fields = set()
    # coll = ""
    # while (zot.nextCollection()):
    #   key = coll.primary.key
    # (coll.primary ? coll.primary: coll).key
    # this.collections[key] = {
    #   parent: coll.fields.parentKey,
    #   name  : coll.name,
    # };
    # }

  def all_coll(self):
    all_coll = zot.all_collections()
    for coll in all_coll:
      curr_keys = coll['data'].keys()
      self.all_coll_fields = self.all_coll_fields | set(curr_keys)

  def get_all_collections(self):
    dump_collections = open('dump_collections0.txt', 'w')
    dump_all_collections = open('dump_all_collections0.txt', 'w')
    print(zot.collections(), file = dump_collections)
    print(zot.all_collections(), file = dump_all_collections)

    dump_collections.close()
    dump_all_collections.close()


class ToMysql:
  """
    `person` text NOT NULL DEFAULT '',
  `first_name` text DEFAULT '',
  `last_name` text DEFAULT '',

  """

  def __init__(self):
    self.entry_table_name = "entry"

    self.zotero_to_sql_fields = {
      'creators'    : 'role.role', # creator
      'name'        : 'person.person',  # creator, #creator_other
      'firstName'   : 'person.first_name',  # creator, #creator_other
      'lastName'    : 'person.last_name',  # creator, #creator_other
      'abstractNote': 'description.description',
      'bookTitle'   : 'title.title',
      'title'       : 'title.title',
      'date'        : 'season.season',  # 'date_exact', 'date_season', 'date_season_yyyy',
      'language'    : 'language.language',
      'publicationTitle': 'publisher.publisher',
      'publisher'   : 'publisher.publisher',
      'rights'      : 'rights.rights',
      'volume'      : 'source.source',
    }
    """
    add to temp_table first?
    make an identifier
    add to entry
    
    """
    self.many_values_to_one_field = {
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

    self.entry_rows_dict = defaultdict()
    self.make_upload_queries()
    self.insert_entry_row()
    print("DONE")

  """TODO: If there more than one person
  a) combine them in one row in "person" table and provide one id in entry
  or
  b) make as many entry rows as there are different persons
  """
  def insert_person_combination_and_get_id(self, person_list):
    persons_str = "; ".join(sorted(person_list))
    table_name = "person"
    field_name = "person"
    return self.get_id_by_serch_or_insert(table_name, field_name, persons_str)

  def insert_entry_row(self):
    # TODO: get empty field names from entry table once here
    for key, val_dict in self.entry_rows_dict.items():
      if len(val_dict) > 0:
        """
        self.entry_rows_dict = {defaultdict: 5} defaultdict(None, {'JSQB7M8J': defaultdict(None, {'title_id': 4791, 'person': [{'person_id': 1121, 'role_id': 1}], 'publisher_id': 14, 'source_id': 802, 'season_id': 457}), 'NKVCAI2K': defaultdict(None, {}), '4Q3GMMWU': defaultdict(None, {}),...

        TODO: DRY with upload_tsv_to_db_for_mcm.py
        select_q = '''SELECT {} FROM {} 
          WHERE {}'''.format(tsv_field_names_to_upload_ids_str, where_to_look_for_ids, where_part0)
        sql_res = mysql_utils.execute_fetch_select_to_dict(select_q, current_row_d.values())
        dict_w_all_ids = upload.find_empty_ids(sql_res[0])
        # IF empty and no id - get it
        mysql_utils.execute_many_fields_one_record(table_name_to_update, list(dict_w_all_ids.keys()), tuple(dict_w_all_ids.values()))
        """
        dict_w_all_ids = self.find_empty_ids(val_dict)

        # pass

  def get_entry_table_field_names(self):
    entry_field_names_q = """
    SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = %s 
      AND table_schema = %s 
      AND column_name <> %s
    """
    vals = (self.entry_table_name, db_schema, self.entry_table_name + "_id")
    return mysql_utils.execute_fetch_select(entry_field_names_q, vals)

  def get_empty_field_names(self, current_row_dict):
    entry_field_names_sql_res = self.get_entry_table_field_names()
    have_field_names = current_row_dict.keys()
    # TODO: seems slow, benchmark and try with utils.subtraction
    empty_field_names = list(set(utils.extract(entry_field_names_sql_res)) - set(have_field_names))
    res = self.convert_names_for_multy_named(empty_field_names)

  def convert_names_for_multy_named(self, empty_field_names):
    """
        table_name_w_id = self.where_to_look_if_not_the_same[tsv_field_name]

    :return:
    """
    for field_name in empty_field_names:
      field_name_no_id = field_name[:-3] # TODO see below, DRY
      table_name_w_id = self.where_to_look_if_not_the_same[field_name_no_id]

  def find_empty_ids(self, current_row_dict):
    """ TODO: DRY with upload script
    """
    # entry_field_names_sql_res = self.get_entry_table_field_names()
    # have_fiedl_names = current_row_dict.keys()
    # # TODO: seems slow, benchmark and try with utils.subtraction
    empty_field_names = self.get_empty_field_names(current_row_dict)
    # empty_field_names = list(set(utils.extract(entry_field_names_sql_res)) - set(current_row_dict.keys()))
    for field in empty_field_names:
      name_no_id = field[:-3]
      # '''select identifier_id from identifier where identifier = ""'''
      select_q = 'SELECT {} FROM {} WHERE {} = ""'.format(field, name_no_id, name_no_id)
      empty_id = mysql_utils.execute_fetch_select(select_q)
      current_row_dict[field] = list(utils.extract(empty_id))[0]
    return current_row_dict


  def make_full_name(self, val_d):
    return "{}, {}".format(val_d['lastName'], val_d['firstName'])

  def update_first_last_names(self, val_d, db_id):
    names_tuple = (val_d['lastName'], val_d['firstName'])
    (table_name, last_name) = self.zotero_to_sql_fields['lastName'].split(".")
    (table_name, first_name) = self.zotero_to_sql_fields['firstName'].split(".")

    update_q = '''UPDATE {}
      SET {} = %s, {} = %s 
      WHERE {} = {}'''.format(table_name, last_name, first_name, table_name + '_id', db_id)
    mysql_utils.execute_no_fetch(update_q, names_tuple)

  def get_person_id(self, full_name):
    table_name = "person"
    field_name = "person"
    db_id = self.get_id_by_serch_or_insert(table_name, field_name, full_name)
    return db_id

  def get_id_by_serch_or_insert(self, table_name, field_name, value):
    field_name_id = field_name + "_id"
    try:
      db_id = mysql_utils.get_id_esc(field_name_id, table_name, field_name, value)
    except IndexError:
      mysql_utils.execute_insert(table_name, field_name, value)
      db_id = mysql_utils.get_id_esc(field_name_id, table_name, field_name, value)
    return db_id

    """
      value = 'creators' = {list: 8} [{'creatorType': 'author', 'firstName': 'Rachel I.', 'lastName': 'Leihy'}, {'creatorType': 'author', 'firstName': 'Bernard W. T.', 'lastName': 'Coetzee'}, {'creatorType': 'author', 'firstName': 'Fraser', 'lastName': 'Morgan'}, {'creatorType': 'author', 'firstName': 'Ben', 'lastName': 'Raymond'}, {'creatorType': 'author', 'firstName': 'Justine D.', 'lastName': 'Shaw'}, {'creatorType': 'author', 'firstName': 'Aleks', 'lastName': 'Terauds'}, {'creatorType': 'author', 'firstName': 'Kees', 'lastName': 'Bastmeijer'}, {'creatorType': 'author', 'firstName': 'Steven L.', 'lastName': 'Chown'}]
0 = {dict: 3} {'creatorType': 'author', 'firstName': 'Rachel I.', 'lastName': 'Leihy'}
1 = {dict: 3} {'creatorType': 'author', 'firstName': 'Bernard W. T.', 'lastName': 'Coetzee'}
...
    """

  def make_entry_rows_dict_of_ids(self, k, v, z_key):
    try:
      db_tbl_field_name = self.zotero_to_sql_fields[k]

      if isinstance(v, list):
        person_id_list = []
        current_persons_list = []

        for d in v:
          full_name = self.make_full_name(d)

          person_db_id = self.get_person_id(full_name)
          self.update_first_last_names(d, person_db_id)

          (table_name, field_name) = db_tbl_field_name.split(".")
          role_db_id1 = self.get_id_by_serch_or_insert(table_name, field_name, d['creatorType'])
          person_id_list.append({"person_id": person_db_id, "role_id": role_db_id1})
          current_persons_list.append(full_name)

          self.entry_rows_dict[z_key]["role_id"] = role_db_id1 # TODO: check if different roles in one dict

        all_cur_persons_id = self.insert_person_combination_and_get_id(current_persons_list)
        self.entry_rows_dict[z_key]["person_id"] = all_cur_persons_id
      else:
        (table_name, field_name) = db_tbl_field_name.split(".")
        db_id = self.get_id_by_serch_or_insert(table_name, field_name, v)
        self.entry_rows_dict[z_key][field_name + "_id"] = db_id
    except KeyError:
      pass # zotero field is not in the db field names list

  def make_upload_queries(self):
    for z_entry in export.all_items_dump:
      z_key = z_entry['key']
      self.entry_rows_dict[z_key] = defaultdict()
      for k, v in z_entry['data'].items():
        if v:
          self.make_entry_rows_dict_of_ids(k, v, z_key)

  def make_all_info_dict(self):
    for item in self.all_items_dump:
      temp_dict = defaultdict()
      """
      item['data'] = {dict: 32} {'key': 'JSQB7M8J', 'version': 3648, 'itemType': 'journalArticle', 'title': 'Abrasion in ice-free -TEST', 'creators': [{'creatorType': 'author', 'firstName': 'Michael C.', 'lastName': 'Malin'}], 'abstractNote': '', 'publicationTitle': 'Antarctic Journal of
 'key' = {str} 'JSQB7M8J'
 'version' = {int} 3648
 'itemType' = {str} 'journalArticle'
 'title' = {str} 'Abrasion in ice-free -TEST'
 'creators' = {list: 1} [{'creatorType': 'author', 'firstName': 'Michael C.', 'lastName': 'Malin'}]
 'abstractNote' = {str} ''
 'publicationTitle' = {str} 'Antarctic Journal of the United States'
 ...
      """
      temp_dict['key'] = item['data']['key']
      temp_dict = self.make_temp_dict(temp_dict, item['data'])

      self.all_items_l_dict.append(temp_dict)
      # self.zotero_to_sql_fields

  def make_temp_dict(self, temp_dict, in_item_dict):
    for k, v in in_item_dict.items():
      if v:  # (don't retain empty values')
        if isinstance(v, (tuple, list)):
          for list_item in v:
            self.make_temp_dict(temp_dict, list_item)
        else:
          try:
            field_name = self.zotero_to_sql_fields[k]
            temp_dict[field_name] = in_item_dict[k]
          except KeyError:
            temp_dict[k] = in_item_dict[k]
    return temp_dict


class Export:
  def __init__(self):

    self.all_items_l_dict = []

    # self.all_items_dump = self.dump_all_items()
    # debug short
    self.all_items_dump = zot.top(limit = 5)

    self.all_items_fields = set()
    self.get_all_zotero_fields()

    # self.make_all_info_dict()

    # self.all_coll_fields = set()

  def print_items_info(self):
    items = zot.top(limit = 5)
    # we've retrieved the latest five top-level items in our library
    # we can print each item's item type and ID
    for item in items:
      self.all_items_fields.add(item['data']['key'])
      print('Item Type: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

  def get_all_items_to_file(self):
    dump_all_items = open('dump_all_items.txt', 'w')
    print(zot.everything(zot.top()), file = dump_all_items)
    dump_all_items.close()

  def get_all_zotero_fields(self):
    for item in self.all_items_dump:
      self.all_items_fields = self.all_items_fields | item['data'].keys()

  def dump_all_items(self):
    return zot.everything(zot.top())


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  utils = util.Utils()

  if utils.is_local():
    db_schema = 'mcm_history'
    mysql_utils = util.Mysql_util(host = 'localhost', db = db_schema, read_default_group = 'clienthome')
    print("host = 'localhost', db = {}".format(db_schema))
  else:
    db_schema = 'mcmurdohistory_metadata'
    host = '127.0.0.1'
    mysql_utils = util.Mysql_util(host = host, db = db_schema, read_default_group = 'client')
    # mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = db_schema, read_default_group = 'client')
    print("host = {}, db {}".format(host, db_schema))

  # upload = upload_tsv_to_db_for_mcm.Upload(utils)

  c = Collections()
  export = Export()
  import_to_mysql = ToMysql()
  # export.()
  # export.print_items_info()
  # export.all_items_fields()
  # export.all_coll()
  # export.get_all()
  # export.get_all_collections()

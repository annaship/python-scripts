#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzotero import zotero
from collections import defaultdict
import util

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
    self.zotero_to_sql_fields = {
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

    self.make_upload_queries()

  def make_query(self, k, v):
    if isinstance(v, (tuple, list)):
      pass
      # for list_item in v:
      #   self.make_query(temp_dict, list_item)
    else:
      try:
        field_name = self.zotero_to_sql_fields[k]
        # execute_insert(self, table_name, field_name, val_list
        upload_q = "INSERT INTO"
        temp_dict[field_name] = in_item_dict[k]
      except KeyError:
        temp_dict[k] = in_item_dict[k]

  def make_upload_queries(self):
    for item in export.all_items_dump:
      for k, v in item:
        if v:
          self.make_query(k, v)

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

    self.make_all_info_dict()

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

      # all_items_l_dict[]


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

  c = Collections()
  export = Export()
  # export.()
  # export.print_items_info()
  # export.all_items_fields()
  # export.all_coll()
  # export.get_all()
  # export.get_all_collections()
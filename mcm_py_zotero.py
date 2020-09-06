#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzotero import zotero
from collections import defaultdict

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
    pass

class Export:
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

    self.all_items_l_dict = []

    # self.all_items_dump = self.dump_all_items()
    # debug short
    self.all_items_dump = zot.top(limit = 5)

    self.all_items_fields = set()
    self.get_all_zotero_fields()

    self.make_all_info_dict()

    # self.all_coll_fields = set()

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

      for creator in item['data']['creators']:
        temp_dict['creatorType'] = creator['creatorType'] #'role'?
        temp_dict = self.make_temp_dict(temp_dict, creator)

      self.all_items_l_dict.append(temp_dict)
      # self.zotero_to_sql_fields

  def make_temp_dict(self, temp_dict, in_item_dict):
    for k, v in in_item_dict.items():
      if params and not isinstance(params, (tuple, list)):

      try:
        field_name = self.zotero_to_sql_fields[k]
        temp_dict[field_name] = in_item_dict[k]
      except KeyError:
        temp_dict[k] = in_item_dict[k]
    return temp_dict

  # def make_temp_dict(self, temp_dict, field_lookup, in_item_dict):
  #   for k, v in field_lookup.items():
  #     try:
  #       temp_dict[v] = in_item_dict[k]
  #     except KeyError:
  #       pass
  #   return temp_dict

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

  c = Collections()
  z = Export()
  # z.()
  # z.print_items_info()
  # z.all_items_fields()
  # z.all_coll()
  # z.get_all()
  # z.get_all_collections()
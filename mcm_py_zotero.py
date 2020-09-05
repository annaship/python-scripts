#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzotero import zotero

"""
    [account_type] => group
    [account_id] => 1415490
    [start] => 
    [api_key] => U4CPfWiKzcs7iyJV9IdPnEZU
"""


class Export:
  def __init__(self):

    library_id = "1415490"
    library_type = "group"
    api_key = "U4CPfWiKzcs7iyJV9IdPnEZU"

    self.zot = zotero.Zotero(library_id, library_type, api_key)

    self.all_items_keys = set()
    self.all_coll_fields = set()

  def print_items_info(self):
    items = self.zot.top(limit = 5)
    # we've retrieved the latest five top-level items in our library
    # we can print each item's item type and ID
    for item in items:
      self.all_items_keys.add(item['data']['key'])
      print('Item Type: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

  def all_coll(self):
    all_coll = self.zot.all_collections()
    for coll in all_coll:
      curr_keys = coll['data'].keys()
      self.all_coll_fields = self.all_coll_fields | set(curr_keys)

  def get_all(self):
    dump_all = open('dump_all.txt', 'w')
    # gen = self.zot.makeiter(self.zot.top(limit = 5))
    # gen.next()  # this will return the first five items
    # print(self.zot.everything(self.zot.top()))
    print(self.zot.everything(self.zot.top()), file = dump_all)
    dump_all.close()


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.csv

  z = Export()
  z.print_items_info()
  # z.all_items_keys()
  z.all_coll()
  z.get_all()
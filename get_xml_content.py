#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.dom import minidom

# https://stackabuse.com/reading-and-writing-xml-files-in-python/
# # from xml.dom import minidom
#
# # parse an xml file by name
# mydoc = minidom.parse('items.xml')
#
# items = mydoc.getElementsByTagName('item')
#
# # one specific item attribute
# print('Item #2 attribute:')
# print(items[1].attributes['name'].value)
#
# # all item attributes
# print('\nAll attributes:')
# for elem in items:
#     print(elem.attributes['name'].value)
#
# # one specific item's data
# print('\nItem #2 data:')
# print(items[1].firstChild.data)
# print(items[1].childNodes[0].data)
#
# # all items data
# print('\nAll item data:')
# for elem in items:
#     print(elem.firstChild.data)


class Read_xml:
  def __init__(self):
    self.in_file_name = "/Users/ashipunova/work/MCM/zotero_pulls/zotero_results.xml"
    self.mydoc = minidom.parse(self.in_file_name)


if __name__ == '__main__':
  read_xml = Read_xml()
  
  items = read_xml.mydoc.getElementsByTagName('entry')
  # # all item attributes
  print('\nAll attributes:')
  for elem in items:
      print(elem.attributes['content'].value)
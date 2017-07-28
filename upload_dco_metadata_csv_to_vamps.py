#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import MySQLdb
import csv
import sys
from collections import defaultdict

class Metadata():
  # parse csv
  # separate required from custom
  # find ids by value
  # find and print errors
  
  def __init__(self):
    self.get_data_from_csv()
    self.get_required_fields_names()
    
  def get_data_from_csv(self):
    # TODO: get from args
    file_name = "/Users/ashipunova/Downloads/metadata-project_DCO_GAI_Bv3v5_AnnaSh_1501274966258.csv"
    csv_file_fields, csv_file_content = utils.read_csv_into_list(file_name)
    print "csv_file_fields = "
    # print csv_file_fields
    
    print "csv_file_content = "
    # print csv_file_content
    
  def get_required_fields_names(self):
    #required_metadata_info
    # pass
    table_name = "required_metadata_info"
    query = """
      SELECT COLUMN_NAME 
      FROM INFORMATION_SCHEMA.COLUMNS 
      WHERE TABLE_SCHEMA='vamps2' 
          AND TABLE_NAME='%s'; 
    """ % table_name
    print query
    
    field_names = mysql_utils.execute_fetch_select(query)
    print field_names
    
    
  def get_custom_field_names(self):
    pass

class Upload():
  # check if all custom fields are in custom_metadata_fields and custom_metadata_##
  # upload custom data
  # upload required data
  
  def __init__(self):
    pass

if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  metadata = Metadata()
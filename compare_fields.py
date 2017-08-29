#! /usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2017, Marine Biological Laboratory

from collections import defaultdict
from timeit import timeit
# print timeit("forin()", forin, number = 100)
import util
import MySQLdb

class Fields:
    def __init__(self, fname_all_fields, fname_exist_fields):
      # print all_fields, exist_fields
      self.fname_all_fields = fname_all_fields
      self.fname_exist_fields = fname_exist_fields
      self.pid_fields_dict = defaultdict(list)
      self.pid_missing_fields_dict = defaultdict(list)
      self.all_fields = [line.strip() for line in open(self.fname_all_fields, 'r')]
      self.diff_dict = defaultdict(list)
      self.all_missing_fields = set()

    def make_fields_per_pr_dict(self):
      file = open(self.fname_exist_fields)
      for line in file:
        # print line,
        pid, field_name = line.strip().split(",");
        self.pid_fields_dict[pid].append(field_name)

      # print "=" *8
      # print self.pid_fields_dict

    def compare_with_all_fields(self):
      # print "self.all_fields"
      # print self.all_fields
      for pid, f_arr in self.pid_fields_dict.items():
        for f_name in set(self.all_fields):
          if f_name not in set(f_arr):
            print "f_name = %s" % (f_name)
            self.diff_dict[pid].append(f_name)
            self.all_missing_fields.add(f_name)

      # for object in set(self.all_fields):
      #     if object in other_set:
      #         return object
      print "self.diff_dict: "
      print self.diff_dict
      print "self.all_missing_fields"
      print self.all_missing_fields

    def get_field_description_for_custom_metadata_fields(self):
      for missing_field in self.all_missing_fields:
        # print "missing_field = %s" % (missing_field)

        query_missing_field = """SELECT field_name, field_units, example FROM custom_metadata_fields
        join project using(project_id)
        WHERE field_name = %s
        AND project like 'DCO%%'
        limit 1
        """ % (missing_field)

        print "query_missing_field"
        print query_missing_field
        res =  mysql_utils.execute_fetch_select(query_missing_field)
        print "res"
        print res
      # return mysql_utils.execute_fetch_select(query_custom_tables)

    def get_field_description_for_custom_metadata_pid(self):
    # custom_metadata_101
      query_column_def = """
        SELECT distinct column_name, data_type FROM information_schema.columns
          WHERE TABLE_NAME LIKE "custom_metadata_%%"
          AND table_schema = "vamps2"
          and column_name in (%s)
          """ % ', '.join(list(self.all_missing_fields))
      print "query_column_def"
      print query_column_def

if __name__ == '__main__':
  fname_all_fields = "all_custom_fields.txt"
  fname_exist_fields = "vampsdb_vamps2_custom_metadata_fields_dco_8-29-17.csv"

  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  fields = Fields(fname_all_fields, fname_exist_fields)
  fields.make_fields_per_pr_dict()
  fields.compare_with_all_fields()
  fields.get_field_description_for_custom_metadata_fields()
  fields.get_field_description_for_custom_metadata_pid()
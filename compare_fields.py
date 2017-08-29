#! /usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2017, Marine Biological Laboratory

from collections import defaultdict
from timeit import timeit
# print timeit("forin()", forin, number = 100)

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
      
      
if __name__ == '__main__':
  fname_all_fields = "all_custom_fields.txt"
  fname_exist_fields = "vampsdb_vamps2_custom_metadata_fields_dco_8-29-17.csv"
  
  # with open(fname_all_fields) as f:
  #   all_fields = f.read()
  # with open(fname_exist_fields) as f:
  #   exist_fields = f.read()
    
  fields = Fields(fname_all_fields, fname_exist_fields)
  fields.make_fields_per_pr_dict()
  fields.compare_with_all_fields()
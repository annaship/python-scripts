#! /usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2017, Marine Biological Laboratory

from collections import defaultdict

class Fields:
    def __init__(self, all_fields, exist_fields):
      # print all_fields, exist_fields
      self.all_fields = all_fields
      self.exist_fields = exist_fields
      self.pid_fields_dict = defaultdict(list)
      self.pid_missing_fields_dict = defaultdict(list)
      
      
    def make_fields_per_pr_dict(self):
      # '879,"temperature"\n'
      for line in self.exist_fields:
        pid, field_name = line.strip().split(",");
        try:
          self.pid_fields_dict[pid].append(field_name)
        # except KeyError:
        #   self.pid_fields_dict[pid] = []
        except:
          raise
        # print pid, field_name
        
      print self.pid_fields_dict
      
    def compare_with_all_fields(self):
      for line in self.all_fields:
        print "line"
        print line.strip()
      
      
      
      
if __name__ == '__main__':
  fname_all_fields = "all_fields.txt"
  fname_exist_fields = "vampsdb_vamps2_custom_metadata_fields_dco_8-29-17.csv"
  
  with open(fname_all_fields) as f:
    all_fields = f.readlines()
  with open(fname_exist_fields) as f:
    exist_fields = f.readlines()
    
  fields = Fields(all_fields, exist_fields)
  fields.make_fields_per_pr_dict()
  fields.compare_with_all_fields()
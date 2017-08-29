#! /usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2017, Marine Biological Laboratory

from collections import defaultdict

class Fields:
    def __init__(self, fname_all_fields, fname_exist_fields):
      # print all_fields, exist_fields
      self.fname_all_fields = fname_all_fields
      self.fname_exist_fields = fname_exist_fields
      self.pid_fields_dict = defaultdict(list)
      self.pid_missing_fields_dict = defaultdict(list)
      self.all_fields = []
      
      
    def make_fields_per_pr_dict(self):
      file = open(self.fname_exist_fields) 
      for line in file: 
        # print line,
        pid, field_name = line.strip().split(",");
        self.pid_fields_dict[pid].append(field_name)
      
      print "=" *8
      print self.pid_fields_dict
      
    def compare_with_all_fields(self):
      file_all_fields = open(self.fname_all_fields, 'r')
      # print type(file_all_fields)
      
      # with open(self.fname_all_fields, 'r') as f:
      #   data = f.readlines()
      # print data
      # print type(data)
      
      # for line in file_all_fields:
      #   self.all_fields.append(line.strip())
        
      self.all_fields = [line.strip() for line in file_all_fields]
      #   # print "line"
      print self.all_fields,
        
      # for line in self.all_fields:
      # print "line"
      # print self.all_fields
      
      
      
      
if __name__ == '__main__':
  fname_all_fields = "all_fields.txt"
  fname_exist_fields = "vampsdb_vamps2_custom_metadata_fields_dco_8-29-17.csv"
  
  # with open(fname_all_fields) as f:
  #   all_fields = f.read()
  # with open(fname_exist_fields) as f:
  #   exist_fields = f.read()
    
  fields = Fields(fname_all_fields, fname_exist_fields)
  fields.make_fields_per_pr_dict()
  fields.compare_with_all_fields()
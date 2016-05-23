#! /opt/local/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2016, Marine Biological Laboratory
import sys
import re

class Entry:
    def __init__(self, line):

      self.orig_name                = line.split(",")[0].strip()
      self.clean_name               = line.split(",")[1].strip()
      self.number_of_ranks          = len(self.orig_name.split(";"))
      self.last_rank_from_orig_name = self.orig_name.split(";")[-1]
      self.domain, self.phylum, self.class_r, self.order, self.family, self.rest = self.orig_name.split(";", 5)
      self.genus                    = self.rest.split(";")[0]
      self.genus_name_from_last     = self.last_rank_from_orig_name.split()[0]
      self.species                  = self.last_rank_from_orig_name.split()[1]
      self.strain                   = ""
      
      try:
        self.species_sp             = self.last_rank_from_orig_name.split(" sp. ")[1]
      except:
        self.species_sp             = ""
      
      try:
        self.strain_name            = self.last_rank_from_orig_name.split()[2:]
      except:
        self.strain_name            = ""
                  
    def print_all(self):
      print "=" * 20
      print "line = %s" % line
      print "self.domain = %s" % self.domain
      print "self.phylum = %s" % self.phylum
      print "self.class_r = %s" % self.class_r
      print "self.order = %s" % self.order
      print "self.family = %s" % self.family
      print "self.rest = %s" % self.rest
      print "self.genus = %s" % self.genus
      print "self.genus_name_from_last = %s" % self.genus_name_from_last
      print "self.species = %s" % self.species
      print "self.strain_name = %s" % self.strain_name
      print "self.species_sp = %s" % self.species_sp
      

      
      """
      ~/Dropbox/mix/today_ch/taxonomy/clostridium$ ./make_query.py  | green_grep "self.family" | sort -u
      self.domain  = Bacteria
      self.phylum  = Firmicutes
      self.class_r = Clostridia
      self.order   = Clostridiales
      self.family  = Clostridiaceae 1
      self.family  = Clostridiaceae 2
      self.family  = Clostridiaceae 4
      self.genus_name_from_last = Clostridium      

      self.genus = Clostridium sensu stricto
      self.genus = Clostridium sensu stricto 1
      self.genus = Clostridium sensu stricto 11
      self.genus = Clostridium sensu stricto 12
      self.genus = Clostridium sensu stricto 13
      self.genus = Clostridium sensu stricto 14
      self.genus = Clostridium sensu stricto 15
      self.genus = Clostridium sensu stricto 16
      self.genus = Clostridium sensu stricto 17
      self.genus = Clostridium sensu stricto 18
      self.genus = Clostridium sensu stricto 19
      self.genus = Clostridium sensu stricto 2
      self.genus = Clostridium sensu stricto 3
      self.genus = Clostridium sensu stricto 4
      self.genus = Clostridium sensu stricto 5
      self.genus = Clostridium sensu stricto 6
      self.genus = Clostridium sensu stricto 7

      """
      
    def compare_genus(self):
      if (self.genus != self.genus_name_from_last):
        print "-" * 20
        print "self.genus = %s" % self.genus
        print "self.genus_name_from_last = %s" % self.genus_name_from_last
        print "self.orig_name = %s" % self.orig_name

    def compare_last(self):
      if (" ".join(self.strain_name) != self.species_sp) and (self.strain_name != ['sp.']):
        print "+" * 20
        print "self.strain_name = %s" % self.strain_name
        print "self.species_sp = %s" % self.species_sp
        print "self.orig_name = %s" % self.orig_name
        self.strain = " ".join(self.strain_name)
        
    def new_clean_taxonomy_base(self):
      return self.domain + ";" + self.phylum + ";" + self.class_r + ";" + self.order + ";"


    def new_clean_taxonomy1(self):
      return self.new_clean_taxonomy_base() + self.family.replace(" ", "_") + ";" + self.genus.replace(" ", "_") + ";" + self.species + ";" + "_".join(self.strain_name)

    def new_clean_taxonomy2(self):
      return self.new_clean_taxonomy_base() + self.family.replace(" ", "_") + ";" + self.genus.replace(" ", "_")

      
    def update_query(self, new_line):
      print """
      UPDATE taxonomy_temp
      SET new_clean_taxonomy = "%s"
      WHERE original_taxonomy = "%s"
      AND clean_taxonomy = "%s";
      """ % (new_line, self.orig_name, self.clean_name)
      

if __name__ == '__main__':
  fname = "newbpcdb2_env454_Clostridium_12_5-23-16.csv"

  with open(fname) as f:
    content = f.readlines()

  for line in content:
    try:
      # print "=" * 20
      # print "line = %s" % line
      e = Entry(line)

      # e.print_all()
      
      # e.compare_genus()
      # e.compare_last()
      
      new_line = e.new_clean_taxonomy2()
      # print "new_line = %s" % new_line
      e.update_query(new_line)
      
    except: 
      raise
  

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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
from collections import defaultdict


class Read_xml:
  def __init__(self):
    self.f_path = "/Users/ashipunova/work/MCM/zotero_pulls/"
    self.in_file_name = "zotero_results.xml"
    self.in_full_file_name = os.path.join(self.f_path, self.in_file_name)
    
    # self.mydoc = minidom.parse(os.path.join(self.f_path, self.in_file_name))
    self.out_file_names = []    
    self.cnt = 0
    self.all_xml = defaultdict(int)

    self.read_file()
  


  def read_file(self):
    in_f = open(self.in_full_file_name, 'r')
    for line in in_f:
      # print(x)
      # line = in_f.readline()
      if "?xml version=" in line:
        self.cnt += 1
        self.all_xml[self.cnt] = line
      else:
        self.all_xml[self.cnt] = self.all_xml[self.cnt] + line
       
    print("done")

  #
  #
  # def write_separate_refid(self, line, out_file):
  #   for r in line[1].strip('"').split(","):
  #     out_file.write("%s,%s" % (line[0], r))
  #     out_file.write("\n")
  #
  # def create_rep_id_refhvr_id_temp(self):
  #   query = """CREATE TABLE IF NOT EXISTS rep_id_refhvr_id_temp
  #     (
  #       rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
  #       rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
  #       refhvr_id varchar(32) NOT NULL,
  #       UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
  #     )
  #
  #     """
  #   print(query)
  #   return mysql_utils.execute_no_fetch(query)
  #
  # # step 3
  # def load_into_rep_id_refhvr_id_temp(self, out_file_path_name):
  #   query = "LOAD DATA LOCAL INFILE '%s' IGNORE INTO TABLE rep_id_refhvr_id_temp  FIELDS TERMINATED BY ',' IGNORE 1 LINES (rep_id, refhvr_id);" % (out_file_path_name)
  #   return mysql_utils.execute_no_fetch(query)
  #   #TODO: remove files
  #
  # def drop_col_refids_per_dataset_temp(self, column_names_arr):
  #   # query = """ALTER TABLE refids_per_dataset_temp
  #   #   drop column project,
  #   #   drop column dataset,
  #   #   drop column refhvr_ids;
  #   #   """
  #   l = len(column_names_arr)
  #   query = "ALTER TABLE refids_per_dataset_temp drop column %s" % column_names_arr[0]
  #   if l > 1:
  #     for x in range(1, l):
  #       query += ", drop column %s" % (column_names_arr[x])
  #   print(query)
  #   return mysql_utils.execute_no_fetch(query)
  #
  #
  # def foreign_key_rep_id_refhvr_id_temp(self):
  #   query = """ALTER TABLE rep_id_refhvr_id_temp
  #     ADD FOREIGN KEY (rep_id) REFERENCES refids_per_dataset_temp (rep_id);
  #     """
  #   print(query)
  #   return mysql_utils.execute_no_fetch(query)
  #
  # def rename_table(self, table_name_from, table_name_to):
  #   query = "RENAME TABLE %s TO %s;" % (table_name_from, table_name_to)
  #   print(query)
  #   return mysql_utils.execute_no_fetch(query)
  #
  # def benchmark_w_return_1(self):
  #   print("\n")
  #   print("-" * 10)
  #   return time.time()
  #
  # def benchmark_w_return_2(self, t0):
  #   t1 = time.time()
  #   total = float(t1-t0) / 60
  #   print('time: %.2f m' % total)
  #   #
  #   # print("time_res = %s s" % total)
  #

if __name__ == '__main__':
  text_c = Read_xml()
  
  
  # utils = util.Utils()
  #
  # if (utils.is_local() == True):
  #   # mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps", read_default_group = "clientservers")
  #   mysql_utils = util.Mysql_util(host = "localhost", db = "test_vamps", read_default_group = "clienthome")
  # else:
  #   mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps", read_default_group = "client")
  #
  # csv_dir      = "/usr/local/tmp"
  # in_filename  = "rep_id_refhvr_ids"
  # file_extension = ".csv"
  # out_file_extension = ".separated"
  #
  # # query = "show tables"
  # # a = mysql_utils.execute_fetch_select(query)
  #
  # update_refhvr_ids = Update_refhvr_ids()
  # # print("AAA")
  # # !!! Uncomment !!!
  #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # update_refhvr_ids.drop_table("refids_per_dataset_temp")
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("create_table_refids_per_dataset_temp")
  # # update_refhvr_ids.create_table_refids_per_dataset_temp()
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("insert_refids_per_dataset_temp")
  # #
  # # rowcount, lastrowid = update_refhvr_ids.insert_refids_per_dataset_temp()
  # # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("get_dataset_id")
  # # rowcount, lastrowid = update_refhvr_ids.get_dataset_id()
  # # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("get_project_id")
  # # rowcount, lastrowid = update_refhvr_ids.get_project_id()
  # # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("foreign_key_refids_per_dataset_temp")
  # # rowcount, lastrowid = update_refhvr_ids.foreign_key_refids_per_dataset_temp()
  # # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  # #
  # # t0 = update_refhvr_ids.benchmark_w_return_1()
  # # print("drop_col_refids_per_dataset_temp")
  # # rowcount, lastrowid = update_refhvr_ids.drop_col_refids_per_dataset_temp(["project", "dataset"])
  # # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # print("get_all_counts")
  # update_refhvr_ids.all_ref_counts = update_refhvr_ids.get_all_counts()
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # print("create_file_names")
  # update_refhvr_ids.create_file_names()
  # print(update_refhvr_ids.in_file_names)
  # print(update_refhvr_ids.out_file_names)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # """  rep_id_refhvr_id  """
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.drop_table("rep_id_refhvr_id_temp")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.create_rep_id_refhvr_id_temp()
  # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # print("process_data")
  # update_refhvr_ids.process_data()
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.drop_col_refids_per_dataset_temp(["refhvr_ids"])
  # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.foreign_key_rep_id_refhvr_id_temp()
  # print("rowcount = %s, lastrowid = %s" % (rowcount, lastrowid))
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.drop_table("rep_id_refhvr_id_previous")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.drop_table("refids_per_dataset_previous")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.rename_table("rep_id_refhvr_id", "rep_id_refhvr_id_previous")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.rename_table("refids_per_dataset", "refids_per_dataset_previous")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.rename_table("refids_per_dataset_temp", "refids_per_dataset")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.rename_table("rep_id_refhvr_id_temp", "rep_id_refhvr_id")
  # update_refhvr_ids.benchmark_w_return_2(t0)

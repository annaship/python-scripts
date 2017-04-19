#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import time
import csv, os

class Update_refhvr_ids:
  def __init__(self):
    self.write_separate_refids_arr = []
    
  def drop_table(self, table_name):
    query = "DROP TABLE IF EXISTS %s;" % (table_name)
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def create_table_refids_per_dataset_temp(self):
    query = """CREATE TABLE IF NOT EXISTS refids_per_dataset_temp
    (
      refids_per_dataset_id int unsigned NOT NULL AUTO_INCREMENT primary key,
      frequency double NOT NULL DEFAULT '0' COMMENT 'sum seq_count (for this seq/project/dataset across all lines and runs) divided by dataset_count',
      project varchar(32) NOT NULL,
      dataset varchar(64) NOT NULL DEFAULT '',
      refhvr_ids text NOT NULL,
      seq_count int(11) unsigned NOT NULL COMMENT 'sum seq_count for this seq/project/dataset across all lines and runs',
      distance decimal(7,5) DEFAULT NULL COMMENT 'gast_distance AS distance',
      rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
      dataset_count mediumint(8) unsigned NOT NULL COMMENT 'number of reads in the dataset',
      dataset_id smallint(5) unsigned NOT NULL,
      project_id mediumint(5) unsigned NOT NULL,
      UNIQUE KEY rep_id (rep_id),
      key dataset (dataset),
      key project (project)
    );

    """
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def insert_refids_per_dataset_temp(self):    
    # use for testing with short vamps_sequences_transfer_temp
    query = """INSERT IGNORE INTO refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)    
      SELECT frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count
        FROM vamps_sequences_transfer_temp
    """
    # real  57m45.418s

    print query
    return mysql_utils.execute_no_fetch(query)
        
  def get_dataset_id(self):
    query = """UPDATE refids_per_dataset_temp
        JOIN new_dataset using(dataset)
        SET refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
    """
    print query
    return mysql_utils.execute_no_fetch(query)

  def get_project_id(self):
    query = """UPDATE refids_per_dataset_temp
        JOIN new_project using(project)
        SET refids_per_dataset_temp.project_id = new_project.project_id;
    """
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def foreign_key_refids_per_dataset_temp(self):
    query = """ALTER TABLE refids_per_dataset_temp
      ADD  FOREIGN KEY (`project_id`) REFERENCES `new_project` (`project_id`),
      ADD  FOREIGN KEY (`dataset_id`) REFERENCES `new_dataset` (`dataset_id`)
      ;
      """
    print query
    return mysql_utils.execute_no_fetch(query)
    
  # def get_rep_id_refhvr_ids(self):
  #   query = "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp"
  #   print query
  #   return mysql_utils.execute_fetch_select(query)
    
  # def write_to_csv_file(self, in_file_path_name, res, file_mode = "wb"):
  def write_to_csv_file(self, in_file_path_name, file_mode = "wb"):
    query = "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp"
    mysql_utils.cursor.execute(query)
    data_from_db = []
    for result in mysql_utils.result_iter(mysql_utils.cursor):
      data_from_db_temp = result
      print "WWW"
      print data_from_db_temp
      data_from_db.append(data_from_db_temp)
      # with open(in_file_path_name, "a") as csv_file:
      #   csv_writer = csv.writer(csv_file)
      #   csv_writer.writerows(data_from_db)
      
    
    
    # get_rep_id_refhvr_ids
    # data_from_db, field_names = res
    # print "VVVV"
    # print field_names
    print data_from_db

    with open(in_file_path_name, file_mode) as csv_file:
      csv_writer = csv.writer(csv_file)
      csv_writer.writerows(data_from_db)
      
  def process_file(self, in_file_path_name, out_file):
    with open(in_file_path_name, 'rb') as in_f:
      reader = csv.reader(in_f)
      for line in reader:  
        self.write_separate_refid(line, out_file)
          
  def write_separate_refid(self, line, out_file):
    for r in line[1].strip('"').split(","):
      out_file.write("%s,%s" % (line[0], r))
      out_file.write("\n")
        
  def create_rep_id_refhvr_id_temp(self):
    query = """CREATE TABLE IF NOT EXISTS rep_id_refhvr_id_temp
      (
        rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
        rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
        refhvr_id varchar(32) NOT NULL,
        UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
      )
  
      """
    print query
    return mysql_utils.execute_no_fetch(query)
  
  def load_into_rep_id_refhvr_id_temp(self, out_file_path_name):
    query = "LOAD DATA LOCAL INFILE '%s' IGNORE INTO TABLE rep_id_refhvr_id_temp  FIELDS TERMINATED BY ',' (rep_id, refhvr_id);" % (out_file_path_name)
    print query
    return mysql_utils.execute_no_fetch(query)
  
  def drop_col_refids_per_dataset_temp(self, column_names_arr):
    # query = """ALTER TABLE refids_per_dataset_temp
    #   drop column project,
    #   drop column dataset,
    #   drop column refhvr_ids;
    #   """
    l = len(column_names_arr)
    query = "ALTER TABLE refids_per_dataset_temp drop column %s" % column_names_arr[0]
    if len > 1:
      for x in range(1, l):
        query += ", drop column %s" % (column_names_arr[x])
    print query
    return mysql_utils.execute_no_fetch(query)

  
  def foreign_key_rep_id_refhvr_id_temp(self):
    query = """ALTER TABLE rep_id_refhvr_id_temp
      ADD FOREIGN KEY (rep_id) REFERENCES refids_per_dataset_temp (rep_id);
      """
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def rename_table(self, table_name_from, table_name_to):
    query = "RENAME TABLE %s TO %s;" % (table_name_from, table_name_to)
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def benchmark_w_return_1(self):
    print  "\n"
    print "-" * 10
    return time.time()
    
  def benchmark_w_return_2(self, t0):
    t1 = time.time()
    total = float(t1-t0) / 60
    print 'time: %.2f m' % total
    #
    # print "time_res = %s s" % total
    
    
if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps", read_default_group = "clientservers")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps", read_default_group = "client")
    
  csv_dir      = "/tmp"
  in_filename  = "rep_id_refhvr_ids.csv"
  out_filename = "rep_id_refhvr_ids_separated.csv"
  in_file_path_name  = os.path.join(csv_dir, in_filename)
  out_file_path_name = os.path.join(csv_dir, out_filename)
  print in_file_path_name
  print out_file_path_name
  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  
  update_refhvr_ids = Update_refhvr_ids()
  # print "AAA"
  # !!! Uncomment !!!
  
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.drop_table("refids_per_dataset_temp")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.create_table_refids_per_dataset_temp()
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.insert_refids_per_dataset_temp()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.get_dataset_id()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.get_project_id()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.foreign_key_refids_per_dataset_temp()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.drop_col_refids_per_dataset_temp(["project", "dataset"])
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)

  """  rep_id_refhvr_id  """
  
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # db_res = update_refhvr_ids.get_rep_id_refhvr_ids()
  # # TODO
  # # do mysql dump to file instead, by chunks 
  # #  combine with write_to_csv_file
  # print "db_res[0][0]"
  # update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  print "write_to_csv_file"
  # update_refhvr_ids.write_to_csv_file(in_file_path_name, db_res)
  update_refhvr_ids.write_to_csv_file(in_file_path_name)
  update_refhvr_ids.benchmark_w_return_2(t0)

  t0 = update_refhvr_ids.benchmark_w_return_1()
  print "process_file"
  
  out_f = open(out_file_path_name, "w")
  update_refhvr_ids.process_file(in_file_path_name, out_f)
  update_refhvr_ids.benchmark_w_return_2(t0)
  out_f.close()

  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.drop_table("rep_id_refhvr_id_temp")
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  rowcount, lastrowid = update_refhvr_ids.create_rep_id_refhvr_id_temp()
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  rowcount, lastrowid = update_refhvr_ids.load_into_rep_id_refhvr_id_temp(out_file_path_name)
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  update_refhvr_ids.benchmark_w_return_2(t0)
  #
  t0 = update_refhvr_ids.benchmark_w_return_1()
  rowcount, lastrowid = update_refhvr_ids.drop_col_refids_per_dataset_temp(["refhvr_ids"])
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  rowcount, lastrowid = update_refhvr_ids.foreign_key_rep_id_refhvr_id_temp()
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.drop_table("rep_id_refhvr_id_previous")
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.drop_table("refids_per_dataset_previous")
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.rename_table("rep_id_refhvr_id", "rep_id_refhvr_id_previous")
  update_refhvr_ids.benchmark_w_return_2(t0)
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.rename_table("refids_per_dataset", "refids_per_dataset_previous")
  update_refhvr_ids.benchmark_w_return_2(t0)
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.rename_table("refids_per_dataset_temp", "refids_per_dataset")
  update_refhvr_ids.benchmark_w_return_2(t0)
  t0 = update_refhvr_ids.benchmark_w_return_1()
  update_refhvr_ids.rename_table("rep_id_refhvr_id_temp", "rep_id_refhvr_id")
  update_refhvr_ids.benchmark_w_return_2(t0)

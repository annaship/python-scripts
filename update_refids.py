#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util
import time
import csv

class Update_refhvr_ids:
  def __init__(self):
    self.separate_refids_arr = []
    
  def drop_table(self, table_name):
    query = "DROP TABLE IF EXISTS %s;" % (table_name)
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def create_table_refids_per_dataset_temp(self):
    query = """CREATE TABLE refids_per_dataset_temp
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
    
  def get_rep_id_refhvr_ids(self):
    query = "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp"
    print query
    return mysql_utils.execute_fetch_select(query)
    
  def write_to_csv_file(self, file_name, res, file_mode = "wb"):
    data_from_db, field_names = res
    # print "VVVV"
    # print field_names

    with open(file_name, file_mode) as csv_file:
      csv_writer = csv.writer(csv_file)
      # if file_mode == "wb":
      #   csv_writer.writerow(field_names) # write headers
      csv_writer.writerows(data_from_db)
      
  def process_file(self, in_filename, out_file):
    with open(in_filename, 'rb') as in_f:
      reader = csv.reader(in_f)
      for line in reader:  
        self.separate_refid(line, out_file)
        
  def process_data(self, line):
    print "AAA line"
    print line
    
  def separate_refid(self, line, out_file):
    # print line
    for r in line[1].strip('"').split(","):
      out_file.write("%s,%s" % (line[0], r))
      out_file.write("\n")
      # print "%s,%s" % (line[0], r)

    
  # def write_file(lines):
  #   f = open('myfile','w')
  #   f.write('hi there\n') # python will convert \n to os.linesep
  #   f.close()
  # TODO: read csv instead?
  
  # def write_data(line):
  #   for r in line[1].strip('"').split(","):
  #     print "%s,%s" % (line[0], r)
  #
  # for line in open(filename):
  #     process_data(line.split())

  def separate_refids(self, res):
    for line in res:
      for r in line[1].split(","):
        self.separate_refids_arr.append((int(line[0]), r))
        
  def create_rep_id_refhvr_id_temp(self):
    query = """CREATE table rep_id_refhvr_id_temp
      (
        rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY,
        rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
        refhvr_id varchar(32) NOT NULL,
        UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
      )
  
      """
    print query
    return mysql_utils.execute_no_fetch(query)
    
  def insert_into_rep_id_refhvr_id_temp(self):
    separate_refids_string = str(self.separate_refids_arr).strip('[]')

    query = """INSERT IGNORE INTO rep_id_refhvr_id_temp (rep_id, refhvr_id)
      VALUES %s; 
    """ % separate_refids_string
    print "INSERT IGNORE INTO rep_id_refhvr_id_temp\nSeparate fields len: "
    print len(self.separate_refids_arr)
    # print query
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
    total = t1-t0
    print 'time: %.2f s' % total
    #
    # print "time_res = %s s" % total
    
    
if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps", read_default_group = "clientservers")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps", read_default_group = "client")
    
  in_filename  = "rep_id_refhvr_ids.csv"
  out_filename = "rep_id_refhvr_ids_separated.csv"
  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  
  update_refhvr_ids = Update_refhvr_ids()
  # print "AAA"
  # !!! Uncomment !!!
  
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # update_refhvr_ids.drop_table("rep_id_refhvr_id_temp")
  # update_refhvr_ids.benchmark_w_return_2(t0)
  # 
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
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  db_res = update_refhvr_ids.get_rep_id_refhvr_ids()
  print "db_res[0][0]"
  # res, field_names = update_refhvr_ids.get_rep_id_refhvr_ids()
  # print field_names
  update_refhvr_ids.benchmark_w_return_2(t0)
  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  print "write_to_csv_file"
  update_refhvr_ids.write_to_csv_file("rep_id_refhvr_ids.csv", db_res)
  update_refhvr_ids.benchmark_w_return_2(t0)

  
  t0 = update_refhvr_ids.benchmark_w_return_1()
  print "process_file"
  out_f = open(out_filename, "w")
  update_refhvr_ids.process_file(in_filename, out_f)
  update_refhvr_ids.benchmark_w_return_2(t0)
  out_f.close()

  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # print "separate_refids"
  # update_refhvr_ids.separate_refids(res)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.create_rep_id_refhvr_id_temp()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.insert_into_rep_id_refhvr_id_temp()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.drop_col_refids_per_dataset_temp(["refhvr_ids"])
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # update_refhvr_ids.benchmark_w_return_2(t0)
  #
  # t0 = update_refhvr_ids.benchmark_w_return_1()
  # rowcount, lastrowid = update_refhvr_ids.foreign_key_rep_id_refhvr_id_temp()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
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


"""
from scratch
  second part
  
---
vamps

time mysql -h vampsdb vamps -e "SELECT rep_id, refhvr_ids FROM refids_per_dataset" | tail -n+2 >rep_id_refhvr_ids.csv
real	7m41.957s

create table rep_id_refhvr_id
(
  rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT primary key,
  rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
  refhvr_id varchar(16) NOT NULL,
  UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
)

/workspace/ashipunova/refhvrid$ 
time cat rep_id_refhvr_ids.csv | tail -n+2 >rep_id_refhvr_ids1.csv
real	1m35.578s

time python separate_refids.py rep_id_refhvr_ids1.csv > rep_id_refhvr_ids_separated.csv; mail_done
real	22m35.823s

time mysql -h vampsdb vamps -e "LOAD DATA LOCAL INFILE '/workspace/ashipunova/refhvrid/rep_id_refhvr_ids_separated.csv' IGNORE INTO TABLE rep_id_refhvr_id  FIELDS TERMINATED BY ',' (rep_id, refhvr_id);"; mail_done
jake
real    84m21.264s

SELECT count(rep_id)
FROM rep_id_refhvr_id
298578304

SELECT count(rep_id)
FROM refids_per_dataset
230039552

alter table refids_per_dataset
drop column refhvr_ids
arthur
Query OK, 0 rows affected (1 hour 38 min 11.67 sec)

alter table rep_id_refhvr_id
add FOREIGN KEY (`rep_id`) REFERENCES `refids_per_dataset` (`rep_id`)
arthur
Query OK, 298578304 rows affected (3 hours 11 min 7.93 sec)

less -N /usr/local/www/vamps/docs/vamps/common_code/taxonomy/crosstab.php

less -N /usr/local/www/vamps/docs/vamps/sequences/just_local_gis.php

===
time mysql -h vampsdb vamps -e "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp" | tail -n+2 >rep_id_refhvr_ids.csv
jake
real    16m29.463s
-- real  7m41.957s

create table rep_id_refhvr_id_temp
(
  rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT primary key,
  rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
  refhvr_id varchar(16) NOT NULL,
  UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
)
done

/workspace/ashipunova/refhvrid$ 
time cat rep_id_refhvr_ids.csv | tail -n+2 >rep_id_refhvr_ids1.csv
-- real  1m35.578s
real	0m46.172s

time python separate_refids.py rep_id_refhvr_ids1.csv > rep_id_refhvr_ids_separated.csv; mail_done
-- real  22m35.823s
jake screen
real    108m43.848s

time mysql -h vampsdb vamps -e "LOAD DATA LOCAL INFILE '/workspace/ashipunova/refhvrid/rep_id_refhvr_ids_separated.csv' IGNORE INTO TABLE rep_id_refhvr_id_temp  FIELDS TERMINATED BY ',' (rep_id, refhvr_id);"; mail_done
-- jake
-- real    84m21.264s
artur
Query OK, 312817494 rows affected, 65535 warnings (1 hour 37 min 44.84 sec)
| Warning | 1265 | Data truncated for column 'refhvr_id' at row 157971 |

once)
alter table rep_id_refhvr_id
change column refhvr_id `refhvr_id` varchar(32) NOT NULL
Records: 312817494  Duplicates: 0  Warnings: 0

SELECT count(rep_id)
FROM rep_id_refhvr_id_temp
-- 298578304
|     312817494 |
+---------------+
1 row in set (1 min 29.60 sec)

SELECT count(rep_id)
FROM refids_per_dataset_temp
-- 230039552
|     240594962 |
+---------------+
1 row in set (8 min 13.48 sec)

alter table refids_per_dataset_temp
drop column project,
drop column dataset,
drop column refhvr_ids


alter table refids_per_dataset_temp
drop column project,
drop column dataset
-- Query OK, 0 rows affected (1 hour 49 min 18.73 sec)
Query OK, 0 rows affected (1 hour 57 min 47.58 sec)

alter table refids_per_dataset_temp
drop column refhvr_ids
-- arthur
-- Query OK, 0 rows affected (1 hour 38 min 11.67 sec)
Query OK, 0 rows affected (1 hour 28 min 43.88 sec)


alter table rep_id_refhvr_id_temp
add FOREIGN KEY (`rep_id`) REFERENCES `refids_per_dataset_temp` (`rep_id`)
-- arthur
-- Query OK, 298578304 rows affected (3 hours 11 min 7.93 sec)
Query OK, 312817494 rows affected (7 hours 47 min 52.72 sec)


less -N /usr/local/www/vamps/docs/vamps/common_code/taxonomy/crosstab.php

less -N /usr/local/www/vamps/docs/vamps/sequences/just_local_gis.php
===
done)
check if 
KEY `pr_dataset` (`project_id`,`dataset_id`)
is faster for refids_per_dataset then project_id
same
===
drop table rep_id_refhvr_id_previous;
drop table refids_per_dataset_previous;

RENAME TABLE rep_id_refhvr_id TO rep_id_refhvr_id_previous;
RENAME TABLE refids_per_dataset TO refids_per_dataset_previous;
RENAME TABLE refids_per_dataset_temp TO refids_per_dataset;
RENAME TABLE rep_id_refhvr_id_temp TO rep_id_refhvr_id;

"""
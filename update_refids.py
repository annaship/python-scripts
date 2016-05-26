#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util

class Update_refhvr_ids:
  def __init__(self):
    self.separate_refids_arr = []
    
  def drop_table(self, table_name):
    query = "DROP TABLE IF EXISTS %s;" % (table_name)
    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
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
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def insert_refids_per_dataset_temp_from_seq_temp(self):    
    # use for testing with short vamps_sequences_transfer_temp
    query = """INSERT IGNORE INTO refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)    
      SELECT frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count
        FROM vamps_sequences_transfer_temp
    """
    # real  57m45.418s

    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def insert_refids_per_dataset_temp(self):      
    query = """INSERT IGNORE INTO refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)    
      SELECT DISTINCT v.frequency, v.project, v.dataset, v.refhvr_ids, v.seq_count, v.distance, v.rep_id, vamps_projects_datasets.dataset_count
        FROM vamps_sequences v
        JOIN vamps_projects_datasets USING(project, dataset)
    ;
    """
    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def get_dataset_id(self):
    query = """UPDATE refids_per_dataset_temp
        JOIN new_dataset using(dataset)
        SET refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
    """
    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)

  def get_project_id(self):
    query = """UPDATE refids_per_dataset_temp
        JOIN new_project using(project)
        SET refids_per_dataset_temp.project_id = new_project.project_id;
    """
    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  # def 
  """
  alter table refids_per_dataset_temp
    add  FOREIGN KEY (`project_id`) REFERENCES `new_project` (`project_id`),
    add  FOREIGN KEY (`dataset_id`) REFERENCES `new_dataset` (`dataset_id`)
  ;
  """

  # def insert_into_refids_per_dataset(self):
  #   query = """
  #     INSERT IGNORE INTO refids_per_dataset (frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id)
  #       SELECT frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id
  #       from refids_per_dataset_temp
  #   """
  #   print query
  #   return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def get_rep_id_refhvr_ids(self):
    query = "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp"
    print query
    return vampsdev_vamps_mysql_util.execute_fetch_select(query)

  def make_dictionary_from_res(self, res):
    return {line[0]: line[1] for line in res}
    
  def separate_refids(self, d):
    for key, value in d.iteritems():
      for r in value.split(","):
        # print "%s,%s" % (key, r)
        self.separate_refids_arr.append((int(key), r))
    # print "self.separate_refids_arr AAA"
    # print self.separate_refids_arr
    # [(80054275L, 'v6_CB202'), (284705110L, 'v6_BE739'),
        
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
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def insert_into_rep_id_refhvr_id_temp(self):
    separate_refids_string = str(self.separate_refids_arr).strip('[]')

    query = """INSERT IGNORE INTO rep_id_refhvr_id_temp (rep_id, refhvr_id)
      VALUES %s; 
    """ % separate_refids_string
    print query
    return vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
    """
    TODO:
    alter table refids_per_dataset_temp
    drop column project,
    drop column dataset,
    drop column refhvr_ids
    """
    
    """
    TODO:
    alter table rep_id_refhvr_id_temp
    add FOREIGN KEY (`rep_id`) REFERENCES `refids_per_dataset_temp` (`rep_id`)
    """
    
if __name__ == '__main__':
  vampsdev_vamps_mysql_util = util.Mysql_util(host = "vampsdev", db = "vamps", read_default_group = "clientservers")
  query = "show tables"
  a = vampsdev_vamps_mysql_util.execute_fetch_select(query)
  
  update_refhvr_ids = Update_refhvr_ids()
  # print "AAA"
  # !!! Uncomment !!!
  rowcount, lastrowid = update_refhvr_ids.drop_table("refids_per_dataset_temp")
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  rowcount, lastrowid = update_refhvr_ids.create_table_refids_per_dataset_temp()
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  rowcount, lastrowid = update_refhvr_ids.insert_refids_per_dataset_temp()
  print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  
  # rowcount, lastrowid = update_refhvr_ids.get_dataset_id()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # rowcount, lastrowid = update_refhvr_ids.get_project_id()
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
"""  todo:
  alter table refids_per_dataset_temp
    add  FOREIGN KEY (`project_id`) REFERENCES `new_project` (`project_id`),
    add  FOREIGN KEY (`dataset_id`) REFERENCES `new_dataset` (`dataset_id`);
""" 
  # res, field_names = update_refhvr_ids.get_rep_id_refhvr_ids()
  # print field_names
  # rowcount, lastrowid = update_refhvr_ids.separate_refids(update_refhvr_ids.make_dictionary_from_res(res))
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # rowcount, lastrowid = update_refhvr_ids.drop_table("rep_id_refhvr_id_temp") # Don't need it!
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # rowcount, lastrowid = update_refhvr_ids.create_rep_id_refhvr_id_temp() # Don't need it!
  # print "rowcount = %s, lastrowid = %s" % (rowcount, lastrowid)
  # rowcount, lastrowid = update_refhvr_ids.insert_into_rep_id_refhvr_id()
  

"""
from scratch

1)
create table refids_per_dataset_temp
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
  UNIQUE KEY rep_id (rep_id)
)
Query OK, 0 rows affected (0.05 sec)

insert into refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)
  SELECT frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count
  from vamps_sequences_transfer_temp
Query OK, 240594962 rows affected (1 hour 1 min 14.35 sec)
-- Query OK, 230039552 rows affected (59 min 14.20 sec)

vamps
alter table refids_per_dataset_temp
add column `dataset_id` smallint(5) unsigned NOT NULL,
add column  `project_id` mediumint(5) unsigned NOT NULL
Query OK, 0 rows affected (1 hour 17 min 22.66 sec)

alter table refids_per_dataset_temp
add key dataset (dataset),
add key project (project)
Query OK, 0 rows affected (58 min 2.64 sec)

update refids_per_dataset_temp
  join new_dataset using(dataset)
  set refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
Query OK, 240594962 rows affected (1 hour 35 min 2.31 sec)
  -- Query OK, 230039552 rows affected (43 min 56.61 sec)

update refids_per_dataset_temp
  join new_project using(project)
  set refids_per_dataset_temp.project_id = new_project.project_id;
Query OK, 240594962 rows affected (1 hour 2 min 43.20 sec)
-- Query OK, 230039552 rows affected (34 min 34.97 sec)
  
alter table refids_per_dataset_temp
  add  FOREIGN KEY (`project_id`) REFERENCES `new_project` (`project_id`),
  add  FOREIGN KEY (`dataset_id`) REFERENCES `new_dataset` (`dataset_id`);
--   Query OK, 230039552 rows affected (1 hour 7 min 51.52 sec)
Query OK, 240594962 rows affected (1 hour 32 min 55.44 sec)

module load mysql/5.6.12
time mysqldump -h vampsdb vamps refids_per_dataset_temp | gzip > /users/ashipunova/backups/refids_per_dataset_temp.`date '+%m%d%y'`.sql.gz 

2)
time mysql -h vampsdb vamps -e "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp" | tail -n+2 >rep_id_refhvr_ids.csv
jake
real    16m29.463s
-- real  7m41.957s

create table rep_id_refhvr_id_temp
(
  rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT primary key,
  rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
  refhvr_id varchar(32) NOT NULL,
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
RENAME TABLE rep_id_refhvr_id TO rep_id_refhvr_id_previous
RENAME TABLE refids_per_dataset TO refids_per_dataset_previous
RENAME TABLE refids_per_dataset_temp TO refids_per_dataset
RENAME TABLE rep_id_refhvr_id_temp TO rep_id_refhvr_id


"""
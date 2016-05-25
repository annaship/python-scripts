#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util

class Update_refhvr_ids:
  def __init__(self):
    pass
    
  def drop_table(self, table_name):
    query = "DROP TABLE IF EXISTS %s;" % (table_name)
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def create_table_refids_per_dataset_temp(self):
    query = """
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
      dataset_id smallint(5) unsigned NOT NULL,
      project_id mediumint(5) unsigned NOT NULL,
      UNIQUE KEY rep_id (rep_id),
      key dataset (dataset),
      key project (project)
    );

    """
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def insert_refids_per_dataset_temp(self):
    query = """
    insert ignore into refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)    
      select v.frequency, v.project, v.dataset, v.refhvr_ids, v.seq_count, v.distance, v.rep_id, v.dataset_count
        from vamps_sequences_transfer_temp v
        LEFT JOIN refids_per_dataset USING(rep_id)
        WHERE refids_per_dataset.rep_id IS NULL
    """
  
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def get_dataset_id(self):
    query = """
      update refids_per_dataset_temp
        join new_dataset using(dataset)
        set refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
    """
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)

  def get_project_id(self):
    query = """
      update refids_per_dataset_temp
        join new_project using(project)
        set refids_per_dataset_temp.project_id = new_project.project_id;
    """
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)

  def insert_into_refids_per_dataset(self):
    query = """
      insert ignore into refids_per_dataset (frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id)
        select frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id
        from refids_per_dataset_temp
    """
    print query
    vampsdev_vamps_mysql_util.execute_no_fetch(query)
    
  def get_rep_id_refhvr_ids(self):
    query = """
      SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp
    """
    print query
    return vampsdev_vamps_mysql_util.execute_fetch_select(query)
    
    

if __name__ == '__main__':
  vampsdev_vamps_mysql_util = util.Mysql_util(host = "vampsdev", db = "vamps", read_default_group = "clientservers")
  query = "show tables"
  a = vampsdev_vamps_mysql_util.execute_fetch_select(query)
  
  update_refhvr_ids = Update_refhvr_ids()
  # print "AAA"
  # update_refhvr_ids.drop_table("refids_per_dataset_temp")
  # update_refhvr_ids.create_table_refids_per_dataset_temp()
  # update_refhvr_ids.insert_refids_per_dataset_temp()
  # update_refhvr_ids.get_dataset_id()
  # update_refhvr_ids.get_project_id()
  # update_refhvr_ids.insert_into_refids_per_dataset()
  res, field_names = update_refhvr_ids.get_rep_id_refhvr_ids()
  print field_names
  
  

"""
incremantal

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
  dataset_id smallint(5) unsigned NOT NULL,
  project_id mediumint(5) unsigned NOT NULL,
  UNIQUE KEY rep_id (rep_id),
  key dataset (dataset),
  key project (project)
)

insert ignore into refids_per_dataset_temp (frequency, project, dataset, refhvr_ids, seq_count, distance, rep_id, dataset_count)
select v.frequency, v.project, v.dataset, v.refhvr_ids, v.seq_count, v.distance, v.rep_id, v.dataset_count
  from vamps_sequences_transfer_temp v
  LEFT JOIN refids_per_dataset USING(rep_id)
  WHERE refids_per_dataset.rep_id IS null
no ignore: ERROR 1062 (23000): Duplicate entry '0' for key 'rep_id'
taiga screen
running
date
Wed May 25 10:45:37 EDT 2016
Query OK, 5187270 rows affected, 2 warnings (34 min 58.52 sec)
| Warning | 1364 | Field 'dataset_id' doesn't have a default value |
| Warning | 1364 | Field 'project_id' doesn't have a default value |


update refids_per_dataset_temp
  join new_dataset using(dataset)
  set refids_per_dataset_temp.dataset_id = new_dataset.dataset_id;
Query OK, 5187270 rows affected (1 min 8.08 sec)

update refids_per_dataset_temp
  join new_project using(project)
  set refids_per_dataset_temp.project_id = new_project.project_id;
Query OK, 5187270 rows affected (57.56 sec)

module load mysql/5.6.12
time mysqldump -h vampsdb vamps refids_per_dataset | gzip > /users/ashipunova/backups/refids_per_dataset.`date '+%m%d%y'`.sql.gz 
real	11m43.972s

create refids_per_dataset_previous instead

insert ignore into refids_per_dataset (frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id)
  select frequency, seq_count, distance, rep_id, dataset_count, dataset_id, project_id
  from refids_per_dataset_temp
Query OK, 5187270 rows affected (2 min 24.65 sec)

2)
cd /workspace/ashipunova/refhvrid
time mysql -h vampsdb vamps -e "SELECT rep_id, refhvr_ids FROM refids_per_dataset_temp" | tail -n+2 >rep_id_refhvr_ids_temp.csv
real	0m9.946s

create table rep_id_refhvr_id_temp
(
  rep_id_refhvr_id_id int(10) unsigned NOT NULL AUTO_INCREMENT primary key,
  rep_id int(10) unsigned NOT NULL COMMENT 'sequence_pdr_info_ill_id AS rep_id',
  refhvr_id varchar(16) NOT NULL,
  UNIQUE KEY rep_id_refhvr (rep_id, refhvr_id)
)

/workspace/ashipunova/refhvrid$ 
time cat rep_id_refhvr_ids_temp.csv | tail -n+2 >rep_id_refhvr_ids_temp1.csv
real	0m46.172s

time python separate_refids.py rep_id_refhvr_ids_temp1.csv > rep_id_refhvr_ids_temp_separated.csv; mail_done
real	0m22.348s

time mysql -h vampsdb vamps -e "LOAD DATA LOCAL INFILE '/workspace/ashipunova/refhvrid/rep_id_refhvr_ids_temp_separated.csv' IGNORE INTO TABLE rep_id_refhvr_id  FIELDS TERMINATED BY ',' (rep_id, refhvr_id);"; mail_done
real	1m17.469s

"""
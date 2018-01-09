# from collections import defaultdict
# import time
import util
import MySQLdb
import csv
import sys
from collections import defaultdict


class Sequence():
  """
  uncompress all seq, create new tab
  """
  def __init__(self):
    self.all_cnt_orig = self.get_all_cnt_orig()
    
  def get_all_cnt_orig(self):
    my_sql = "SELECT COUNT(*) FROM sequence_ill;"
    return mysql_utils.execute_fetch_select(my_sql)
    
  def uncompress_all(self):
    chunk_size = 10000
    cnt = 1
    # range(begin,end, step)
    for counter in range(1, int(self.all_cnt_orig[0][0][0]), chunk_size):
      my_sql = """insert ignore into sequence (sequence)
              select distinct uncompress(sequence_comp) as sequence
              from sequence_ill limit %s, %s
              ON DUPLICATE KEY UPDATE sequence = VALUES(sequence)
              """ % (counter, chunk_size)
      print my_sql
      print mysql_utils.execute_no_fetch_w_info(my_sql)

if __name__ == '__main__':

  utils = util.Utils()

  if (utils.is_local() == True):
    host = 'localhost'
    db = 'test_env454'
    read_default_group = 'clienthome'
  else:
    host = "bpcdb1"
    db = 'env454'
    read_default_group = 'client'
  mysql_utils = util.Mysql_util(host = host, db = db, read_default_group = read_default_group)
  # print "host = %s, db = %s" % (host, db)
    
  seq = Sequence()
  seq.uncompress_all()
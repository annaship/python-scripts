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
      my_sql = """insert ignore into uncomr_seq (sequence)
              select distinct uncompress(sequence_comp) as sequence
              from sequence_ill limit %s, %s
              ON DUPLICATE KEY UPDATE sequence = VALUES(sequence)
              """ % (counter, chunk_size)
      print my_sql

if __name__ == '__main__':

  utils = util.Utils()

  if (utils.is_local() == True):
    db = 'test_env454'
    mysql_utils = util.Mysql_util(host = 'localhost', db = db, read_default_group = 'clienthome')
    print "host = 'localhost', db = %s" % db
  else:
    pass
    # mysql_utils = util.Mysql_util(host = 'vampsdb', db = 'vamps2', read_default_group = 'client')
    
  seq = Sequence()
  seq.uncompress_all()
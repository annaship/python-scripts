import MySQLdb
import sys
import os
import shutil
import shared #use shared to call connection from outside of the module
from pprint import pprint

class MyConnection:
  """
  Connection to env454
  Takes parameters from ~/.my.cnf, default host = "vampsdev", db="test" from read_default_group="clientvampsdev"
  if different use my_conn = MyConnection(read_default_group)
  shared.my_conn = util.MyConnection(read_default_group="clientenv454")
  shared.my_conn = util.MyConnection(read_default_group="clientvampsdev")
  
  to use on local with the server password and on a server:
  import socket
  my_hostname = socket.gethostname()
  if my_hostname.endswith(".local"):
    shared.my_conn = util.MyConnection(host="newbpcdb2", db="env454", read_default_group="clientenv454")
  else:
    shared.my_conn = util.MyConnection(host="newbpcdb2", db="env454")
  
  """
  def __init__(self, host="vampsdev", db="test", read_default_group="client"):
      self.conn   = None
      self.cursor = None
      self.rows   = 0
      self.new_id = None
      self.lastrowid = None
              
      try:
          print "=" * 40
          print "host = " + str(host) + ", db = "  + str(db) + ", group = " + str(read_default_group)
          print "=" * 40

          self.conn   = MySQLdb.connect(host=host, db=db, read_default_group=read_default_group, read_default_file="~/.my.cnf")
          self.cursor = self.conn.cursor()
                 
      except MySQLdb.OperationalError, e:
        print "=" * 40
        # print "No read_default_group, use host and db. (MySQLdb.OperationalError)"
        print "host = " + str(host) + ", db = "  + str(db)
        print "=" * 40
        
        self.conn   = MySQLdb.connect(host=host, db=db, read_default_file="~/.my.cnf")
        self.cursor = self.conn.cursor()      
        
      except MySQLdb.Error, e:
          print "Error %d: %s" % (e.args[0], e.args[1])
          raise
      except:                       # catch everything
          print "Unexpected:"         # handle unexpected exceptions
          print sys.exc_info()[0]     # info about curr exception (type,value,traceback)
          raise                       # re-throw caught exception   

  def close(self):
    if self.cursor:
      # print dir(self.cursor)
      self.cursor.close()
      self.conn.close()
      
  def execute_fetch_select(self, sql):
      if self.cursor:
          self.cursor.execute(sql)
          res = self.cursor.fetchall ()
          return res

  def execute_no_fetch(self, sql):
      if self.cursor:
          self.cursor.execute(sql)
          self.conn.commit()
          return self.cursor.lastrowid

class MySQLUtil:
    def __init__(self):
        res_names       = self.get_file_prefix_project_dataset()
        self.names_dict = self.make_names_dict(res_names)    
        
    def remove_all_new_files(self, path = "."):
        for filename in os.listdir(path):            
            print filename
            # [shutil.copyfile(os.path.join(path, filename), os.path.join(path, filename.replace(dict_name, self.names_dict[dict_name]))) for dict_name in self.names_dict.keys() if filename.startswith(dict_name)]            
            for new_filename in self.names_dict.values():
                if filename.startswith(new_filename):
                    # print filename
                    try:
                        os.remove(filename)
                    except OSError:
                        pass
        # print "Please remove all files starting with project name after you done with them"
        # l = [("rm %s*" % (x)) for x in set(self.names_dict.values())]
        # print l
                
        
    def rename_files_to_pr_dataset(self):
        # get idx_runkey - project/dataset info from db: get_file_prefix_project_dataset()
        # create dict: make_self.names_dict()
        # take all file names in the dir from args
        # cp! and rename files
        # remove new files
        
        self.get_file_names()
        # self.remove_all_new_files(self.names_dict)
        
    
    def get_file_names(self, path = "."):
        for filename in os.listdir(path):            
            # [shutil.copyfile(os.path.join(path, filename), os.path.join(path, filename.replace(dict_name, self.names_dict[dict_name]))) for dict_name in self.names_dict.keys() if filename.startswith(dict_name)]            
            for dict_name in self.names_dict.keys():
                if filename.startswith(dict_name):
                    new_name = filename.replace(dict_name, self.names_dict[dict_name])
                    # print "Copying %s to %s" % (filename, new_name)
                    shutil.copyfile(os.path.join(path, filename), os.path.join(path, new_name))
        
    def make_names_dict(self, res_names):
        self.names_dict = dict([(names[3], names[0] + "-" + names[1]) for names in res_names])
        return self.names_dict
        
    def get_file_prefix_project_dataset(self):
        # todo: run and lane in arguments
        query_sel_name = """SELECT DISTINCT project, dataset, lane, file_prefix 
			FROM env454.run_info_ill 
			JOIN env454.run USING(run_id) 
			JOIN env454.project USING(project_id) 
			JOIN env454.dataset USING(dataset_id) 
			WHERE run = \"20130419\" AND lane = 1 
            """
        print query_sel_name
        shared.my_conn.cursor.execute (query_sel_name)
        res_names = shared.my_conn.cursor.fetchall ()
        return res_names
        


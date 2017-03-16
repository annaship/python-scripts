import os
import MySQLdb
import logging
import timeit
import time

class Mysql_util:
    """
    Connection to vamps or vampsdev

    Takes parameters from ~/.my.cnf, default host = "vampsdev", db = "vamps"
    if different use my_conn = Mysql_util(host, db, read_default_file, port)
    """
    # def __init__(self, host = "bpcweb7", db = "vamps", read_default_file = os.path.expanduser("~/.my.cnf"), port = 3306):
    def __init__(self, host = "vampsdev", db = "test", read_default_group = "client", read_default_file = os.path.expanduser("~/.my.cnf")):
        self.utils     = Utils()
        self.conn      = None
        self.cursor    = None
        self.rows      = 0
        self.new_id    = None
        self.lastrowid = None
        self.rowcount  = None
        
        if read_default_file == "":
          if self.utils.is_local():
            read_default_file = os.path.expanduser("~/.my.cnf_local")
        # print "read_default_file = %s" % read_default_file

        try:
            self.utils.print_both("=" * 40)
            self.utils.print_both("host = " + str(host) + ", db = "  + str(db) + ", read_default_group = " + str(read_default_group)  + ", read_default_file = " + str(read_default_file))
            self.utils.print_both("=" * 40)

            # self.conn = MySQLdb.connect(host = host, db = db, read_default_file = read_default_file, port = port)
            self.conn    =  MySQLdb.connect(host = host, db = db, read_default_group = read_default_group, read_default_file = "~/.my.cnf")
            # print "host = %s, db = %s, read_default_file = %s" % (host, db, read_default_file)
            
            self.cursor = self.conn.cursor()

        except MySQLdb.Error, e:
            self.utils.print_both("Error %d: %s" % (e.args[0], e.args[1]))
            raise
        except:                       # catch everything
            self.utils.print_both("Unexpected:")
            self.utils.print_both(sys.exc_info()[0])
            raise                       # re-throw caught exception

    def execute_fetch_select(self, sql):
      # print "+" * 20
      # print sql
      if self.cursor:
        try:
          self.cursor.execute(sql)
          res         = self.cursor.fetchall ()
          field_names = [i[0] for i in self.cursor.description]
        except:
          self.utils.print_both(("ERROR: query = %s") % sql)
          raise
        return (res, field_names)

    def execute_no_fetch(self, sql):
      if self.cursor:
          self.cursor.execute(sql)
          self.conn.commit()
          # return self.cursor.lastrowid
          return (self.cursor.rowcount, self.cursor.lastrowid)

    def execute_insert(self, table_name, field_name, val_list, ignore = "IGNORE"):
      try:
        sql = "INSERT %s INTO %s (%s) VALUES (%s)" % (ignore, table_name, field_name, val_list)

        if self.cursor:
          self.cursor.execute(sql)
          self.conn.commit()
          return (self.cursor.rowcount, self.cursor.lastrowid)
      except:
        self.utils.print_both(("ERROR: query = %s") % sql)
        raise

    def get_all_name_id(self, table_name, id_name = "", field_name = "", where_part = ""):
      if (field_name == ""):
        field_name = table_name
      if (id_name == ""):
        id_name = table_name + '_id'
      my_sql  = """SELECT %s, %s FROM %s %s""" % (field_name, id_name, table_name, where_part)
      # self.utils.print_both(("my_sql from get_all_name_id = %s") % my_sql)
      res     = self.execute_fetch_select(my_sql)
      if res:
        return res[0]

    def execute_simple_select(self, field_name, table_name, where_part):
      id_query  = "SELECT %s FROM %s %s" % (field_name, table_name, where_part)
      return self.execute_fetch_select(id_query)[0]

    def get_id(self, field_name, table_name, where_part, rows_affected = [0,0]):
      # self.utils.print_array_w_title(rows_affected, "=====\nrows_affected from def get_id")

      if rows_affected[1] > 0:
        id_result = int(rows_affected[1])
      else:
        try:
          # id_query  = "SELECT %s FROM %s %s" % (field_name, table_name, where_part)
          id_result_full = self.execute_simple_select(field_name, table_name, where_part)
          id_result = int(id_result_full[0][0])
        except:
          self.utils.print_both("Unexpected:")
          # self.utils.print_both(sys.exc_info()[0])
          raise

      # self.utils.print_array_w_title(id_result, "=====\nid_result IN get_id")
      return id_result


class Utils:
    def __init__(self):
        pass

    def is_local(self):
        print os.uname()[1]


        dev_comps = ['ashipunova.mbl.edu', "as-macbook.home", "as-macbook.local", "Ashipunova.local", "Annas-MacBook-new.local", "Annas-MacBook.local",'Andrews-Mac-Pro.local']


        if os.uname()[1] in dev_comps:
            return True
        else:
            return False

    def is_vamps(self):
        print os.uname()[1]
        dev_comps = ['bpcweb8','bpcweb7','bpcweb7.bpcservers.private', 'bpcweb8.bpcservers.private']
        if os.uname()[1] in dev_comps:
            return True
        else:
            return False
            
    def is_vamps_prod(self):
        print os.uname()[1]
        dev_comps = ['bpcweb8', 'bpcweb8.bpcservers.private']
        if os.uname()[1] in dev_comps:
            return True
        else:
            return False
            
    def print_both(self, message):
        print message
        logging.debug(message)

    def print_array_w_title(self, message, title = 'message'):
      print title
      print message

    def read_csv_into_list(self, file_name):
      csv_file_content_all = list(csv.reader(open(file_name, 'rb'), delimiter = ','))
      csv_file_fields      = csv_file_content_all[0]
      csv_file_content     = csv_file_content_all[1:]
      return (csv_file_fields, csv_file_content)

    def flatten_2d_list(self, list):
      return [item for sublist in list for item in sublist]

    def wrapper(self, func, *args, **kwargs):
        def wrapped():
            return func(*args, **kwargs)
        return wrapped

    def benchmarking(self, func, func_name, *args, **kwargs):
      print "START %s" % func_name
      wrapped  = self.wrapper(func, *args)
      time_res = timeit.timeit(wrapped, number = 1)
      print 'time: %.2f s' % time_res
      # USE: utils.benchmarking(pr.parse_project_csv, "parse_project_csv", project_csv_file_name)

    def search_in_2d_list(self, search, data):
      for sublist in data:
        if search in sublist:
          return sublist
          break

    def find_val_in_nested_list(self, hey, needle):
      return [v for k, v in hey if k.lower() == needle.lower()]

    def find_key_by_value_in_dict(self, hey, needle):
      return [k for k, v in hey if v == needle]

    def make_entry_w_fields_dict(self, fields, entry):
      return dict(zip(fields, entry))

    def write_to_csv_file(self, file_name, res, file_mode = "wb"):
      data_from_db, field_names = res
      # print "VVVV"
      # print field_names

      with open(file_name, file_mode) as csv_file:
        csv_writer = csv.writer(csv_file)
        if file_mode == "wb":
          csv_writer.writerow(field_names) # write headers
        csv_writer.writerows(data_from_db)    

    def get_csv_file_calls(self, query):
      return prod_mysql_util.execute_fetch_select(query)
      # prod_mysql_util = Mysql_util(host = host_prod, db = "vamps", read_default_file = read_default_file_prod, port = port_prod)
      
    def slicedict(self, my_dict, key_list):
      return {k: v for k, v in my_dict.items() if k in key_list}
      
    def benchmark_w_return_1(self, message):
      print  "\n"
      print "-" * 10
      print message
      return time.time()
    
    def benchmark_w_return_2(self, t0, message = ""):
      t1 = time.time()
      total = float(t1-t0) / 60
      print '%s time: %.2f m' % (message, total)
    
    
    def chunks(self, arr, max_lines):
        """Yield successive n-sized chunks from l.
        Ex. for chunk in utils.chunks(query_a, self.max_lines):
            query_chunk = ", ".join(chunk)

            rowcount, lastrowid = self.run_insert_chunk(insert_seq_first_line, query_chunk)
        """
        for i in range(0, len(arr), max_lines):
            yield arr[i:i + max_lines]

    def print_out_dict(self, dict_name):
      print dict_name
      for k, v in dict_name.items():
          print "%s: %s" % (k, v)

    def initialize_dict_of_lists(self, list_of_keys):
      return {key: [] for key in list_of_keys}
    

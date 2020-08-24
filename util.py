from __future__ import generators  # needs to be at the top of your module
import os
from pathlib import Path
import sys

try:
  import mysqlclient as mysql
except ImportError:
  try:
    import pymysql as mysql
  except ImportError:
    import MySQLdb as mysql
import timeit
import time
import csv
from collections import Iterable

import datetime
import logging


class Log_system:
  def __init__(self, log_level_num = None):
    self.log_modes = {
      "debug"  : logging.DEBUG,
      "info"   : logging.INFO,
      "warn"   : logging.WARN,
      "warning": logging.WARNING,
      "error"  : logging.ERROR,
    }

    # logging.basicConfig(level = log_level_num)
    # logging.basicConfig(level = logging.INFO, filename = time.strftime("my-%Y-%m-%d.log"))
    # self.loggers = {}
    # self.logger = self.myLogger('debug')

    # def myLogger(self, name):
    #     if self.loggers.get(name):
    #         return self.loggers.get(name)
    #     else:
    #         logger = logging.getLogger(name)
    #         logger.setLevel(logging.DEBUG)
    #         now = datetime.datetime.now()
    #         FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    #         handler = logging.FileHandler(
    #             'debug'
    #             + now.strftime("%Y-%m-%d")
    #             + '.log')
    #         formatter = logging.Formatter(FORMAT)
    #         handler.setFormatter(formatter)
    #         logger.addHandler(handler)
    #         self.loggers[name] = logger
    #
    #         return logger

    # DEFAULTS:
    self.log_level_name = "debug"

    if log_level_num == None:
      self.log_level_num = self.get_log_level_num(self.log_level_name)
    else:
      self.log_level_num = log_level_num
      self.log_level_name = list(self.log_modes.keys())[list(self.log_modes.values()).index(self.log_level_num)]

    now = datetime.datetime.now()
    self.log_file_name = self.log_level_name + now.strftime("%Y-%m-%d") + ".log"

    self.logger = self.fetchLogger()

  def fetchLogger(self, log_file_name = None, log_level_name = None):
    logger = logging.getLogger(__name__)

    if logger.hasHandlers():
      logger.handlers = []

    if log_file_name == None:
      log_file_name = self.log_file_name

    if log_level_name == None:
      log_level_name = self.log_level_name

    log_level_num = self.get_log_level_num(log_level_name)
    logger.setLevel(log_level_num)

    # create File for Log

    handler = logging.FileHandler(str(log_file_name))
    handler.setLevel(log_level_num)
    # log format
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(FORMAT)
    handler.setFormatter(formatter)
    # adding the handler to Logging System
    logger.addHandler(handler)

    return logger

  def get_log_level_num(self, log_level_name):
    try:
      return self.log_modes[log_level_name.lower()]
    except:
      return self.log_level_num


class Mysql_util:
  """
  Connection to vamps or vampsdev

  Takes parameters from ~/.my.cnf, default host = "vampsdev", db = "vamps"
  if different use my_conn = Mysql_util(host, db, read_default_file, port)
  """

  # def __init__(self, host = "bpcweb7", db = "vamps", read_default_file = os.path.expanduser("~/.my.cnf"), port = 3306):
  def __init__(self, host = "vampsdev", db = "test", read_default_group = "client",
               read_default_file = os.path.expanduser("~/.my.cnf")):
    self.utils = Utils()
    self.conn = None
    self.cursor = None
    self.rows = 0
    self.new_id = None
    self.lastrowid = None
    self.rowcount = None
    self.dict_cursor = None

    if read_default_file == "":
      if self.utils.is_local():
        read_default_file = os.path.expanduser("~/.my.cnf_local")
    # print("read_default_file = %s" % read_default_file)

    try:
      self.utils.print_both("=" * 40)
      self.utils.print_both("host = " + str(host) + ", db = " + str(db) + ", read_default_group = " + str(
        read_default_group) + ", read_default_file = " + str(read_default_file))
      self.utils.print_both("=" * 40)

      # self.conn = mysql.connect(host = host, db = db, read_default_file = read_default_file, port = port)
      self.conn = mysql.connect(host = host, db = db, read_default_group = read_default_group,
                                read_default_file = read_default_file)
      # print("host = %s, db = %s, read_default_file = %s" % (host, db, read_default_file))

      self.cursor = self.conn.cursor()
      self.dict_cursor = self.conn.cursor(mysql.cursors.DictCursor)

    except mysql.Error as e:
      self.utils.print_both("Error %d: %s" % (e.args[0], e.args[1]))
      raise
    except:  # catch everything
      self.utils.print_both("Unexpected:")
      self.utils.print_both(sys.exc_info()[0])
      raise  # re-throw caught exception

  def execute_fetch_select(self, sql):
    # print("+" * 20)
    # print(sql)
    if self.cursor:
      try:
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        field_names = [i[0] for i in self.cursor.description]
      except:
        self.utils.print_both(("ERROR: query = %s") % sql)
        raise
      return (res, field_names)

  def execute_fetch_select_where(self, sql, values):
    # print("+" * 20)
    # print(sql)
    # print(values)
    if self.cursor:
      try:
        self.cursor.execute(sql, values)
        res = self.cursor.fetchall()
        field_names = [i[0] for i in self.cursor.description]
      except:
        self.utils.print_both(("ERROR: query = %s, values = %s") % (sql, values))
        raise
      return (res, field_names)

  # http://code.activestate.com/recipes/137270-use-generators-for-fetching-large-db-record-sets/
  def result_iter(self, cursor, arraysize = 1000):
    'An iterator that uses fetchmany to keep memory usage down'

    while True:
      results = self.cursor.fetchmany(arraysize)
      if not results:
        break
      for result in results:
        yield result

  def execute_fetchmany(self, sql, arraysize = 1000):
    if self.cursor:
      print(sql)
      self.cursor.execute(sql)
      # print("self.cursor.lastrowid")
      # print(self.cursor.lastrowid)
      print("self.cursor.rowcount")
      print(self.cursor.rowcount)

      data_from_db = []
      for result in self.result_iter(self.cursor, arraysize):
        data_from_db.append(result)

      return data_from_db

  def execute_no_fetch_w_info(self, sql):
    if self.cursor:
      self.cursor.execute(sql)
      self.conn.commit()
      try:
        return self.cursor._info
      except AttributeError as e:
        pass

  def execute_no_fetch(self, sql):
    if self.cursor:
      try:
        self.cursor.execute(sql)
      except mysql.InternalError as e:
        print(e)
        raise
        # pymysql.err.InternalError: (1054, "Unknown column 'place' in 'where clause'")
      except mysql.ProgrammingError as e:
        print(e)
        raise
      self.conn.commit()
      # print(self.cursor.lastrowid)
      return (self.cursor.rowcount, self.cursor.lastrowid)

  def execute_no_fetch_w_values(self, sql, values):
    if self.cursor:
      try:
        self.cursor.execute(sql, values)
        self.conn.commit()
        # print(self.cursor.lastrowid)
        return (self.cursor.rowcount, self.cursor.lastrowid)
      except:
        self.utils.print_both(("ERROR: query = %s, values = %s") % (sql, values))

  def execute_fetch_select_to_dict(self, sql):
    if self.dict_cursor:
      try:
        self.dict_cursor.execute(sql)
        # print("DDD")
        # print(self.dict_cursor.description)
        return self.dict_cursor.fetchall()
      except:
        # self.utils.print_both(("ERROR: query = %s") % sql)
        raise

  def execute_many_fields_one_record(self, table_name, field_names_arr, values_tuple, ignore = "IGNORE"):
    field_names_str = ', '.join(field_names_arr)
    values_str_pattern = ", ".join(['%s' for e in field_names_arr])

    my_sql_insert_query = "INSERT {} INTO {} ({}) VALUES ({})".format(ignore, table_name, field_names_str,
                                                                      values_str_pattern)

    # print("my_sql_insert_query FROM util: {}, ".format(my_sql_insert_query, values_tuple))

    res = self.cursor.execute(my_sql_insert_query, values_tuple)
    self.conn.commit()

    # print("execute_many_fields_one_record FROM util res: {}".format(res))

  def execute_insert_many(self, table_name, field_name, records_to_insert_arr, ignore = "IGNORE"):
    try:
      mySql_insert_query = "INSERT {} INTO {} ({}) VALUES (%s)".format(ignore, table_name, field_name)

      if self.cursor:
        self.cursor.executemany(mySql_insert_query, records_to_insert_arr)
        self.conn.commit()
        return (self.cursor.rowcount, self.cursor.lastrowid)
    except:
      self.utils.print_both(("ERROR: sql = {}, val_list = {}").format(mySql_insert_query, records_to_insert_arr))
      raise

  def execute_insert(self, table_name, field_name, val_list, ignore = "IGNORE", sql = ""):
    try:
      if sql == "":
        sql = "INSERT {} INTO {} ({}) VALUES (%s)".format(ignore, table_name, field_name)
      if self.cursor:
        self.cursor.execute(sql, val_list)
        self.conn.commit()
        return (self.cursor.rowcount, self.cursor.lastrowid)
    except:
      self.utils.print_both(("ERROR: sql = {}, val_list = {}").format(sql, val_list))
      raise

  def get_all_name_id(self, table_name, id_name = "", field_name = "", where_part = ""):
    if (field_name == ""):
      field_name = table_name
    if (id_name == ""):
      id_name = table_name + '_id'
    my_sql = """SELECT %s, %s FROM %s %s""" % (field_name, id_name, table_name, where_part)
    # self.utils.print_both(("my_sql from get_all_name_id = %s") % my_sql)
    res = self.execute_fetch_select(my_sql)
    if res:
      return res[0]

  def execute_simple_select(self, field_name, table_name, where_part):
    id_query = "SELECT %s FROM %s %s" % (field_name, table_name, where_part)
    return self.execute_fetch_select(id_query)[0]

  def get_id(self, field_name, table_name, where_part, rows_affected = [0, 0]):
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
        self.utils.print_both(
          'field_name = "{}", table_name = "{}", where_part = "{}"'.format(field_name, table_name, where_part))
        raise

    # self.utils.print_array_w_title(id_result, "=====\nid_result IN get_id")
    return id_result

  def get_table_names(self, table_schema):
    query = """
        SELECT TABLE_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA='%s';
      """ % (table_schema)
    # print(query)
    return self.execute_fetch_select(query)

  def get_field_names(self, table_schema, table_name):
    query = """
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA='%s'
            AND TABLE_NAME='%s';
      """ % (table_schema, table_name)
    # print(query)
    return self.execute_fetch_select(query)

  """SELECT CONSTRAINT_NAME
  FROM `TABLE_CONSTRAINTS` 
  join INFORMATION_SCHEMA.KEY_COLUMN_USAGE using(CONSTRAINT_NAME, TABLE_SCHEMA, table_name)
  WHERE 
    TABLE_SCHEMA = 'mcm_history'
  and `CONSTRAINT_TYPE` = 'unique' and table_name = 'content';"""

  def get_uniq_index_columns(self, table_schema, table_name):
    query = """
            SELECT DISTINCT CONSTRAINT_NAME
            FROM information_schema.KEY_COLUMN_USAGE
            JOIN information_schema.TABLE_CONSTRAINTS USING(CONSTRAINT_NAME, TABLE_SCHEMA, TABLE_NAME)
            WHERE
              TABLE_SCHEMA = '%s'
              AND TABLE_NAME = '%s'
              AND CONSTRAINT_TYPE = 'UNIQUE';
        """ % (table_schema, table_name)
    rows = self.execute_fetch_select(query)
    return list(self.utils.extract(rows[0]))

  # def get_uniq_index_columns(self, table_schema, table_name):
  #     query = """
  #         SELECT DISTINCT COLUMN_NAME
  #         FROM information_schema.KEY_COLUMN_USAGE
  #         JOIN information_schema.TABLE_CONSTRAINTS USING(CONSTRAINT_NAME, TABLE_SCHEMA, TABLE_NAME)
  #         WHERE
  #           TABLE_SCHEMA = '%s'
  #           AND TABLE_NAME = '%s'
  #           AND CONSTRAINT_TYPE = 'UNIQUE';
  #     """ % (table_schema, table_name)
  #     rows = self.execute_fetch_select(query)
  #     return list(self.utils.extract(rows[0]))

  def get_column_names(self, table_name):
    query = "SHOW columns FROM %s" % table_name
    return self.execute_fetch_select(query)


class Utils:
  def __init__(self):
    self.log_system = Log_system()

  def print_both(self, message, file_name = None, log_level_name = None):
    if file_name is None:
      file_name = self.log_system.log_file_name

    if log_level_name is None:
      logger = self.log_system.logger
      log_level_name = "debug"
    else:
      logger = self.log_system.fetchLogger(file_name, log_level_name)

    log_level_num = self.log_system.get_log_level_num(log_level_name)

    print(message)
    try:
      logger.log(log_level_num, message)
    except:
      raise

  def is_local(self):
    print("os.environ['HOME']:")
    print(os.environ['HOME'])

    # print(os.uname()[1])

    dev_comps = ['ashipunova.mbl.edu', "as-macbook.home", "as-macbook.local", "Ashipunova.local",
                 "Annas-MacBook-new.local", "Annas-MacBook.local", 'Andrews-Mac-Pro.local']

    if (os.uname()[1] in dev_comps) or (os.environ['HOME'] == "/Users/ashipunova"):
      return True
    else:
      return False

  def is_vamps(self):
    print(os.uname()[1])
    dev_comps = ['bpcweb8', 'bpcweb7', 'bpcweb7.bpcservers.private', 'bpcweb8.bpcservers.private']
    if os.uname()[1] in dev_comps:
      return True
    else:
      return False

  def is_vamps_prod(self):
    print(os.uname()[1])
    dev_comps = ['bpcweb8', 'bpcweb8.bpcservers.private']
    if os.uname()[1] in dev_comps:
      return True
    else:
      return False

  def print_array_w_title(self, message, title = 'message'):
    print(title)
    print(message)

  def read_csv_into_list(self, file_name, delimiter = ','):
    csv_file_content_all = list(csv.reader(open(file_name, 'rt'), delimiter = delimiter))
    csv_file_fields = csv_file_content_all[0]
    csv_file_content = csv_file_content_all[1:]
    return (csv_file_fields, csv_file_content)

  def read_csv_into_dict(self, file_name, delimiter = ','):
    csv_file_content_all = csv.DictReader(open(file_name, 'rt'), delimiter = delimiter)
    return [row for row in csv_file_content_all]

  def convert_each_to_str(self, my_list):
    return [str(val) for val in my_list]

  def make_quoted_str(self, my_list):
    res_str = ', '.join('"{0}"'.format(w) for w in my_list)
    # "'%s'" % "', '".join(self.convert_each_to_str(my_list))
    return res_str

  def make_quoted_str_from_tuple_sql_rows(self, tuple_sql_rows):
    my_list = [x[0] for x in tuple_sql_rows[0]]
    res_str = self.make_quoted_str(my_list)
    return res_str

  def flatten_2d_list(self, my_list):
    return [item for sublist in my_list for item in sublist]

  """
  https://stackoverflow.com/questions/49247894/recursive-function-for-extract-elements-from-deep-nested-lists-tuples/49247980#49247980
  """

  def flatten(self, collection):
    for x in collection:
      if isinstance(x, Iterable) and not isinstance(x, str):
        yield from self.flatten(x)
      else:
        yield x

  def extract(self, data, exclude = ()):
    # use list(data)
    yield from (x for x in self.flatten(data) if x not in exclude)

  def flatten_single_mysql_res_tuple_to_int(self, data, exclude = ()):
    return int(list(self.extract(data, exclude = exclude))[0])

  def sort_case_insesitive(self, unsorted_list):
    try:
      sorted_list = sorted(unsorted_list, key = lambda s: s.lower())
    except AttributeError:
      sorted_list = sorted(unsorted_list)
    except:
      raise
    return sorted_list

  def wrapper(self, func, *args, **kwargs):
    def wrapped():
      return func(*args, **kwargs)

    return wrapped

  def benchmarking(self, func, func_name, *args, **kwargs):
    print("START %s" % func_name)
    wrapped = self.wrapper(func, *args)
    time_res = timeit.timeit(wrapped, number = 1)
    print('time: %.2f s' % time_res)
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

  def transpose_mtrx(self, list_of_lists):
    return zip(*list_of_lists)

  def write_to_csv_file_matrix(self, file_name, matrix_to_csv, headers = [], file_mode = "w"):
    with open(file_name, file_mode) as csv_file:
      csv_writer = csv.writer(csv_file)
      if headers:
        csv_writer.writerows(headers)
      csv_writer.writerows(matrix_to_csv)

  def write_to_csv_file_db_res(self, file_name, res, file_mode = "w"):
    data_from_db, field_names = res
    # print("VVVV")
    # print(field_names)

    with open(file_name, file_mode) as csv_file:
      csv_writer = csv.writer(csv_file)
      if file_mode == "w":
        csv_writer.writerow(field_names)  # write headers
      csv_writer.writerows(data_from_db)

  def get_csv_file_calls(self, query):
    return prod_mysql_util.execute_fetch_select(query)
    # prod_mysql_util = Mysql_util(host = host_prod, db = "vamps", read_default_file = read_default_file_prod, port = port_prod)

  # TODO: make intersection my_dict.keys() & key_list, use for list; benchmark
  def slicedict(self, my_dict, key_list):
    return {k: v for k, v in my_dict.items() if k in key_list}

  def intersection(self, lst1, lst2):
    return list(set(lst1) & set(lst2))

  def benchmark_w_return_1(self, message):
    print("\n")
    print("-" * 10)
    print(message)
    return time.time()

  def benchmark_w_return_2(self, t0, message = ""):
    t1 = time.time()
    total = float(t1 - t0) / 60
    print('%s time: %.2f m' % (message, total))

  def chunks(self, arr, max_lines):
    """Yield successive n-sized chunks from l.
    Ex. for chunk in utils.chunks(query_a, self.max_lines):
        query_chunk = ", ".join(chunk)

        rowcount, lastrowid = self.run_insert_chunk(insert_seq_first_line, query_chunk)
    """
    for i in range(0, len(arr), max_lines):
      yield arr[i:i + max_lines]

  def print_out_dict(self, dict_name):
    print(dict_name)
    for k, v in dict_name.items():
      print("%s: %s" % (k, v))

  def initialize_dict_of_lists(self, list_of_keys):
    return {key: [] for key in list_of_keys}

  def grouper(self, iterable, n, fillvalue = None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue = fillvalue)

  def find_in_nested_dict(self, nested_dict, to_find):
    reverse_linked_q = list()
    reverse_linked_q.append((list(), nested_dict))
    while reverse_linked_q:
      this_key_chain, this_v = reverse_linked_q.pop()
      # finish search if found the mime type
      if this_v == to_find:
        return this_key_chain
      # not found. keep searching
      # queue dicts for checking / ignore anything that's not a dict
      try:
        items = this_v.items()
      except AttributeError:
        continue  # this was not a nested dict. ignore it
      for k, v in items:
        reverse_linked_q.append((this_key_chain + [k], v))
    # if we haven't returned by this point, we've exhausted all the contents

    return False

  def check_if_file_exists(self, filename):
    my_file = Path(filename)

    file_exists = my_file.exists() and my_file.is_file()
    return file_exists

  """
  >>> from collections import defaultdict
  >>> def autodict(): return defaultdict(autodict)
  ...
  >>> foo = autodict()
  >>> foo['foo']['bar']['baz']['quuz'] = 42
  >>> foo['bar']['baz'] = 123

  """
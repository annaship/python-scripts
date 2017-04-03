import IlluminaUtils.lib.fastalib as fa
import gzip
from itertools import izip
from collections import defaultdict
import time
import util

class Metadata():
  def __init__(self):
    pass

  def get_all_all_custom_tables(self):
    query_custom_tables = """
    SELECT table_name FROM information_schema.tables
    WHERE TABLE_NAME LIKE "custom_metadata_%"
    AND table_schema = "vamps2"
    """
    return mysql_utils.execute_fetch_select(query_custom_tables)
  
  def get_all_dco_project_ids(self):
    query_project_ids = """select project_id, project from project where project like "DCO%" """
    return mysql_utils.execute_fetch_select(query_project_ids)
    
  def get_all_custom_metadata_tabel_names(self, all_dco_project_ids):
    return [str(int(x[0])) for x in all_dco_project_ids[0]]

  def get_dco_custom_fields(self, dco_cutom_tables):
    for table_name in dco_cutom_tables:
      get_metadata_query = """ select 

      """

    dco_custom_fields_query = """select distinct project_id, field_name, field_units, example from custom_metadata_fields where project_id in (%s)""" % (", ".join(all_project_ids))
    # print dco_custom_fields_query
    dco_custom_fields = mysql_utils.execute_fetch_select(dco_custom_fields_query)
    # print dco_custom_fields
    """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
    return dco_custom_fields
    
  def get_custom_metadata_per_project(self, project_id, field_name):
    query = """select `%s` from custom_metadata_%s""" % (field_name, str(project_id))
    # print query
    return mysql_utils.execute_fetch_select(query)
    
  def make_custom_metadata_distinct_list(self, custom_metadata):
    return [y[0] for y in set([x for x in custom_metadata[0]])]
  
  def populate_dict_of_dicts(self, my_dict, key, key_to_use = ""):
    if key_to_use == "":
      key_to_use = key
    # print "9" * 9
    # print my_dict
    # print "key = %s" % key
    if key not in my_dict:
        my_dict[key_to_use] = {}
    return my_dict

  def populate_dict_of_lists(self, my_dict, key, key_to_use = ""):
    if key_to_use == "":
      key_to_use = key
    if key not in my_dict:
        my_dict[key_to_use] = []
    return my_dict
  
  def make_my_dict(self, my_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list):
    my_dict = self.populate_dict_of_dicts(my_dict, str_project_id)

    if field_name not in my_dict[str_project_id]:
        my_dict[str_project_id][field_name__descr] = []

    my_dict[str_project_id][field_name__descr].append(custom_metadata_distinct_list)
    return my_dict
    
  def get_project_name(self, all_dco_project_ids, str_project_id):
    return [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    
  def make_custom_metadata_per_field_dict(self, my_dict2, custom_metadata_distinct_list, field_name__descr):
    for custom_metadatum in custom_metadata_distinct_list:
      my_dict2 = self.populate_dict_of_lists(my_dict2, field_name__descr)
      
      my_dict2[field_name__descr].append(custom_metadatum)
    return my_dict2
      
if __name__ == '__main__':
  utils = util.Utils()

  if (utils.is_local() == True):
    mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
  else:
    mysql_utils = util.Mysql_util(host = "vampsdb", db = "vamps2", read_default_group = "client")

  metadata = Metadata()
  # query = "show tables"
  # a = mysql_utils.execute_fetch_select(query)
  # print a
  
  # print all_custom_tables
  
  # for t in all_custom_tables[0]:
  #   print t[0]

  all_custom_tables = metadata.get_all_all_custom_tables()
  
  query_project_ids = """select project_id, project from project where project like "DCO%" """
  all_dco_project_ids = metadata.get_all_dco_project_ids()
  
  # print "all_dco_project_ids"
  # print all_dco_project_ids
  dco_cutom_tables = ['custom_metadata_' + str(int(x[0])) for x in all_dco_project_ids[0]]
  
  all_project_ids = metadata.get_all_custom_metadata_tabel_names(all_dco_project_ids)
  # print dco_cutom_tables
  # print len(dco_cutom_tables)
  # 64
  
  dco_custom_fields = metadata.get_dco_custom_fields(dco_cutom_tables)
  # print "=" * 5
  # print dco_custom_fields
  
  custom_metadata_distinct_list_per_field_per_project_dict = {}
  
  all_field_names = []
  all_field_name__descr = []
  for dco_custom_field_info in dco_custom_fields[0]:
    # print "dco_custom_field_info"
    # print dco_custom_field_info
    # (860L, 'resistivity', 'ohm-meters', 'n.d.')
    # (860L, 'trace element geochemistry', '', 'yes')
    project_id = dco_custom_field_info[0]
    field_name = dco_custom_field_info[1]
    # my_dict[project_id]field_name].append
    # query = """select `%s` from custom_metadata_%s""" % (field_name, str(project_id))
    # print query
    # custom_metadata = metadata.get_custom_metadata_per_project(project_id, field_name)
    # mysql_utils.execute_fetch_select(query)
    # print "custom_metadata HHHH"
    # print custom_metadata
    # ((('',), ('',), ('',), ('',), ('',), ('',), ('',), ('',), ('3363',), ('2796',), ('',), ('',), ('',), ('',), ('',), ('',), ('4500',), ('4286',)), ['methane'])
    
    custom_metadata_distinct_list = metadata.make_custom_metadata_distinct_list(metadata.get_custom_metadata_per_project(project_id, field_name))
    # [y[0] for y in set([x for x in custom_metadata[0]])]
    # print "YYY"
    # print custom_metadata_distinct_list
    # print "field_name = %s" % field_name
    # print dco_custom_field_info[3] == custom_metadata_distinct_list[0]
    # 
    # if not (dco_custom_field_info[3] == custom_metadata_distinct_list[0]):
    #   print "dco_custom_field_info[3] = %s, custom_metadata_distinct_list[0] = %s" % (dco_custom_field_info[3], custom_metadata_distinct_list[0])
    
    str_project_id = str(project_id)
    field_name__descr = field_name + "__" + dco_custom_field_info[2]
    all_field_names.append(field_name)
    all_field_name__descr.append(field_name__descr)

    custom_metadata_distinct_list_per_field_per_project_dict = metadata.make_my_dict(custom_metadata_distinct_list_per_field_per_project_dict, str_project_id, field_name, field_name__descr, custom_metadata_distinct_list)
    # for x in custom_metadata_distinct_list:
    #   if dco_custom_field_info[3] != x:
    #     # print "dco_custom_field_info[3] = %s, x = %s" % (dco_custom_field_info[3], x)
    #     pass
    
  # print "my_dict"
  # print my_dict
  # lat_lon': [['', '28.596 S, 173.381 W', '28.596 S, 173.280 W']], 'samp_store_temp': [['-80']]}}
  
  # print "555"
  # for str_project_id, d1 in my_dict.items():
  #   """
  #   all_dco_project_ids
  #   (((300L, 'DCO_BKR_Av4v5'), (110L, 'DCO_BKR_Bv4v5'), (301L, 'DCO_BOM_Av6'), (101L, 'DCO_BOM_Bv6'), (302L, 'DCO_BPC_Bv6'), (103L, 'DCO_BRA_Av6'), (303L, 'DCO_BRA_Bv6'),
  #   """
  #   
  #   project_name = [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
  #   for field_name__descr, custom_metadata_distinct_list in d1.items():
  #     for custom_metadatum in custom_metadata_distinct_list:
  #       pass
  #       # print project_name[0], field_name__descr, custom_metadatum
  #       
  #       "/workspace/ashipunova/metadata/dco$ python dco_metadata_exapmles_per_dataset.py >all_dco_metadata.csv"
  #       
        # ===
  custom_metadata_per_field_dict = {}
  for str_project_id, d1 in custom_metadata_distinct_list_per_field_per_project_dict.items():  
    project_name = metadata.get_project_name(all_dco_project_ids, str_project_id)      
    for field_name__descr, custom_metadata_distinct_list in d1.items():
      custom_metadata_per_field_dict = metadata.make_custom_metadata_per_field_dict(custom_metadata_per_field_dict, custom_metadata_distinct_list, field_name__descr)
  
  for k, v in custom_metadata_per_field_dict.items():
    print k, set([item for sublist in v for item in sublist])
    
  print len(set(all_field_name__descr))
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
  
  print "all_dco_project_ids"
  print all_dco_project_ids
  dco_cutom_tables = ['custom_metadata_' + str(int(x[0])) for x in all_dco_project_ids[0]]
  
  all_project_ids = metadata.get_all_custom_metadata_tabel_names(all_dco_project_ids)
  print dco_cutom_tables
  # print len(dco_cutom_tables)
  # 64
  
  for table_name in dco_cutom_tables:
    get_metadata_query = """ select 
    
    """
  
  dco_custom_fields_query = """select distinct project_id, field_name, field_units, example from custom_metadata_fields where project_id in (%s)""" % (", ".join(all_project_ids))
  # print dco_custom_fields_query
  dco_custom_fields = mysql_utils.execute_fetch_select(dco_custom_fields_query)
  # print dco_custom_fields
  """((...(860L, 'trace element geochemistry', '', 'yes')), ['project_id', 'field_name', 'field_units', 'example'])"""
  
  my_dict = {}
  # defaultdict(dict)
  # my_dict = utils.initialize_dict_of_lists(all_project_ids)
  
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
    query = """select `%s` from custom_metadata_%s""" % (field_name, str(project_id))
    # print query
    custom_metadata = mysql_utils.execute_fetch_select(query)
    custom_metadata_list = [y[0] for y in set([x for x in custom_metadata[0]])]
    # print custom_metadata_list
    # print "field_name = %s" % field_name
    # print dco_custom_field_info[3] == custom_metadata_list[0]
    # 
    # if not (dco_custom_field_info[3] == custom_metadata_list[0]):
    #   print "dco_custom_field_info[3] = %s, custom_metadata_list[0] = %s" % (dco_custom_field_info[3], custom_metadata_list[0])
    
    str_project_id = str(project_id)
    field_name__descr = field_name + "__" + dco_custom_field_info[2]
    all_field_names.append(field_name)
    all_field_name__descr.append(field_name__descr)
    if str_project_id not in my_dict:
        my_dict[str_project_id] = {}

    if field_name not in my_dict[str_project_id]:
        my_dict[str_project_id][field_name__descr] = []

    my_dict[str_project_id][field_name__descr].append(custom_metadata_list)
  
    for x in custom_metadata_list:
      if dco_custom_field_info[3] != x:
        # print "dco_custom_field_info[3] = %s, x = %s" % (dco_custom_field_info[3], x)
        pass
    
  # print my_dict
  # lat_lon': [['', '28.596 S, 173.381 W', '28.596 S, 173.280 W']], 'samp_store_temp': [['-80']]}}
  
  print "555"
  for str_project_id, d1 in my_dict.items():
    """
    all_dco_project_ids
    (((300L, 'DCO_BKR_Av4v5'), (110L, 'DCO_BKR_Bv4v5'), (301L, 'DCO_BOM_Av6'), (101L, 'DCO_BOM_Bv6'), (302L, 'DCO_BPC_Bv6'), (103L, 'DCO_BRA_Av6'), (303L, 'DCO_BRA_Bv6'),
    """
    
    project_name = [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    for field_name__descr, custom_metadata_list in d1.items():
      for custom_metadatum in custom_metadata_list:
        pass
        # print project_name[0], field_name__descr, custom_metadatum
        
        "/workspace/ashipunova/metadata/dco$ python dco_metadata_exapmles_per_dataset.py >all_dco_metadata.csv"
        
        # ===
  my_dict2 = {}
  for str_project_id, d1 in my_dict.items():  
    project_name = [x[1] for x in all_dco_project_ids[0] if int(x[0]) == int(str_project_id)]
    for field_name__descr, custom_metadata_list in d1.items():
      for custom_metadatum in custom_metadata_list:
        if field_name__descr not in my_dict2:
            my_dict2[field_name__descr] = []
        
        my_dict2[field_name__descr].append(custom_metadatum)
  
  for k, v in my_dict2.items():
    print k, set([item for sublist in v for item in sublist])
    
  print len(set(all_field_name__descr))
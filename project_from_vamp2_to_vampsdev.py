import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from subprocess import Popen, PIPE
import util
import IlluminaUtils.lib.fastalib as fastalib
from collections import defaultdict

try:
    import mysqlclient as mysql
except ImportError:
    try:
        import pymysql as mysql
    except ImportError:
        import MySQLdb as mysql


class dbUpload:
    """db upload methods"""
    Name = "dbUpload"
    """
    Order:
        # put_run_info
        # insert_seq()
        # insert_pdr_info()
        # gast
        # insert_taxonomy()
        # insert_sequence_uniq_info_ill()

    """

    def __init__(self, project = None, db_name = None):

        self.db_name = db_name
        self.utils = util.Utils()
        self.project = project
        self.get_project_id()


        self.db_cnf = {
            "vamps2": {
                "local"      : {"host": "localhost", "db": "vamps2"},
                "production" : {"host": "vampsdb", "db": "vamps2"},
                "development": {"host": "vampsdev", "db": "vamps2"}
            },
            "env454": {
                "local"      : {"host": "localhost", "db": "test_env454"},
                "production" : {"host": "bpcdb1", "db": "env454"},
                "development": {"host": "vampsdev", "db": "test"}
            }
        }
        # mysql_utils = self.get_conn()

        self.table_names_dict = {
            "vamps2": {
                "sequence_field_name"         : "sequence_comp", "sequence_table_name": "sequence",
                "sequence_pdr_info_table_name": "sequence_pdr_info", "contact": "user", "username": "username",
                "connect_pr_dat_table"        : "dataset"
            },
            "env454": {
                "sequence_field_name"         : "sequence_comp", "sequence_table_name": "sequence_ill",
                "sequence_pdr_info_table_name": "sequence_pdr_info_ill", "contact": "contact", "username": "vamps_name",
                "connect_pr_dat_table"        : "run_info_ill"
            }
        }
        self.db_marker = "vamps2"
        self.table_names = self.table_names_dict[self.db_marker]

    def get_conn(self):

        if self.utils.is_local():
            is_local = "local"
        else:
            is_local = "development"

        try:
            host = self.db_cnf['vamps2']['local']['host']
            db = "vamps2"
        except Exception:
            self.db_marker = "vamps2"
            host = self.db_cnf['vamps2']['development']['host']
            db = self.db_cnf['vamps2']['development']['db']

        # mysql_utils = MyConnection(host, db)

            # host = C.db_cnf[self.db_marker][is_local]["host"]
            # db = C.db_cnf[self.db_marker][is_local]["db"]


    def get_project_id(self):
        project_sql = "SELECT distinct project_id FROM project where project = '%s'" % (self.project)
        res = mysql_utils.execute_fetch_select_to_dict(project_sql)
        self.project_id = res[0]['project_id']

    def get_dataset_ids_for_project_id(self):
        where_part = "WHERE project_id = '%s'" % (self.project_id)
        dataset_ids_for_project_id = """SELECT dataset_id FROM %s %s 
                                            """ % (self.table_names["connect_pr_dat_table"], where_part)

        rows = mysql_utils.execute_fetch_select(dataset_ids_for_project_id)
        dataset_ids_list = [y[0] for x in rows for y in x]
        return dataset_ids_list


    def put_project_info(self):
        pass

if __name__ == '__main__':
    utils = util.Utils()

    if (utils.is_local() == True):
        mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
    else:
        mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps2", read_default_group = "client")

    # TODO: get from args
    project = "JG_NPO_Bv4v5"
    upl = dbUpload(project)

    dataset_ids_list = upl.get_dataset_ids_for_project_id()
    print(upl.project_id)
    print(dataset_ids_list)

    """TODO: args - create, update"""

    #
    # t = utils.benchmark_w_return_1("get_metadata_info")
    # metadata.get_metadata_info()
    # utils.benchmark_w_return_2(t, "get_metadata_info")
    #

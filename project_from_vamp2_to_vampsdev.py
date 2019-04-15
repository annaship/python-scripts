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
        dataset_ids_list = [x[0] for x in rows[0]]
        return dataset_ids_list

    def get_dataset_per_run_info_id(self, dataset_ids_list):
        dataset_ids_string = "', '".join(str(x) for x in dataset_ids_list)

        all_dataset_run_info_sql = """SELECT run_info_ill_id, dataset_id FROM run_info_ill 
                                    WHERE dataset_id in ('%s') """ % (dataset_ids_string)
        res = mysql_utils.execute_fetch_select_to_dict(all_dataset_run_info_sql)
        # {t['dataset_id']: t["run_info_ill_id"] for t in res}
        return res


    def get_run_info_ill_id(self, dataset_ids_list):
        dataset_ids_string = "', '".join(str(x) for x in dataset_ids_list)
        my_sql = """SELECT run_info_ill_id FROM run_info_ill
                    WHERE dataset_id in ('%s')
                    ;
        """ % (dataset_ids_string)

        rows = mysql_utils.execute_fetch_select(my_sql)
        if rows:
            return [x[0] for x in rows[0]]


    def put_project_info(self):
        pass


class Project:

    def __init__(self, project = None):
        self.project = project

    def get_project_info(self):
        # "distinct" and "limit 1" are redundant for clarity, a project name is unique in the db
        project_sql = "SELECT distinct * FROM project where project = '%s' limit 1" % (self.project)
        project_info = mysql_utils.execute_fetch_select_to_dict(project_sql)
        return project_info[0]



if __name__ == '__main__':
    utils = util.Utils()

    if (utils.is_local() == True):
        mysql_utils = util.Mysql_util(host = "localhost", db = "vamps2", read_default_group = "clienthome")
    else:
        mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps2", read_default_group = "client")

    # TODO: get from args
    project = "JG_NPO_Bv4v5"

    pr_obj = Project(project)
    pr_info = pr_obj.get_project_info()

    upl = dbUpload(project)

    insert_sql_template = "INSERT IGNORE INTO %s WHERE %s"

    user_id = pr_info['owner_user_id']
    insert_user_sql = insert_sql_template % ("user", user_id)

    dataset_ids_list = upl.get_dataset_ids_for_project_id()
    print(upl.project_id)
    print(dataset_ids_list)

    tuple_of_dataset_and_run_info_ids = upl.get_dataset_per_run_info_id(dataset_ids_list)

    """TODO: args - project name"""
    """
user
project
access
custom_metadata_#
custom_metadata_fields
dataset
project_notes
user_project_status

dna_region
domain
env_package
illumina_index
primer_suite
run
run_key
sequencing_platform
target_gene

ontology
term

run
run_key

sequence
classifier

rank
strain
genus
domain
family
klass
order
phylum
species
silva_taxonomy
rdp_taxonomy

silva_taxonomy_info_per_seq
rdp_taxonomy_info_per_seq

required_metadata_info
run_info_ill
sequence_pdr_info
sequence_uniq_info
    """



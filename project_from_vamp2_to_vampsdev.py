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

class User:

    def __init__(self, user_id = None):
        self.user_id = user_id

    def get_user_info(self):
        """
        UNIQUE KEY `contact_email_inst` (`first_name`,`last_name`,`email`,`institution`),
        UNIQUE KEY `username` (`username`),

        """
        user_sql = "SELECT * FROM user where user_id = '%s'" % (self.user_id)
        user_info = mysql_utils.execute_fetch_select_to_dict(user_sql)
        return user_info[0]



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

    user_id = pr_info['owner_user_id']
    user_obj = User(user_id)
    user_info = user_obj.get_user_info()
    
    upl = dbUpload(project)

    insert_sql_template = "INSERT IGNORE INTO %s VALUES (%s)"

    insert_user_sql = insert_sql_template % ("user", user_id)

    dataset_ids_list = upl.get_dataset_ids_for_project_id()
    print(upl.project_id)
    print(dataset_ids_list)

    tuple_of_dataset_and_run_info_ids = upl.get_dataset_per_run_info_id(dataset_ids_list)

    """TODO: args - project name"""
    """insert with select to find what's behind ids
    
    
user
project
access
dataset
custom_metadata_#
custom_metadata_fields
project_notes
user_project_status

In full:
dna_region
domain
env_package
illumina_index
primer_suite
run
run_key
sequencing_platform
target_gene

Used only:
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

    """
    pipeline upload methods:
    
    dbUpload
__init__
get_conn
reset_auto_increment
convert_samples_to_dict
check_files_csv
collect_project_ids
get_projects_and_ids
get_fasta_file_names
send_message
get_run_info_ill_id
get_project_id_per_dataset_id
get_dataset_per_run_info_id
get_id
make_gast_files_dict
gast_filename
get_gast_result
put_run_info
insert_test_contact
get_contact_id
insert_rundate
insert_project
insert_dataset
convert_env_sample_source
get_all_metadata_info
get_env_sample_source
insert_metadata
insert_run_info
put_required_metadata
del_sequence_pdr_info_by_project_dataset
count_sequence_pdr_info
get_primer_suite_name
get_lane
count_seq_from_files_grep
check_seq_upload
put_seq_statistics_in_file
insert_taxonomy
insert_pdr_info
insert_sequence_uniq_info
insert_silva_taxonomy_info_per_seq

Taxonomy
__init__
get_taxonomy_from_gast
get_taxonomy_id_dict
insert_whole_taxonomy
insert_split_taxonomy
parse_taxonomy
get_taxa_by_rank
make_uniqued_taxa_by_rank_dict
insert_taxa
shield_rank_name
get_all_rank_w_id
make_uniqued_taxa_by_rank_w_id_dict
insert_silva_taxonomy
silva_taxonomy
make_silva_taxonomy_rank_list_w_ids_dict
make_rank_name_id_t_id_str
make_silva_taxonomy_ids_dict
get_silva_taxonomy_ids
make_silva_taxonomy_id_per_taxonomy_dict

Seq
__init__
prepare_fasta_dict
make_seq_upper
insert_seq
get_seq_id_dict
prepare_pdr_info_values
get_seq_id_w_silva_taxonomy_info_per_seq_id
insert_sequence_uniq_info2
insert_sequence_uniq_info_ill
    """



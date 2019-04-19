import sys
import os
import time
import logging

logger = logging.getLogger('')
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)

"""TODO: get all info from vamps2, put into vampsdev"""

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

    def __init__(self, project_obj = None, db_name = None):

        self.db_name = db_name
        self.utils = util.Utils()
        self.project_obj = project_obj
        self.project_id = self.project_obj.project_id

        # mysql_utils = self.get_conn()

        self.db_marker = "vamps2"
        self.table_names = const.table_names_dict[self.db_marker]

        self.metadata_info = defaultdict(dict)

    def insert_bulk_data(self, key, values):
        query_tmpl = "INSERT IGNORE INTO %s (%s) VALUES (%s)"
        val_tmpl = "'%s'"
        my_sql = query_tmpl % (key, key, '), ('.join([val_tmpl % v for v in values]))
        my_sql = my_sql + " ON DUPLICATE KEY UPDATE %s = VALUES(%s);" % (key, key)
        mysql_utils_out.execute_no_fetch(my_sql)

    def make_sql_for_groups(self, table_name, fields_str):
        field_list = fields_str.split(",")
        my_sql_1 = "INSERT IGNORE INTO %s (%s) VALUES " % (table_name, fields_str)
        my_sql_2 = " ON DUPLICATE KEY UPDATE "
        for field_name in field_list[:-1]:
            my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
        my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (field_list[-1].strip(), field_list[-1].strip())
        return my_sql_1 + " %s " + my_sql_2

    # def get_conn(self):
    #
    #     if self.utils.is_local():
    #         is_local = "local"
    #     else:
    #         is_local = "development"
    #
    #     try:
    #         in_marker = "vamps2"
    #         out_marker = "vampsdev"
    #         host  = const.db_cnf['all_local'][in_marker]['host']
    #         db  = const.db_cnf['all_local'][in_marker]['db']
    #     except Exception:
    #         self.db_marker = "vamps2"
    #         host = const.db_cnf['vamps2']['development']['host']
    #         db = const.db_cnf['vamps2']['development']['db']
    #
    #     """            "all_local": {
    #             "env454"   : {"host": "localhost", "db": "test_env454"},
    #             "vamps2"   : {"host": "localhost", "db": "vamps2"},
    #             "vampsdev" : {"host": "localhost", "db": "vampsdev_testing"},
    #             "old_vamps": {"host": "localhost", "db": "test_vamps"}
    #         }"""


    def get_unknown_term_id(self):
        my_sql = "SELECT %s FROM %s WHERE %s = '%s';" % ("term_id", "term", "term_name", "unknown")
        # and ontology_id = 1
        # logger.debug("my_sql from get_all_metadata_info: %s" % my_sql)
        rows = mysql_utils_in.execute_fetch_select(my_sql)
        return [x[0] for x in rows[0]]

    # def empty_metadata_info(self):
    #     metadata_info = defaultdict(dict)
    #     keys = []
    #     # metadata_info['adaptor'] =
    #     # metadata_info['amp_operator'] =
    #     # metadata_info['anchor'] =
    #     # metadata_info['barcode'] =
    #     # metadata_info['barcode_index'] =
    #     metadata_info['data_owner'] = user_info.user_id
    #     # metadata_info['dataset'] =
    #     # metadata_info['dataset_description'] =
    #     # metadata_info['direction'] =
    #     # metadata_info['dna_region'] =
    #     # metadata_info['email'] =
    #     # metadata_info['env_sample_source_id'] =
    #     # metadata_info['first_name'] =
    #     # metadata_info['forward_primers'] =
    #     # metadata_info['funding'] =
    #     # metadata_info['insert_size'] =
    #     # metadata_info['institution'] =
    #     # metadata_info['lane'] =
    #     # metadata_info['last_name'] =
    #     # metadata_info['overlap'] =
    #     # metadata_info['pool'] =
    #     # metadata_info['primer_suite'] =
    #     # metadata_info['project'] =
    #     # metadata_info['project_description'] =
    #     # metadata_info['project_title'] =
    #     # metadata_info['read_length'] =
    #     # metadata_info['reverse_primers'] =
    #     # metadata_info['run_key'] =
    #     # metadata_info['seq_operator'] =
    #     # metadata_info['stop_sequences'] =
    #     # metadata_info['taxonomic_domain'] =
    #     # metadata_info['tubelabel'] =
    #     # metadata_info['use_mbl_primers'] =

    def get_all_metadata_info(self, run_info_obj):
        # missing_terms = []
        # if self.db_marker == "vamps2":
        # missing_terms = ["env_biome_id", "env_feature_id", "env_material_id", "geo_loc_name_id"]
        unknown_term_id = self.get_unknown_term_id()

        domain_by_adj = dict(zip(const.domain_adj, const.domains))
        domain_by_adj['Fungal'] = 'Eukarya'

        self.metadata_info = run_info_obj.run_info_by_dataset_id

        # for d_id, run_inf_entry in run_info_obj.items:
        # self.metadata_info['contact_id'] = self.get_user_id()
        # self.metadata_info['data_owner'] = user_info.user_id

            #
            # metadata_info['dataset_id'] = self.get_id('dataset', content_row.dataset)
            # metadata_info['dna_region_id'] = self.get_id('dna_region', content_row.dna_region)
            # metadata_info[
            #     'file_prefix'] = content_row.barcode_index + "_" + content_row.run_key + "_" + content_row.lane  # use self.runobj.idx_keys?
            # metadata_info['illumina_index_id'] = self.get_id('illumina_index', content_row.barcode_index)
            # if '_' in metadata_info['overlap']:
            #     metadata_info['overlap'] = metadata_info['overlap'].split("_")[1]  # hs_compete, ms_partial
            # metadata_info['platform'] = self.runobj.platform
            # metadata_info['primer_suite_id'] = self.get_id('primer_suite', content_row.primer_suite)
            # metadata_info['project_id'] = self.get_id('project', content_row.project)
            # metadata_info['run'] = self.rundate
            # metadata_info['run_id'] = self.run_id
            # if not self.run_id:
            #     metadata_info['run_id'] = self.get_id('run', self.rundate)
            # metadata_info['run_key_id'] = self.get_id('run_key', content_row.run_key)
            #
            # if self.db_marker == "vamps2":
            #     metadata_info['adapter_sequence_id'] = metadata_info['run_key_id']
            #
            #     and_part = ' and project_id = %s' % metadata_info['project_id']
            #     metadata_info['dataset_id'] = self.get_id('dataset', content_row.dataset, and_part = and_part)
            #
            #     metadata_info['domain_id'] = self.get_id('domain', domain_by_adj[content_row.taxonomic_domain])
            #     env_sample_source = self.get_env_sample_source(content_row)
            #     converted_env_sample_source = self.convert_env_sample_source(env_sample_source)
            #     metadata_info['env_package_id'] = self.get_id("env_package", converted_env_sample_source)
            #
            #     platform = self.runobj.platform
            #     if self.runobj.platform in const.illumina_list:
            #         platform = 'Illumina'
            #     metadata_info['sequencing_platform_id'] = self.get_id('sequencing_platform', platform)
            #     target_gene = '16s'
            #     if content_row.taxonomic_domain.lower().startswith(("euk", "its", "fung")):
            #         target_gene = '18s'
            #     metadata_info['target_gene_id'] = self.get_id('target_gene', target_gene)
            #     metadata_info['updated_at'] = self.runobj.configPath['general']['date']
            #     for term_name in missing_terms:
            #         metadata_info[term_name] = unknown_term_id[0][0]
            #
            # self.metadata_info_all[key] = metadata_info


    def make_insert_template(self, table_name, fields_str, values_str):
        my_sql_1 = "INSERT IGNORE INTO %s (%s) VALUES " % (table_name, fields_str)
        my_sql_2 = " ON DUPLICATE KEY UPDATE "

        field_list = fields_str.split(",")
        for field_name in field_list[:-1]:
            my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
        my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (field_list[-1].strip(), field_list[-1].strip())

        my_sql_tmpl = my_sql_1 + values_str + my_sql_2
        return my_sql_tmpl

    def get_run(self, run_info_obj):
        return set([(entry['run'], entry['run_prefix'], entry['date_trimmed'], entry['run.platform']) for entry in run_info_obj.run_info_t_dict])

    def insert_rundate(self, run_info_obj):
        run_vals = []
        run_rows = self.get_run(run_info_obj)
        for row in run_rows:
            run_str = '", "'.join(str(v) for v in row)
            run_vals.append('("%s")' % run_str)

        table_name = "run"
        fields_str = 'run, run_prefix, date_trimmed, platform'
        my_sql = self.make_insert_template(table_name, fields_str, ', '.join(run_vals))
        mysql_utils_out.execute_no_fetch(my_sql)

    def insert_contact(self, user_obj):
        # TODO: check what happens if this user_id exists
        fields = user_obj.user_info.keys()
        field_list = ", ".join(fields)
        user_values = user_obj.user_info.values()
        user_values_list = "', '".join(str(v) for v in user_values)
        my_sql = '''INSERT IGNORE INTO %s (%s)
                VALUES ('%s');''' % (self.table_names["contact"], field_list, user_values_list)

        return mysql_utils_out.execute_no_fetch(my_sql)

    # TODO: use for all? Separately for one liner and more
    def insert_project(self):
        fields_str = "%s" % (", ".join(str(x) for x in pr_info.keys()))

        vals_list = [str(x) for x in pr_info.values()]
        vals_str = "('%s')" % ("', '".join(vals_list))

        templ = self.make_sql_for_groups("project", fields_str)

        mysql_utils_out.execute_no_fetch(templ % vals_str)

        return pr_info['project']

    def insert_dataset(self):
        fields = "dataset, dataset_description"
        dataset_values = ""
        if self.db_marker == "vamps2":
            project_id = self.get_id('project', content_row.project)
            fields += ", project_id, updated_at"
            dataset_values = "('%s', '%s', %s, NOW())" % (
                content_row.dataset, content_row.dataset_description, project_id)
            # uniq_fields = ['dataset', 'project_id']
        elif self.db_marker == "env454":
            dataset_values = "('%s', '%s')" % (content_row.dataset, content_row.dataset_description)
            # uniq_fields = ['dataset', 'dataset_description']
        my_sql = make_sql_for_groups("dataset", fields) % dataset_values
        # self.utils.print_both(my_sql)
        return mysql_utils_out.execute_no_fetch(my_sql)

    def convert_env_sample_source(self, env_sample_source):
        if (env_sample_source == "miscellaneous_natural_or_artificial_environment"):
            env_sample_source_replaced = "miscellaneous"
        else:
            env_sample_source_replaced = env_sample_source.replace("_", " ")
        return env_sample_source_replaced

    def insert_run_keys(self, run_info_obj):
        run_keys = set([entry['run_key'] for entry in run_info_obj.run_info_t_dict])
        self.insert_bulk_data('run_key', run_keys)

    def insert_dna_regions(self, run_info_obj):
        dna_regions = set([entry['dna_region'] for entry in run_info_obj.run_info_t_dict])
        self.insert_bulk_data('dna_region', dna_regions)

    def insert_metadata_info(self, run_info_obj, user_obj):
        self.insert_run_keys(run_info_obj)
        self.insert_dna_regions(run_info_obj)
        self.insert_rundate(run_info_obj)
        self.insert_contact(user_obj)
        self.used_project_names = self.insert_project()
        self.insert_dataset()
        self.get_all_metadata_info_with_new_ids()
        self.insert_run_info()

class Dataset:

    def __init__(self, project_id = None):
        self.project_id = project_id
        self.db_marker = "vamps2"
        self.table_names = const.table_names_dict[self.db_marker]
        self.dataset_info = self.get_dataset_info()
        self.dataset_fields_list = self.dataset_info[1]
        print("HERE!")
        print(*utils.extract(self.dataset_info[0]))

        ", ".join(utils.extract(self.dataset_info[0]))
        flat_dat_info = utils.extract(self.dataset_info[0])
        # "', '".join(str(x) for x in utils.extract(self.dataset_info[0]))


        # self.dataset_ids_list = self.get_dataset_ids_for_project_id()
        # self.dataset_ids_string = "', '".join(str(x) for x in self.dataset_ids_list)

    def get_dataset_ids_for_project_id(self):
        where_part = "WHERE project_id = '%s'" % (self.project_id)
        dataset_ids_for_project_id_sql = """SELECT dataset_id FROM %s %s 
                                            """ % (self.table_names["connect_pr_dat_table"], where_part)

        rows = mysql_utils_in.execute_fetch_select(dataset_ids_for_project_id_sql)
        return [x[0] for x in rows[0]]
    
    def get_dataset_info(self):
        dataset_sql = "SELECT distinct * FROM dataset where project_id = '%s'" % (self.project_id)
        dataset_info = mysql_utils_in.execute_fetch_select(dataset_sql)
        return dataset_info

    # def get_dataset_per_run_info_id(self):
    #     all_dataset_run_info_sql = """SELECT run_info_ill_id, dataset_id FROM run_info_ill
    #                                 WHERE dataset_id in ('%s') """ % (self.dataset_ids_string)
    #     res = mysql_utils_in.execute_fetch_select_to_dict(all_dataset_run_info_sql)
    #     return res

class Project:

    def __init__(self, project = None):
        self.project = project
        self.get_project_id()

    def get_project_id(self):
        project_sql = "SELECT distinct project_id FROM project where project = '%s'" % (self.project)
        res = mysql_utils_in.execute_fetch_select_to_dict(project_sql)
        self.project_id = res[0]['project_id']

    def get_project_info(self):
        # "distinct" and "limit 1" are redundant for clarity, a project name is unique in the db
        project_sql = "SELECT distinct * FROM project where project = '%s' limit 1" % (self.project)
        project_info = mysql_utils_in.execute_fetch_select_to_dict(project_sql)
        return project_info[0]

class User:

    def __init__(self, user_id = None):
        self.user_id = user_id
        self.user_info = self.get_user_info()

    def get_user_info(self):
        """
        UNIQUE KEY `contact_email_inst` (`first_name`,`last_name`,`email`,`institution`),
        UNIQUE KEY `username` (`username`),

        """
        user_sql = "SELECT * FROM user where user_id = '%s'" % (self.user_id)
        res = mysql_utils_in.execute_fetch_select_to_dict(user_sql)
        return res[0]



class Run_info:
    def __init__(self):
        # upl
        self.run_info_t_dict = self.get_run_info()
        self.run_info_by_dataset_id = self.convert_run_info_to_dict_by_dataset_id()

    def get_run_info(self):
        my_sql = """SELECT * FROM run_info_ill
                    JOIN run using(run_id)
                    JOIN run_key using(run_key_id)
                    JOIN dna_region using(dna_region_id)
                    JOIN primer_suite using(primer_suite_id)
                    JOIN illumina_index using(illumina_index_id)
                    JOIN dataset using(dataset_id)
                    WHERE dataset_id in ('%s')
                    ;
        """ % (dat_obj.dataset_ids_string)

        rows = mysql_utils_in.execute_fetch_select_to_dict(my_sql)
        return rows

    def convert_run_info_to_dict_by_dataset_id(self):
        run_info_by_dataset_id = defaultdict(dict)

        for entry in self.run_info_t_dict:
            d_id = entry['dataset_id']
            run_info_by_dataset_id[d_id] = entry

        return run_info_by_dataset_id


class Constant:
    def __init__(self):
        self.ranks = ('domain', 'phylum', 'class', 'orderx', 'family', 'genus', 'species', 'strain')
        self.domains = ('Archaea', 'Bacteria', 'Eukarya', 'Organelle', 'Unknown')
        self.domain_adj = ('Archaeal', 'Bacterial', 'Eukaryal', 'Organelle', 'Unknown')  # Fungal
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
            },
            "all_local": {
                "env454"   : {"host": "localhost", "db": "test_env454"},
                "vamps2"   : {"host": "localhost", "db": "vamps2"},
                "vampsdev" : {"host": "localhost", "db": "vampsdev_testing"},
                "old_vamps": {"host": "localhost", "db": "test_vamps"}
            }

        }
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


if __name__ == '__main__':
    utils = util.Utils()

    const = Constant()

    in_marker = "vamps2"
    out_marker = "vampsdev"
    local_marker = "all_local"

    if (utils.is_local() == True):
        db_in  = const.db_cnf['all_local'][in_marker]['db']
        db_out = const.db_cnf['all_local'][out_marker]['db']

        mysql_utils_in  = util.Mysql_util(host = "localhost", db = db_in,  read_default_group = "clienthome")
        mysql_utils_out = util.Mysql_util(host = "localhost", db = db_out, read_default_group = "clienthome")
    else:
        mysql_utils = util.Mysql_util(host = "vampsdev", db = "vamps2", read_default_group = "client")


    # TODO: get from args
    project = "JG_NPO_Bv4v5"

    pr_obj = Project(project)
    pr_info = pr_obj.get_project_info()
    
    dat_obj = Dataset(pr_obj.project_id)
    dat_info = dat_obj.get_dataset_info()

    user_id = pr_info['owner_user_id']
    user_obj = User(user_id)

    upl = dbUpload(pr_obj) #don't send, it's available already. Make it clear

    run_info_obj = Run_info()
    upl.get_all_metadata_info(run_info_obj)
    upl.insert_metadata_info(run_info_obj, user_obj)

    insert_sql_template = "INSERT IGNORE INTO %s VALUES (%s)"

    insert_user_sql = insert_sql_template % ("user", user_id)

    print(upl.project_id)

    # tuple_of_dataset_and_run_info_ids = upl.get_dataset_per_run_info_id()

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



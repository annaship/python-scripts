import sys
import os
import time
import logging
import subprocess

logger = logging.getLogger('')
FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG,format=FORMAT)

"""TODO: get all info from vamps2, put into vampsdev"""

sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

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
    Name = "dbUpload"
    """
    Order:
        # insert_metadata_info_and_short_tables
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

        self.db_marker = "vamps2"
        self.table_names = const.table_names_dict[self.db_marker]

        self.metadata_info = defaultdict(dict)

    def execute_select_insert(self, table_name, fields_str, unique_fields, where_part = ""):
        sql1_select = "SELECT %s FROM %s %s" % (fields_str, table_name, where_part)
        try:
            mysql_utils_in.cursor.execute(sql1_select)
            rows = mysql_utils_in.cursor.fetchall()
            sql2_insert = "INSERT INTO %s (%s)" % (table_name, fields_str)
            fields_num_part = ", ". join(["%s" for x in range(len(fields_str.split(",")))])
            sql2_insert = sql2_insert + " values (%s)" % (fields_num_part)

            duplicate_update_part_list = []
            for unique_field in unique_fields.split(", "):
                duplicate_update_part_list.append("%s = VALUES (%s)" % (unique_field, unique_field))
            duplicate_update_part = ", ".join(duplicate_update_part_list)

            sql2_insert = sql2_insert + " ON DUPLICATE KEY UPDATE %s;" % duplicate_update_part

            try:
                rowcount = mysql_utils_out.cursor.executemany(sql2_insert, rows)
                mysql_utils_out.conn.commit()
            except:
                self.utils.print_both(("ERROR: query = %s") % sql2_insert)
                raise
        except:
            self.utils.print_both(("ERROR: query = %s") % sql1_select)
            raise

        return rowcount

    def table_dump(self, table_name, host_names, db_names, where_clause = ""):
        """
        :param table_name: "run"
        :param host_names: [in, out]
        :param db_names: [in, out]

        mysqldump database table_bame --where="date_column BETWEEN '2012-07-01 00:00:00' and '2012-12-01 00:00:00'"

        """
        if (where_clause):
            where_clause = "--where='%s'" % where_clause

        dump_command = 'mysqldump -h %s %s %s %s | mysql -h %s %s' % (host_names[0], db_names[0], table_name, where_clause,
                                                                      host_names[1], db_names[1])
        res = subprocess.check_output(dump_command,
                                    stderr = subprocess.STDOUT,
                                    shell = True)
        self.test_dump_result(res)

    def split_long_lists(self, my_list, chunk_size=None):
        if chunk_size is None:
            chunk_size = const.chunk_size
        # my_list = my_list[:10] #<class 'list'>: [195834, 197128, 201913, 202277, 205279, 205758, 206531, 206773, 207317, 207496]
        total_len = len(my_list)
        all_chunks = []

        for i in range(0, total_len, chunk_size):
            all_chunks.append(my_list[i:i + chunk_size])

        return all_chunks


    def test_dump_result(self, res):
        if (res):
            utils.print_both("Mysqldump error: %s" % res)

    def run_groups(self, group_vals, query_tmpl, join_xpr = ', '):
        for group in group_vals:
            val_part = join_xpr.join([key for key in group if key is not None])
            my_sql = query_tmpl % val_part
            insert_info = self.execute_no_fetch(my_sql)
            print(insert_info)

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

    def get_unknown_term_id(self):
        my_sql = "SELECT %s FROM %s WHERE %s = '%s';" % ("term_id", "term", "term_name", "unknown")
        # and ontology_id = 1
        # logger.debug("my_sql from get_all_metadata_info: %s" % my_sql)
        rows = mysql_utils_in.execute_fetch_select(my_sql)
        return [x[0] for x in rows[0]]

    def make_insert_template(self, table_name, fields_str, values_str):
        my_sql_1 = "INSERT IGNORE INTO %s (%s) VALUES " % (table_name, fields_str)
        my_sql_2 = " ON DUPLICATE KEY UPDATE "

        field_list = fields_str.split(",")
        for field_name in field_list[:-1]:
            my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
        my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (field_list[-1].strip(), field_list[-1].strip())

        my_sql_tmpl = my_sql_1 + values_str + my_sql_2
        return my_sql_tmpl

    # def insert_one_full_value(self, table_name, info_data):
    #     fields_str = "%s" % (", ".join(utils.convert_each_to_str(info_data.keys())))
    #
    #     vals_list = utils.convert_each_to_str(info_data.values())
    #     vals_str = "('%s')" % ("', '".join(vals_list))
    #
    #     templ = self.make_sql_for_groups(table_name, fields_str)
    #
    #     res = mysql_utils_out.execute_no_fetch(templ % vals_str)
    #     return res

    # def insert_multiple_values(self, table_name, fields_str, values_matrix):
    #     all_vals = []
    #     for row in values_matrix:
    #         vals_list = utils.convert_each_to_str(row)
    #         vals_str = "('%s')" % ("', '".join(vals_list))
    #         all_vals.append(vals_str)
    #
    #     dataset_values = ", ".join(all_vals)
    #     my_sql = self.make_sql_for_groups(table_name, fields_str)  % dataset_values
    #
    #     return mysql_utils_out.execute_no_fetch(my_sql)


    # def get_run(self, run_info_obj):
    #     return set([(entry['run_id'], entry['run'], entry['run_prefix'], entry['date_trimmed'], entry['run.platform']) for entry in run_info_obj.run_info_t_dict])

    # def insert_rundate(self, run_info_obj):
    #     # TODO: do like project, all at once
    #     run_vals = []
    #     run_rows = self.get_run(run_info_obj)
    #     for row in run_rows:
    #         run_str = '", "'.join(utils.convert_each_to_str(row))
    #         run_vals.append('("%s")' % run_str)
    #
    #     table_name = "run"
    #     fields_str = 'run_id, run, run_prefix, date_trimmed, platform'
    #     my_sql = self.make_insert_template(table_name, fields_str, ', '.join(run_vals))
    #     mysql_utils_out.execute_no_fetch(my_sql)
    #
    # def insert_dataset(self):
    #     fields_str = ", ".join(dataset_obj.dataset_fields_list)
    #     all_vals = []
    #     for row in dataset_obj.dataset_info[0]:
    #         vals_list = utils.convert_each_to_str(row)
    #         vals_str = "('%s')" % ("', '".join(vals_list))
    #         all_vals.append(vals_str)
    #
    #     table_name = "dataset"
    #     dataset_values = ", ".join(all_vals)
    #     my_sql = self.make_sql_for_groups(table_name, fields_str)  % dataset_values
    #
    #     return mysql_utils_out.execute_no_fetch(my_sql)

    # def convert_env_sample_source(self, env_sample_source):
    #     if (env_sample_source == "miscellaneous_natural_or_artificial_environment"):
    #         env_sample_source_replaced = "miscellaneous"
    #     else:
    #         env_sample_source_replaced = env_sample_source.replace("_", " ")
    #     return env_sample_source_replaced
    #
    # def insert_run_keys(self, run_info_obj):
    #     run_keys = set([entry['run_key'] for entry in run_info_obj.run_info_t_dict])
    #     self.insert_bulk_data('run_key', run_keys)

    # def insert_dna_regions(self, run_info_obj):
    #     dna_regions = set([entry['dna_region'] for entry in run_info_obj.run_info_t_dict])
    #     self.insert_bulk_data('dna_region', dna_regions)

    # def insert_run_info(self):
    #     run_info_obj.run_info_t_dict[0].values()

    def insert_metadata_info_and_short_tables(self):
        for table_name in const.full_short_ordered_tables:
            utils.print_both("Dump %s" % table_name)
            self.table_dump(table_name, [host_in, host_out], [db_in, db_out])

        custom_metadata_table_name = "custom_metadata_%s" % (self.project_id)
        utils.print_both("Dump %s" % custom_metadata_table_name)
        self.table_dump(custom_metadata_table_name, [host_in, host_out], [db_in, db_out])

    def insert_long_table_info(self, id_list, table_obj, id_name = None):
        if id_name is None:
            id_name = table_obj["id_name"]
        all_chunks = self.split_long_lists(id_list)
        table_name = table_obj["table_name"]
        fields_str = table_obj["fields_str"]
        unique_fields = table_obj["unique_fields_str"]
        for n, chunk in enumerate(all_chunks):
            chunk_str = utils.make_quoted_str(chunk)

            where_part = "WHERE %s in (%s)" % (id_name, chunk_str)
            utils.print_both("Dump %s, %d" % (table_name, n + 1))
            rowcount = self.execute_select_insert(table_name, fields_str, unique_fields, where_part = where_part)
            # utils.print_both("Inserted %d" % (rowcount))


    def call_insert_long_tables_info(self):
        self.insert_long_table_info(sequence_obj.sequence_id_list, sequence_obj.sequence_table_data)
        self.insert_long_table_info(sequence_obj.pdr_id_list, sequence_obj.pdr_info_table_data)
        self.insert_long_table_info(taxonomy_obj.silva_taxonomy_ids_list, taxonomy_obj.silva_taxonomy_table_data)
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.silva_taxonomy_info_per_seq_table_data, "sequence_id")
        self.insert_long_table_info(taxonomy_obj.rdp_taxonomy_ids_list, taxonomy_obj.rdp_taxonomy_table_data)
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.rdp_taxonomy_info_per_seq_table_data, "sequence_id")
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.sequence_uniq_info_table_data, "sequence_id")

class Dataset:

    def __init__(self, project_id = None):
        self.project_id = project_id
        self.db_marker = "vamps2"
        self.table_names = const.table_names_dict[self.db_marker]

        self.dataset_info = self.get_dataset_info()
        self.dataset_fields_list = self.dataset_info[1]
        self.dataset_fields_str = ", ".join(self.dataset_fields_list)

        self.dataset_values_matrix = self.dataset_info[0]

        self.dataset_ids_list = self.get_dataset_ids_for_project_id()
        self.dataset_ids_string = utils.make_quoted_str(self.dataset_ids_list)

    def get_dataset_ids_for_project_id(self):
        where_part = "WHERE project_id = '%s'" % (self.project_id)
        dataset_ids_for_project_id_sql = """SELECT dataset_id FROM %s %s 
                                            """ % (self.table_names["connect_pr_dat_table"], where_part)

        rows = mysql_utils_in.execute_fetch_select(dataset_ids_for_project_id_sql)
        return list(utils.extract(rows[0]))
    
    def get_dataset_info(self):
        dataset_sql = "SELECT distinct * FROM dataset where project_id = '%s'" % (self.project_id)
        dataset_info = mysql_utils_in.execute_fetch_select(dataset_sql)
        # self.dataset_info_dict = mysql_utils_in.execute_fetch_select_to_dict(dataset_sql)
        # print("HERE!")
        return dataset_info

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

class Run_info:
    def __init__(self):
        # upl
        self.run_info_t_dict = self.get_run_info()
        self.run_info_by_dataset_id = self.convert_run_info_to_dict_by_dataset_id()
        self.used_run_info_id_list = self.get_used_run_info_ids()
        self.used_run_info_id_str = utils.make_quoted_str(self.used_run_info_id_list)


    def get_run_info(self):
        my_sql = """SELECT * FROM run_info_ill
                    JOIN run using(run_id)
                    JOIN run_key using(run_key_id)
                    JOIN dna_region using(dna_region_id)
                    JOIN primer_suite using(primer_suite_id)
                    JOIN illumina_index using(illumina_index_id)
                    JOIN dataset using(dataset_id)
                    WHERE dataset_id in (%s)
                    ;
        """ % (dataset_obj.dataset_ids_string)

        rows = mysql_utils_in.execute_fetch_select_to_dict(my_sql)
        return rows

    def convert_run_info_to_dict_by_dataset_id(self):
        run_info_by_dataset_id = defaultdict(dict)

        for entry in self.run_info_t_dict:
            d_id = entry['dataset_id']
            run_info_by_dataset_id[d_id] = entry

        return run_info_by_dataset_id

    def get_used_run_info_ids(self):
        return [entry['run_info_ill_id'] for entry in self.run_info_t_dict]

class LongTables:
    def __init__(self, project_id):
        self.utils = util.Utils()

    def get_table_data(self, table_name):
        table_data = defaultdict()

        table_data["table_name"] = table_name
        table_data["id_name"] = table_name + "_id"
        table_data["fields"] = mysql_utils_in.get_field_names(table_name)
        table_data["fields_str"] = ", ".join([x[0] for x in table_data["fields"][0]])
        table_data["unique_fields"] = mysql_utils_in.get_uniq_index_columns(db_in, table_name)
        table_data["unique_fields_str"] = ", ".join(table_data["unique_fields"])
        return table_data

class Seq(LongTables):
    """
    get sequence ids
    get their amount
    upload by chunks (in upload class):
             mysql_utils.execute_no_fetch_w_info(q_update_table_look_up_tax % (counter, chunk_size))

    """
    def __init__(self, project_id):
        pdr_info_table_name = table_names["sequence_pdr_info_table_name"]
        self.pdr_info_table_data = self.get_table_data(pdr_info_table_name)

        sequence_table_name = table_names["sequence_table_name"]
        self.sequence_table_data = self.get_table_data(sequence_table_name)

        pdr_id_seq_id = self.get_pdr_info()

        self.pdr_id_list = [x[0] for x in pdr_id_seq_id[0]]
        self.pdr_id_list_str = utils.make_quoted_str(self.pdr_id_list)

        self.sequence_id_list = [x[1] for x in pdr_id_seq_id[0]]
        self.sequence_id_str = utils.make_quoted_str(self.sequence_id_list)

    def get_pdr_info(self):
        # SELECT sequence_pdr_info_id, sequence_id
        all_seq_ids_sql = """SELECT DISTINCT %s, %s FROM %s
                             WHERE dataset_id IN (%s)
                             AND run_info_ill_id IN (%s)""" % (self.pdr_info_table_data["id_name"], self.sequence_table_data["id_name"], self.pdr_info_table_data["table_name"],
                                                             dataset_obj.dataset_ids_string,
                                                             run_info_obj.used_run_info_id_str)

        rows = mysql_utils_in.execute_fetch_select(all_seq_ids_sql)
        return rows


class Taxonomy(LongTables):
    def __init__(self, sequence_id_str):
        self.sequence_id_str = sequence_id_str
        self.table_names_to_insert = ["strain", "genus", "domain", "family", "klass", "order", "phylum", "species",
                                 "silva_taxonomy", "silva_taxonomy_info_per_seq",
                                 "generic_taxonomy", "generic_taxonomy_info",
                                 "rdp_taxonomy", "rdp_taxonomy_info_per_seq",
                                 "sequence_uniq_info"]

        self.table_names_to_get_ids_second = ["strain", "genus", "domain", "family", "klass", "order", "phylum", "species"]
        self.long_tax_tables = ["silva_taxonomy", "silva_taxonomy_info_per_seq", "rdp_taxonomy", "rdp_taxonomy_info_per_seq",
                                 "sequence_uniq_info"]

        self.get_ids()
        self.silva_taxonomy_table_data = self.get_table_data("silva_taxonomy")
        self.silva_taxonomy_info_per_seq_table_data = self.get_table_data("silva_taxonomy_info_per_seq")
        self.rdp_taxonomy_table_data = self.get_table_data("rdp_taxonomy")
        self.rdp_taxonomy_info_per_seq_table_data = self.get_table_data("rdp_taxonomy_info_per_seq")
        self.sequence_uniq_info_table_data = self.get_table_data("sequence_uniq_info")

    def get_ids(self):
        where_id_name = "sequence_id"
        where_id_str = self.sequence_id_str

        what_to_select = "sequence_uniq_info_id"
        from_table_name = "sequence_uniq_info"
        self.sequence_uniq_info_ids = self.get_all_ids_from_db(what_to_select, from_table_name, where_id_name, where_id_str)

        what_to_select = "silva_taxonomy_id"
        from_table_name = "silva_taxonomy_info_per_seq"
        self.silva_taxonomy_ids = self.get_all_ids_from_db(what_to_select, from_table_name, where_id_name, where_id_str)
        self.silva_taxonomy_ids_list = [x[0] for x in self.silva_taxonomy_ids[0]]
        self.silva_taxonomy_str = utils.make_quoted_str(self.silva_taxonomy_ids_list)

        what_to_select = "rdp_taxonomy_id"
        from_table_name = "rdp_taxonomy_info_per_seq"
        self.rdp_taxonomy_ids = self.get_all_ids_from_db(what_to_select, from_table_name, where_id_name, where_id_str)
        self.rdp_taxonomy_ids_list = [x[0] for x in self.rdp_taxonomy_ids[0]]
        self.rdp_taxonomy_str = utils.make_quoted_str(self.rdp_taxonomy_ids_list)

    def get_all_ids_from_db(self, what_to_select, from_table_name, where_id_name, where_id_str):
        all_ids_sql = """SELECT %s FROM %s
                         WHERE %s IN (%s)
                         """ % (what_to_select,
                                from_table_name,
                                where_id_name,
                                where_id_str)

        rows = mysql_utils_in.execute_fetch_select(all_ids_sql)
        return rows


class Constant:
    def __init__(self):

        self.chunk_size = 1000
        self.full_short_ordered_tables = ["classifier", "dna_region", "domain", "env_package", "illumina_adaptor", "illumina_index", "illumina_run_key", "illumina_adaptor_ref", "primer_suite", "rank", "run", "run_key", "sequencing_platform", "target_gene", "primer_suite"
                                         , "user", "project", "dataset", "run_info_ill", "required_metadata_info", "custom_metadata_fields", "rank", "domain", "phylum", "klass", "order", "family", "genus", "species", "strain"]
        self.ranks = ('domain', 'phylum', 'class', 'orderx', 'family', 'genus', 'species', 'strain')
        self.domains = ('Archaea', 'Bacteria', 'Eukarya', 'Organelle', 'Unknown')
        self.domain_adj = ('Archaeal', 'Bacterial', 'Eukaryal', 'Organelle', 'Unknown')  # Fungal
        self.db_cnf = {
            "vamps2": {
                "local"      : {"host": "localhost", "db": "vamps2"},
                "production" : {"host": "vampsdb", "db": "vamps2"},
                "development": {"host": "bpcweb7", "db": "vamps2"}
            },
            "env454": {
                "local"      : {"host": "localhost", "db": "test_env454"},
                "production" : {"host": "bpcdb1", "db": "env454"},
                "development": {"host": "bpcweb7.bpcservers.private", "db": "test"}
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

    # TODO: change in dbUpload class to use this
    table_names = const.table_names_dict[in_marker]

    if (utils.is_local() == True):
        db_in  = const.db_cnf['all_local'][in_marker]['db']
        db_out = const.db_cnf['all_local'][out_marker]['db']
        host_in  = const.db_cnf['all_local'][in_marker]['host']
            # "localhost"
        host_out = const.db_cnf['all_local'][out_marker]['host']

        mysql_utils_in  = util.Mysql_util(host = host_in, db = db_in,  read_default_group = "clienthome")
        mysql_utils_out = util.Mysql_util(host = host_out, db = db_out, read_default_group = "clienthome")
    else:
        host_in = const.db_cnf['vamps2']['production']['host'] # "vampsdb"
        host_out = const.db_cnf['vamps2']['development']['host'] # "vampsdev"

        db_in  = "vamps2"
        db_out = "vamps2"

        mysql_utils_in = util.Mysql_util(host = host_in, db = db_in, read_default_group = "client")
        mysql_utils_in = util.Mysql_util(host = host_out, db = db_out, read_default_group = "client")


    # TODO: get from args
    project = "SLM_CITY_Bv4v5"

    project_obj = Project(project)
    project_info = project_obj.get_project_info()
    
    dataset_obj = Dataset(project_obj.project_id)

    user_id = project_info['owner_user_id']
    # user_obj = User(user_id)

    upl = dbUpload(project_obj) #TODO: don't send, it's available already. Make it clear

    run_info_obj = Run_info()

    # TODO: restore! Commented for testing
    # upl.insert_metadata_info_and_short_tables()
    sequence_obj = Seq(project_obj.project_id)
    taxonomy_obj = Taxonomy(sequence_obj.sequence_id_str)
    # TODO: restore! Commented for testing
    upl.call_insert_long_tables_info()



    utils.print_both("project_id = %s" % upl.project_id)

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



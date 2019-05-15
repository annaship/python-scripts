import sys
import os
import time
import subprocess
import argparse

"""Gets info from vamps2, puts into vampsdev or into files"""

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


class Current_connection:

    def __init__(self, args = None):

        self.args = args

        self.in_marker = "vamps2"
        self.out_marker = "vampsdev"
        self.local_marker = "all_local"

        self.table_names = const.table_names_dict[self.in_marker]

        self.db_info_dict = self.get_db_info_dict()

        self.mysql_utils_in = util.Mysql_util(host = self.db_info_dict["host_in"],
                                              db = self.db_info_dict["db_in"],
                                              read_default_group = self.db_info_dict["read_default_group"])
        self.mysql_utils_out = util.Mysql_util(host = self.db_info_dict["host_out"],
                                               db = self.db_info_dict["db_out"],
                                               read_default_group = self.db_info_dict["read_default_group"])

    def get_db_info_dict(self):
        db_info_dict = {}
        if (utils.is_local() == True):
            db_info_dict["host_in"] = const.db_cnf['all_local'][self.in_marker]['host']
            db_info_dict["host_out"] = const.db_cnf['all_local'][self.out_marker]['host']

            db_info_dict["db_in"] = const.db_cnf['all_local'][self.in_marker]['db']
            db_info_dict["db_out"] = const.db_cnf['all_local'][self.out_marker]['db']

            db_info_dict["read_default_group"] = "clienthome"

        else:
            db_info_dict["host_in"] = const.db_cnf['vamps2']['production']['host']  # "vampsdb"
            db_info_dict["host_out"] = const.db_cnf['vamps2']['development']['host']  # "vampsdev"

            db_info_dict["db_in"] = "vamps2"
            db_info_dict["db_out"] = "vamps2"

            db_info_dict["read_default_group"] = "client"

        if self.args.host_in:
            db_info_dict["host_in"] = self.args.host_in
        if self.args.host_out:
            db_info_dict["host_out"] = self.args.host_out
        if self.args.db_in:
            db_info_dict["db_in"] = self.args.db_in
        if self.args.db_out:
            db_info_dict["db_out"] = self.args.db_out

        return db_info_dict


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

    def __init__(self, project_obj, curr_connection):

        # self.utils = util.Utils()
        self.project_obj = project_obj
        self.project_id = self.project_obj.project_id

        self.metadata_info = defaultdict(dict)

        self.host_in = curr_conn_obj.db_info_dict["host_in"]
        self.db_in = curr_conn_obj.db_info_dict["db_in"]
        self.host_out = curr_conn_obj.db_info_dict["host_out"]
        self.db_out = curr_conn_obj.db_info_dict["db_out"]

        self.mysql_utils_in = curr_conn_obj.mysql_utils_in
        self.mysql_utils_out = curr_conn_obj.mysql_utils_out

    def execute_select_insert(self, table_name, fields_str, unique_fields, where_part = "", chunk_num = None):
        if chunk_num is None:
            chunk_num = 0
        sql1_select = "SELECT %s FROM %s %s" % (fields_str, table_name, where_part)
        try:
            self.mysql_utils_in.cursor.execute(sql1_select)
            rows = self.mysql_utils_in.cursor.fetchall()
            sql2_insert = "INSERT INTO %s (%s)" % (table_name, fields_str)
            fields_num_part = ", ". join(["%s" for x in range(len(fields_str.split(",")))])
            sql2_insert = sql2_insert + " values (%s)" % (fields_num_part)

            duplicate_update_part_list = []
            for unique_field in unique_fields.split(", "):
                duplicate_update_part_list.append("%s = VALUES (%s)" % (unique_field, unique_field))
            duplicate_update_part = ", ".join(duplicate_update_part_list)

            sql2_insert = sql2_insert + " ON DUPLICATE KEY UPDATE %s;" % duplicate_update_part
            try:
                rowcount = self.mysql_utils_out.cursor.executemany(sql2_insert, rows)
                self.mysql_utils_out.conn.commit()
            except:
                utils.print_both(("ERROR: query = %s") % sql2_insert)
                raise
        except:
            utils.print_both(("ERROR: query = %s") % sql1_select)
            raise

        return rowcount

    def table_dump_to_db(self, table_name, where_clause = ""):
        """
        :param table_name: "run"

        mysqldump database table_name --where="date_column BETWEEN '2012-07-01 00:00:00' and '2012-12-01 00:00:00'"

        """
        if (where_clause):
            where_clause = "--where='%s'" % where_clause

        dump_command = 'mysqldump -h %s %s %s %s | mysql -h %s %s' % (self.host_in, self.db_in, table_name, where_clause,
                                                                      self.host_out, self.db_out)
        res = subprocess.check_output(dump_command,
                                    stderr = subprocess.STDOUT,
                                    shell = True)
        self.test_dump_result(res)

    def part_dump_to_file(self, table_name, where_clause = "", file_out_name = "", no_drop_and_create = ""):
        file_out_name += ".gz"
        if where_clause:
            where_clause = "--where='%s'" % where_clause.lstrip("WHERE")

        if no_drop_and_create:
            no_drop_and_create = "--skip-add-drop-table --no-create-info"

        if utils.check_if_file_exists(file_out_name):
            utils.print_both('WARNING: File %s already exists! The script will not overwrite it.' % file_out_name)
            return
        else:
            res_file = subprocess.check_output("touch %s" % file_out_name,
                                        stderr = subprocess.STDOUT,
                                        shell = True)

        dump_command = 'mysqldump -h %s --insert-ignore %s %s %s %s | gzip > %s' % (self.host_in, self.db_in, table_name, where_clause,
                                                                    no_drop_and_create,
                                                                    file_out_name)
        res = subprocess.check_output(dump_command,
                                    stderr = subprocess.STDOUT,
                                    shell = True)
        return res

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
            print("insert_info from run_groups")
            print(insert_info)

    def insert_bulk_data(self, key, values):
        query_tmpl = "INSERT IGNORE INTO %s (%s) VALUES (%s)"
        val_tmpl = "'%s'"
        my_sql = query_tmpl % (key, key, '), ('.join([val_tmpl % v for v in values]))
        my_sql = my_sql + " ON DUPLICATE KEY UPDATE %s = VALUES(%s);" % (key, key)
        self.mysql_utils_out.execute_no_fetch(my_sql)

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
        rows = self.mysql_utils_in.execute_fetch_select(my_sql)
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

    def make_file_out_num_name(self, file_prefix, table_number, table_name, add_more = None):
        if add_more == None:
            add_more = ""
        else:
            add_more = ".%s" % add_more
        file_out_name = file_prefix + "%s.%s" + add_more + ".sql"
        return file_out_name % (table_number, table_name)

    def dump_metadata_info_and_short_tables(self, file_prefix):
        table_number = 0

        for table_name in const.full_short_ordered_tables:
            table_number += 1
            utils.print_both("Dump %s" % table_name)
            file_out_num_name = self.make_file_out_num_name(file_prefix, table_number, table_name)
            self.part_dump_to_file(table_name, "", file_out_num_name)

        custom_metadata_table_name = "custom_metadata_%s" % (self.project_id)
        utils.print_both("Dump %s" % custom_metadata_table_name)
        file_out_num_name = self.make_file_out_num_name(file_prefix, table_number, custom_metadata_table_name)
        self.part_dump_to_file(custom_metadata_table_name, "", file_out_num_name)

    def insert_metadata_info_and_short_tables(self):
        for table_name in const.full_short_ordered_tables:
            utils.print_both("Dump %s" % table_name)
            self.table_dump_to_db(table_name)

        custom_metadata_table_name = "custom_metadata_%s" % (self.project_id)
        utils.print_both("Dump %s" % custom_metadata_table_name)
        self.table_dump_to_db(custom_metadata_table_name)

    def insert_long_table_info(self, id_list, table_obj, file_prefix = None, id_name = None, long_table_num = None):
        if long_table_num is None:
            long_table_num = 0
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
            chunk_num = n
            if file_prefix:
                file_out_name = self.make_file_out_num_name(file_prefix, long_table_num, table_name, chunk_num)
                # file_out_name = file_prefix + ".%s.%s.sql" % (table_name, chunk_num)
                self.part_dump_to_file(table_name, where_part, file_out_name, "no_drop")
                # part_dump_to_file(self, table_name, where_clause = "", file_out_name = "", no_drop = ""):
            else:
                rowcount = self.execute_select_insert(table_name, fields_str, unique_fields, where_part = where_part, chunk_num = chunk_num)
            # utils.print_both("Inserted %d" % (rowcount))


    def call_insert_long_tables_info(self, file_out_name = None):
        long_table_num = 0
        self.insert_long_table_info(sequence_obj.sequence_id_list, sequence_obj.sequence_table_data, file_out_name, long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(sequence_obj.pdr_id_list, sequence_obj.pdr_info_table_data, file_out_name, long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(taxonomy_obj.silva_taxonomy_ids_list, taxonomy_obj.silva_taxonomy_table_data, file_out_name, long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.silva_taxonomy_info_per_seq_table_data, file_out_name, "sequence_id", long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(taxonomy_obj.rdp_taxonomy_ids_list, taxonomy_obj.rdp_taxonomy_table_data, file_out_name, long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.rdp_taxonomy_info_per_seq_table_data, file_out_name, "sequence_id", long_table_num)
        long_table_num = long_table_num + 1
        self.insert_long_table_info(sequence_obj.sequence_id_list, taxonomy_obj.sequence_uniq_info_table_data, file_out_name, "sequence_id", long_table_num)

class Dataset:

    def __init__(self, project_id, curr_connection):
        self.project_id = project_id

        self.dataset_info = self.get_dataset_info()
        self.dataset_fields_list = self.dataset_info[1]
        self.dataset_fields_str = ", ".join(self.dataset_fields_list)

        self.dataset_values_matrix = self.dataset_info[0]

        self.dataset_ids_list = self.get_dataset_ids_for_project_id()
        self.dataset_ids_string = utils.make_quoted_str(self.dataset_ids_list)

    def get_dataset_ids_for_project_id(self):
        where_part = "WHERE project_id = '%s'" % (self.project_id)
        dataset_ids_for_project_id_sql = """SELECT dataset_id FROM %s %s 
                                            """ % (curr_conn_obj.table_names["connect_pr_dat_table"], where_part)

        rows = curr_conn_obj.mysql_utils_in.execute_fetch_select(dataset_ids_for_project_id_sql)
        return list(utils.extract(rows[0]))
    
    def get_dataset_info(self):
        dataset_sql = "SELECT distinct * FROM dataset where project_id = '%s'" % (self.project_id)
        dataset_info = curr_conn_obj.mysql_utils_in.execute_fetch_select(dataset_sql)
        return dataset_info

class Project:

    def __init__(self, project, curr_conn_obj):
        self.project = project
        self.get_project_id()

    def get_project_id(self):
        project_sql = "SELECT distinct project_id FROM project where project = '%s'" % (self.project)
        res = curr_conn_obj.mysql_utils_in.execute_fetch_select_to_dict(project_sql)
        self.project_id = res[0]['project_id']

    def get_project_info(self):
        # "distinct" and "limit 1" are redundant for clarity, a project name is unique in the db
        project_sql = "SELECT distinct * FROM project where project = '%s' limit 1" % (self.project)
        project_info = curr_conn_obj.mysql_utils_in.execute_fetch_select_to_dict(project_sql)
        return project_info[0]

class Run_info:
    def __init__(self, curr_conn_obj):
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

        rows = curr_conn_obj.mysql_utils_in.execute_fetch_select_to_dict(my_sql)
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
    def __init__(self, curr_conn_obj):
        self.utils = util.Utils()

    def get_table_data(self, table_name):
        table_data = defaultdict()

        table_data["table_name"] = table_name
        table_data["id_name"] = table_name + "_id"
        table_data["fields"] = curr_conn_obj.mysql_utils_in.get_field_names(table_name)
        table_data["fields_str"] = ", ".join([x[0] for x in table_data["fields"][0]])
        table_data["unique_fields"] = curr_conn_obj.mysql_utils_in.get_uniq_index_columns(curr_conn_obj.db_info_dict["db_in"], table_name)
        table_data["unique_fields_str"] = ", ".join(table_data["unique_fields"])
        return table_data

class Seq(LongTables):
    """
    get sequence ids
    get their amount
    upload by chunks (in upload class):
             mysql_utils.execute_no_fetch_w_info(q_update_table_look_up_tax % (counter, chunk_size))

    """
    def __init__(self, project_id, curr_conn_obj):

        pdr_info_table_name = curr_conn_obj.table_names["sequence_pdr_info_table_name"]
        self.pdr_info_table_data = self.get_table_data(pdr_info_table_name)

        sequence_table_name = curr_conn_obj.table_names["sequence_table_name"]
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

        rows = curr_conn_obj.mysql_utils_in.execute_fetch_select(all_seq_ids_sql)
        return rows


class Taxonomy(LongTables):
    def __init__(self, sequence_id_str, curr_conn_obj):
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
        try:
            self.silva_taxonomy_ids_list = [x[0] for x in self.silva_taxonomy_ids[0]]
        except TypeError:
            utils.print_both("No silva_taxonomy_ids", "error")
            self.silva_taxonomy_ids_list = []
        except:
            raise

        self.silva_taxonomy_str = utils.make_quoted_str(self.silva_taxonomy_ids_list)

        what_to_select = "rdp_taxonomy_id"
        from_table_name = "rdp_taxonomy_info_per_seq"
        self.rdp_taxonomy_ids = self.get_all_ids_from_db(what_to_select, from_table_name, where_id_name, where_id_str)
        try:
            self.rdp_taxonomy_ids_list = [x[0] for x in self.rdp_taxonomy_ids[0]]
        except TypeError:
            utils.print_both("No rdp_taxonomy_ids", "error")
            self.rdp_taxonomy_ids_list = []
        except:
            raise
        self.rdp_taxonomy_str = utils.make_quoted_str(self.rdp_taxonomy_ids_list)

    def get_all_ids_from_db(self, what_to_select, from_table_name, where_id_name, where_id_str):
        all_ids_sql = """SELECT %s FROM %s
                         WHERE %s IN (%s)
                         """ % (what_to_select,
                                from_table_name,
                                where_id_name,
                                where_id_str)

        try:
            rows = curr_conn_obj.mysql_utils_in.execute_fetch_select(all_ids_sql)
            return rows
        except:
            utils.print_both("Error running this query: %s" % (all_ids_sql))



class Constant:
    def __init__(self):

        self.chunk_size = 1000
        self.full_short_ordered_tables = ["classifier", "dna_region", "domain", "env_package", "illumina_adaptor", "illumina_index"
            , "illumina_run_key", "illumina_adaptor_ref", "primer_suite", "rank", "run", "run_key", "sequencing_platform", "target_gene"
            , "user", "project", "dataset", "run_info_ill", "required_metadata_info", "custom_metadata_fields"
            , "rank", "phylum", "klass", "order", "family", "genus", "species", "strain"]
        self.ranks = ('domain', 'phylum', 'class', 'orderx', 'family', 'genus', 'species', 'strain')
        self.domains = ('Archaea', 'Bacteria', 'Eukarya', 'Organelle', 'Unknown')
        self.domain_adj = ('Archaeal', 'Bacterial', 'Eukaryal', 'Organelle', 'Unknown')  # Fungal
        self.db_cnf = {
            "vamps2": {
                "local"      : {"host": "localhost", "db": "vamps2", "read_default_group": "clienthome"},
                "production" : {"host": "vampsdb", "db": "vamps2", "read_default_group": "client"},
                "development": {"host": "bpcweb7", "db": "vamps2", "read_default_group": "client"}
            },
            "env454": {
                "local"      : {"host": "localhost", "db": "test_env454"},
                "production" : {"host": "bpcdb1", "db": "env454"},
                "development": {"host": "bpcweb7.bpcservers.private", "db": "test"}
            },
            "all_local": {
                "env454"   : {"host": "localhost", "db": "test_env454", "read_default_group": "clienthome"},
                "vamps2"   : {"host": "localhost", "db": "vamps2", "read_default_group": "clienthome"},
                "vampsdev" : {"host": "localhost", "db": "vampsdev_testing", "read_default_group": "clienthome"},
                "old_vamps": {"host": "localhost", "db": "test_vamps", "read_default_group": "clienthome"}
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

def get_args():
  parser = argparse.ArgumentParser()

  parser.add_argument("--project_name", "-p", type=str, required=True)
  parser.add_argument("--file_out", "-f", type=str, required=False)
  parser.add_argument("--host_in", "-hi", type=str, required=False)
  parser.add_argument("--host_out", "-ho", type=str, required=False)
  parser.add_argument("--db_in", "-di", type=str, required=False)
  parser.add_argument("--db_out", "-do", type=str, required=False)

  args = parser.parse_args()

  return args

if __name__ == '__main__':
    utils = util.Utils()
    args = get_args()

    const = Constant()
    curr_conn_obj = Current_connection(args)

    if args.project_name:
        project = args.project_name

    project_obj = Project(project, curr_conn_obj)
    project_info = project_obj.get_project_info()
    
    dataset_obj = Dataset(project_obj.project_id, curr_conn_obj)

    user_id = project_info['owner_user_id']
    # user_obj = User(user_id)

    upl = dbUpload(project_obj, curr_conn_obj)

    run_info_obj = Run_info(curr_conn_obj)

    file_out_name = ""
    if args.file_out:
        file_out_name = args.file_out
        upl.dump_metadata_info_and_short_tables(file_out_name)
    else:
        upl.insert_metadata_info_and_short_tables()

    # TODO: change to the abstract class call - long tables
    utils.print_both("Making seq obj...", log_level_name = "info")
    sequence_obj = Seq(project_obj.project_id, curr_conn_obj)
    utils.print_both("Making tax obj...", log_level_name = "INFO")
    taxonomy_obj = Taxonomy(sequence_obj.sequence_id_str, curr_conn_obj)
    upl.call_insert_long_tables_info(file_out_name)

    utils.print_both("project_id = %s" % upl.project_id)


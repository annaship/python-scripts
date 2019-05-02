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
        # insert_metadata_info
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
            sql2_insert = "INSERT IGNORE INTO %s (%s)" % (table_name, fields_str)
            fields_num_part = ", ". join(["%s" for x in range(len(fields_str.split(",")))])
            # sql2 = sql2 + " values (%s, %s, %s, %s)"
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

    def insert_metadata_info(self):
        for table_name in const.full_short_ordered_tables:
            utils.print_both("Dump %s" % table_name)
            self.table_dump(table_name, [host_in, host_out], [db_in, db_out])

        custom_metadata_table_name = "custom_metadata_%s" % (self.project_id)
        utils.print_both("Dump %s" % custom_metadata_table_name)
        self.table_dump(custom_metadata_table_name, [host_in, host_out], [db_in, db_out])

    def insert_sequence(self):
        # short_list = sequence_obj.pdr_id_list[0:20]
        all_chunks = self.split_long_lists(sequence_obj.sequence_id_list)
        where_part = ""
        table_name = sequence_obj.sequence_name
        fields_str = sequence_obj.seq_fields_str
            # "sequence_id, sequence_comp, created_at, updated_at"
        unique_fields = sequence_obj.sequence_uniq_index_str
        for n, chunk in enumerate(all_chunks):
            chunk_str = utils.make_quoted_str(chunk)

            where_part = "WHERE %s_id in (%s)" % (table_name, chunk_str)
            utils.print_both("Dump %s, %d" % (table_name, n+1))
            rowcount = self.execute_select_insert(table_name, fields_str, unique_fields, where_part = where_part)
            utils.print_both("Inserted %d" % (rowcount))

    def insert_pdr_info(self):
        # short_list = sequence_obj.pdr_id_list[0:20]
        all_chunks = self.split_long_lists(sequence_obj.pdr_id_list)
        table_name = sequence_obj.pdr_info_table_data["table_name"]
        fields_str = sequence_obj.pdr_info_table_data["fields_str"]
        unique_fields = sequence_obj.pdr_info_table_data["unique_fields_str"]
        for n, chunk in enumerate(all_chunks):
            chunk_str = utils.make_quoted_str(chunk)

            where_part = "WHERE %s in (%s)" % (sequence_obj.pdr_info_table_data["id_name"], chunk_str)
            utils.print_both("Dump %s, %d" % (table_name, n+1))
            rowcount = self.execute_select_insert(table_name, fields_str, unique_fields, where_part = where_part)
            utils.print_both("Inserted %d" % (rowcount))

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

# class User:
#
#     def __init__(self, user_id = None):
#         self.user_id = user_id
#         self.user_info = self.get_user_info()
#
#     def get_user_info(self):
#         """
#         UNIQUE KEY `contact_email_inst` (`first_name`,`last_name`,`email`,`institution`),
#         UNIQUE KEY `username` (`username`),
#
#         """
#         user_sql = "SELECT * FROM user where user_id = '%s'" % (self.user_id)
#         res = mysql_utils_in.execute_fetch_select_to_dict(user_sql)
#         return res[0]

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

class Taxonomy:
    def __init__(self, my_conn):

        self.utils = util.Utils()
        self.my_conn = my_conn
        self.taxa_content = set()
        self.ranks = ['domain', 'phylum', 'klass', 'order', 'family', 'genus', 'species', 'strain']
        self.taxa_by_rank = []
        self.all_rank_w_id = set()
        self.uniqued_taxa_by_rank_dict = {}
        self.uniqued_taxa_by_rank_w_id_dict = {}
        self.tax_id_dict = {}
        self.taxa_list_dict = {}
        self.taxa_list_w_empty_ranks_dict = defaultdict(list)
        self.taxa_list_w_empty_ranks_ids_dict = defaultdict(list)
        self.silva_taxonomy_rank_list_w_ids_dict = defaultdict(list)
        self.silva_taxonomy_ids_dict = defaultdict(list)
        self.silva_taxonomy_id_per_taxonomy_dict = defaultdict(list)
        self.get_all_rank_w_id()

    def get_taxonomy_from_gast(self, gast_dict):
        self.taxa_content = set(v[0] for v in gast_dict.values())

    def get_taxonomy_id_dict(self):
        my_sql = "SELECT %s, %s FROM %s;" % ("taxonomy_id", "taxonomy", "taxonomy")
        res = self.my_conn.execute_fetch_select(my_sql)
        one_tax_id_dict = dict((y, int(x)) for x, y in res)
        self.tax_id_dict.update(one_tax_id_dict)

    def insert_whole_taxonomy(self):
        val_tmpl = "('%s')"
        all_taxonomy = set([val_tmpl % taxonomy.rstrip() for taxonomy in self.taxa_content])
        group_vals = self.utils.grouper(all_taxonomy, len(all_taxonomy))
        query_tmpl = make_sql_for_groups("taxonomy", "taxonomy")
        logger.debug("insert taxonomy:")
        self.my_conn.run_groups(group_vals, query_tmpl)

    def insert_split_taxonomy(self):
        self.parse_taxonomy()
        self.get_taxa_by_rank()
        self.make_uniqued_taxa_by_rank_dict()
        #         if (args.do_not_insert == False):
        self.insert_taxa()
        self.silva_taxonomy()
        #         if (args.do_not_insert == False):
        self.insert_silva_taxonomy()
        self.get_silva_taxonomy_ids()
        self.make_silva_taxonomy_id_per_taxonomy_dict()

    def parse_taxonomy(self):
        self.taxa_list_dict = {taxon_string: taxon_string.split(";") for taxon_string in self.taxa_content}
        self.taxa_list_w_empty_ranks_dict = {taxonomy: tax_list + [""] * (len(self.ranks) - len(tax_list)) for
                                             taxonomy, tax_list in self.taxa_list_dict.items()}

    def get_taxa_by_rank(self):
        self.taxa_by_rank = list(zip(*self.taxa_list_w_empty_ranks_dict.values()))

    def make_uniqued_taxa_by_rank_dict(self):
        for rank in self.ranks:
            rank_num = self.ranks.index(rank)
            uniqued_taxa_by_rank = set(self.taxa_by_rank[rank_num])
            try:
                self.uniqued_taxa_by_rank_dict[rank] = uniqued_taxa_by_rank
            except Exception:
                raise

    def insert_taxa(self):
        for rank, uniqued_taxa_by_rank in self.uniqued_taxa_by_rank_dict.items():
            insert_taxa_vals = '), ('.join(["'%s'" % key for key in uniqued_taxa_by_rank])

            shielded_rank_name = self.shield_rank_name(rank)
            self.my_conn.execute_insert(shielded_rank_name, shielded_rank_name, insert_taxa_vals)

    #             self.utils.print_array_w_title(rows_affected, "rows affected by self.my_conn.execute_insert(%s, %s, insert_taxa_vals)" % (rank, rank))

    @staticmethod
    def shield_rank_name(rank):
        return "`" + rank + "`"

    def get_all_rank_w_id(self):
        all_rank_w_id = self.my_conn.get_all_name_id("rank")

        try:
            klass_id = self.utils.find_val_in_nested_list(all_rank_w_id, "klass")
        except Exception:
            raise
        if not klass_id:
            klass_id = self.utils.find_val_in_nested_list(all_rank_w_id, "class")
        temp_l = list(all_rank_w_id)
        temp_l.append(("class", klass_id[0]))
        self.all_rank_w_id = dict((x, y) for x, y in set(temp_l))
        # (('domain', 78), ('family', 82), ('genus', 83), ('klass', 80), ('NA', 87), ('order', 81), ('phylum', 79), ('species', 84), ('strain', 85), ('superkingdom', 86))

    def make_uniqued_taxa_by_rank_w_id_dict(self):
        # self.utils.print_array_w_title(self.uniqued_taxa_by_rank_dict, "===\nself.uniqued_taxa_by_rank_dict from def silva_taxonomy")

        for rank, uniqued_taxa_by_rank in self.uniqued_taxa_by_rank_dict.items():
            shielded_rank_name = self.shield_rank_name(rank)
            taxa_names = ', '.join(["'%s'" % key for key in uniqued_taxa_by_rank])
            taxa_w_id = self.my_conn.get_all_name_id(shielded_rank_name, rank + "_id", shielded_rank_name,
                                                     'WHERE %s in (%s)' % (shielded_rank_name, taxa_names))
            self.uniqued_taxa_by_rank_w_id_dict[rank] = taxa_w_id

    def insert_silva_taxonomy(self):
        all_insert_st_vals = []

        for arr in self.taxa_list_w_empty_ranks_ids_dict.values():
            insert_dat_vals = ', '.join("'%s'" % key for key in arr)
            all_insert_st_vals.append('(%s)' % insert_dat_vals)

        fields = "domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id"
        query_tmpl = make_sql_for_groups("silva_taxonomy", fields)
        group_vals = self.utils.grouper(all_insert_st_vals, len(all_insert_st_vals))
        logger.debug("insert silva_taxonomy:")
        self.my_conn.run_groups(group_vals, query_tmpl)

    def silva_taxonomy(self):
        # silva_taxonomy (domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id)
        self.make_uniqued_taxa_by_rank_w_id_dict()

        for taxonomy, tax_list in self.taxa_list_w_empty_ranks_dict.items():
            # ['Bacteria', 'Proteobacteria', 'Deltaproteobacteria', 'Desulfobacterales', 'Nitrospinaceae', 'Nitrospina', '', '']
            silva_taxonomy_sublist = []
            for rank_num, taxon in enumerate(tax_list):
                rank = self.ranks[rank_num]
                taxon_id = int(self.utils.find_val_in_nested_list(self.uniqued_taxa_by_rank_w_id_dict[rank], taxon)[0])
                silva_taxonomy_sublist.append(taxon_id)
                # self.utils.print_array_w_title(silva_taxonomy_sublist, "===\nsilva_taxonomy_sublist from def silva_taxonomy: ")
            self.taxa_list_w_empty_ranks_ids_dict[taxonomy] = silva_taxonomy_sublist
            # self.utils.print_array_w_title(self.taxa_list_w_empty_ranks_ids_dict, "===\ntaxa_list_w_empty_ranks_ids_dict from def silva_taxonomy: ")

    def make_silva_taxonomy_rank_list_w_ids_dict(self):
        for taxonomy, silva_taxonomy_id_list in self.taxa_list_w_empty_ranks_ids_dict.items():
            rank_w_id_list = []
            for rank_num, taxon_id in enumerate(silva_taxonomy_id_list):
                rank = self.ranks[rank_num]
                t = (rank, taxon_id)
                rank_w_id_list.append(t)

            self.silva_taxonomy_rank_list_w_ids_dict[taxonomy] = rank_w_id_list
            # self.utils.print_array_w_title(self.silva_taxonomy_rank_list_w_ids_dict, "===\nsilva_taxonomy_rank_list_w_ids_dict from def make_silva_taxonomy_rank_list_w_ids_dict: ")
            """
            {'Bacteria;Proteobacteria;Alphaproteobacteria;Rhizobiales;Rhodobiaceae;Rhodobium': [('domain', 2), ('phylum', 2016066), ('klass', 2085666), ('order', 2252460), ('family', 2293035), ('genus', 2303053), ('species', 1), ('strain', 2148217)], ...
            """

    @staticmethod
    def make_rank_name_id_t_id_str(rank_w_id_list):
        a = ""
        for t in rank_w_id_list[:-1]:
            a += t[0] + "_id = " + str(t[1]) + " AND\n"
        a += rank_w_id_list[-1][0] + "_id = " + str(rank_w_id_list[-1][1]) + "\n"
        return a

    def make_silva_taxonomy_ids_dict(self, silva_taxonomy_ids):
        for ids in silva_taxonomy_ids:
            # ids[-1] = silva_taxonomy_id, the rest are ids for each rank
            self.silva_taxonomy_ids_dict[int(ids[-1])] = [int(my_id) for my_id in ids[0:-1]]
        # self.utils.print_array_w_title(self.silva_taxonomy_ids_dict, "===\nsilva_taxonomy_ids_dict from def get_silva_taxonomy_ids: ")
        # {2436595: [2, 2016066, 2085666, 2252460, 2293035, 2303053, 1, 2148217], 2436596: [...

    def get_silva_taxonomy_ids(self):
        self.make_silva_taxonomy_rank_list_w_ids_dict()

        # sql_part = ""
        # start2 = time.time()
        sql_part_list = ["%s" % self.make_rank_name_id_t_id_str(rank_w_id_list) for rank_w_id_list in
                         self.silva_taxonomy_rank_list_w_ids_dict.values()]
        sql_inner_part = "  UNION ALL  "

        field_names = "domain_id, phylum_id, klass_id, order_id, family_id, genus_id, species_id, strain_id"
        table_name = "silva_taxonomy"
        id_name = "silva_taxonomy_id"
        # where_part = "WHERE " + sql_part
        # silva_taxonomy_ids = self.my_conn.get_all_name_id(table_name, "", field_names, where_part)
        # elapsed2 = (time.time() - start2)
        # print("QQQ2 sql_part2 time: %s s" % elapsed2)

        my_sql_parts = []
        for l in sql_part_list:
            where_part = "".join(l)
            my_sql_part = """(SELECT %s, %s FROM %s WHERE %s)""" % (field_names, id_name, table_name, where_part)
            my_sql_parts.append(my_sql_part)
        #         self.utils.print_both(("my_sql from get_all_name_id = %s") % my_sql)
        my_sql = sql_inner_part.join(my_sql_parts)
        silva_taxonomy_ids = self.my_conn.execute_fetch_select(my_sql)
        #
        # elapsed4 = (time.time() - start2)
        # print("QQQ2 sql_part4 time: %s s" % elapsed4)

        """
        ((2436595L, 2L, 2016066L, 2085666L, 2252460L, 2293035L, 2303053L, 1L, 2148217L), ...
        """
        self.make_silva_taxonomy_ids_dict(silva_taxonomy_ids)

    def make_silva_taxonomy_id_per_taxonomy_dict(self):
        for silva_taxonomy_id, st_id_list1 in self.silva_taxonomy_ids_dict.items():
            taxon_string = self.utils.find_key_by_value_in_dict(self.taxa_list_w_empty_ranks_ids_dict.items(),
                                                                st_id_list1)
            self.silva_taxonomy_id_per_taxonomy_dict[taxon_string[0]] = silva_taxonomy_id
        # self.utils.print_array_w_title(self.silva_taxonomy_id_per_taxonomy_dict, "silva_taxonomy_id_per_taxonomy_dict from silva_taxonomy_info_per_seq = ")

class Seq:
    """
    get sequence ids
    get their amount
    upload by chunks (in upload class):
             mysql_utils.execute_no_fetch_w_info(q_update_table_look_up_tax % (counter, chunk_size))

    """
    def __init__(self, project_id):
        self.utils = util.Utils()
        pdr_info_table_name = table_names["sequence_pdr_info_table_name"]
        self.pdr_info_table_data = self.get_pdr_info_table_data(pdr_info_table_name)


        self.sequence_table_data = self.get_sequence_table_data()

        pdr_id_seq_id = self.get_pdr_info()

        self.pdr_id_list = [x[0] for x in pdr_id_seq_id[0]]
        self.pdr_id_list_str = utils.make_quoted_str(self.pdr_id_list)

        self.sequence_id_list = [x[1] for x in pdr_id_seq_id[0]]
        self.sequence_id_str = utils.make_quoted_str(self.sequence_id_list)


        # self.pdr_uniq_index = utils.get_uniq_index_columns(self.sequence_name, db_in)

    def get_pdr_info_table_data(self, table_name):
        pdr_info_table_data = defaultdict()

        pdr_info_table_data["table_name"] = table_name
        pdr_info_table_data["id_name"] = table_name + "_id"
        pdr_info_table_data["fields"] = mysql_utils_in.get_field_names(table_name)
        pdr_info_table_data["fields_str"] = ", ".join([x[0] for x in pdr_info_table_data["fields"][0]])
        pdr_info_table_data["unique_fields"] = mysql_utils_in.get_uniq_index_columns(db_in, table_name)
        pdr_info_table_data["unique_fields_str"] = ", ".join(pdr_info_table_data["unique_fields"])
        return pdr_info_table_data

    def get_sequence_table_data(self):

        self.sequence_name = table_names["sequence_table_name"]
        self.sequence_id_name = self.sequence_name + "_id"

        self.seq_fields = mysql_utils_in.get_field_names(self.sequence_name)
        self.seq_fields_str = ", ".join([x[0] for x in self.seq_fields[0]])

        self.sequence_uniq_index = mysql_utils_in.get_uniq_index_columns(db_in, self.sequence_name)
        self.sequence_uniq_index_str = ", ".join(self.sequence_uniq_index)


    def get_pdr_info(self):
        # SELECT sequence_pdr_info_id, sequence_id
        all_seq_ids_sql = """SELECT DISTINCT %s, %s FROM %s
                             WHERE dataset_id IN (%s)
                             AND run_info_ill_id IN (%s)""" % (self.pdr_info_table_data["id_name"], self.sequence_id_name, self.pdr_info_table_data["table_name"],
                                                             dataset_obj.dataset_ids_string,
                                                             run_info_obj.used_run_info_id_str)

        rows = mysql_utils_in.execute_fetch_select(all_seq_ids_sql)
        return rows

    # def insert_seq(self, sequences):
    #     seq_field = self.table_names["sequence_field_name"]
    #     val_tmpl = " COMPRESS('%s') AS %s "
    #     all_seq = set([val_tmpl % (seq, seq_field) for seq in sequences])
    #     # group_vals = self.utils.grouper(all_seq, 10)
    #     group_vals = self.utils.grouper(all_seq, len(all_seq))
    #     # query_tmpl = make_sql_for_groups(self.table_names["sequence_table_name"],
    #     #                                  self.table_names["sequence_field_name"])
    #     logger.debug("insert sequences:")
    #
    #     unique_fields = ['sequence_comp']
    #     query_tmpl1 = make_sql_for_groups1(self.table_names["sequence_table_name"],
    #                                         self.table_names["sequence_field_name"], unique_fields)
    #     # print("q2a: sequences")
    #     # print(query_tmpl1)
    #     # self.my_conn.run_groups(group_vals, query_tmpl)
    #     # self.my_conn.run_groups(group_vals, query_tmpl1, ' UNION ALL SELECT ')
    #     join_xpr = ' UNION ALL SELECT '
    #     self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)
    #
    # def get_seq_id_dict(self, sequences):
    #     # TODO: ONCE IN CLASS
    #
    #     sequence_field_name = self.table_names["sequence_field_name"]
    #     sequence_table_name = self.table_names["sequence_table_name"]
    #     id_name = self.table_names["sequence_table_name"] + "_id"
    #     query_tmpl = """SELECT %s, uncompress(%s) FROM %s WHERE %s in (COMPRESS(%s))"""
    #     val_tmpl = "'%s'"
    #     try:
    #         group_seq = self.utils.grouper(sequences, len(sequences))
    #         for group in group_seq:
    #             # key for conv.escape_string(key) in group if key is not None
    #             seq_part = '), COMPRESS('.join([val_tmpl % key for key in group if key is not None])
    #             my_sql = query_tmpl % (id_name, sequence_field_name, sequence_table_name, sequence_field_name, seq_part)
    #             res = self.my_conn.execute_fetch_select(my_sql)
    #             one_seq_id_dict = dict((y.decode().upper(), int(x)) for x, y in res)
    #
    #             self.seq_id_dict.update(one_seq_id_dict)
    #     except Exception:
    #         if len(sequences) == 0:
    #             self.utils.print_both(
    #                 "ERROR: There are no sequences, please check if there are correct fasta files in the directory %s" % self.fasta_dir)
    #         raise
    #
    # def prepare_pdr_info_values(self, run_info_ill_id, all_dataset_run_info_dict, db_name, current_db_host_name):
    #
    #     all_insert_pdr_info_vals = []
    #
    #     for fasta_id, seq in self.fasta_dict.items():
    #         if not run_info_ill_id:
    #             err_msg = "ERROR: There is no run info yet, please check if it's uploaded to %s" % db_name
    #             self.utils.print_both(err_msg)
    #             self.seq_errors.append(err_msg)
    #             break
    #         try:
    #             sequence_id = self.seq_id_dict[seq]
    #
    #             seq_count = int(fasta_id.split('|')[-1].split(':')[-1])
    #             vals = ""
    #             sequence_id_field = self.table_names["sequence_table_name"] + "_id"
    #
    #             if current_db_host_name == "vamps2":
    #                 try:
    #                     dataset_id = all_dataset_run_info_dict[run_info_ill_id]
    #                     # vals = "(%s, %s, %s, %s)" % (dataset_id, sequence_id, seq_count, C.classifier_id)
    #                     vals = "%s AS dataset_id, %s AS run_info_ill_id, %s AS %s, %s AS seq_count, %s AS classifier_id" % (dataset_id, run_info_ill_id, sequence_id, sequence_id_field, seq_count, C.classifier_id)
    #                 except KeyError:
    #                     logger.error("No such run info, please check a file name and the csv file")
    #                     logger.debug("From prepare_pdr_info_values, all_dataset_run_info_dict: %s" % all_dataset_run_info_dict)
    #
    #             elif current_db_host_name == "env454":
    #                 # vals = "(%s, %s, %s)" % (run_info_ill_id, sequence_id, seq_count)
    #                 vals = "%s AS run_info_ill_id, %s AS %s, %s AS seq_count" % (run_info_ill_id, sequence_id, sequence_id_field, seq_count)
    #
    #             all_insert_pdr_info_vals.append(vals)
    #             fasta_id = ""
    #             seq = ""
    #             seq_count = 0
    #             sequence_id = ""
    #         except Exception:
    #             logger.error("FFF0 fasta_id %s" % fasta_id)
    #             logger.error("SSS0 seq %s" % seq)
    #             raise
    #     return all_insert_pdr_info_vals
    #
    # def get_seq_id_w_silva_taxonomy_info_per_seq_id(self):
    #     logger.debug("get_seq_id_w_silva_taxonomy_info_per_seq_id:")
    #     sequence_ids_strs = [str(i) for i in self.seq_id_dict.values()]
    #     field_names = "sequence_id, silva_taxonomy_info_per_seq_id"
    #     where_part = 'WHERE sequence_id in (%s)'
    #     query_tmpl = """SELECT %s FROM %s %s""" % (field_names, "silva_taxonomy_info_per_seq", where_part)
    #     group_vals = self.utils.grouper(sequence_ids_strs,
    #                                     len(sequence_ids_strs))
    #     for group in group_vals:
    #         val_part = ", ".join([key for key in group if key is not None])
    #         my_sql = query_tmpl % val_part
    #         self.seq_id_w_silva_taxonomy_info_per_seq_id.extend(self.my_conn.execute_fetch_select(my_sql))
    #
    # def insert_sequence_uniq_info2(self):
    #     self.get_seq_id_w_silva_taxonomy_info_per_seq_id()
    #     fields = "sequence_id, silva_taxonomy_info_per_seq_id"
    #     # sequence_uniq_info_values = ["(%s,  %s)" % (i1, i2) for i1, i2 in self.seq_id_w_silva_taxonomy_info_per_seq_id]
    #     sequence_uniq_info_values = ["%s AS sequence_id, %s AS get_seq_id_w_silva_taxonomy_info_per_seq_id" % (i1, i2) for i1, i2 in self.seq_id_w_silva_taxonomy_info_per_seq_id]
    #     # query_tmpl = make_sql_for_groups("sequence_uniq_info", fields)
    #     group_vals = self.utils.grouper(sequence_uniq_info_values, len(sequence_uniq_info_values))
    #     logger.debug("insert sequence_uniq_info_ill:")
    #     # print("q3: insert_sequence_uniq_info2")
    #     # print(query_tmpl)
    #     unique_fields = ['sequence_id']
    #     query_tmpl1 = make_sql_for_groups1("sequence_uniq_info", fields, unique_fields)
    #     # print("q3a: insert_sequence_uniq_info2")
    #     # print(query_tmpl1)
    #     join_xpr = ' UNION ALL SELECT '
    #
    #     self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)
    #
    # def insert_sequence_uniq_info_ill(self, gast_dict):
    #     all_insert_sequence_uniq_info_ill_vals = []
    #     for fasta_id, gast in gast_dict.items():
    #         (taxonomy, distance, rank, refssu_count, vote, minrank, taxa_counts, max_pcts, na_pcts, refhvr_ids) = gast
    #         seq = self.fasta_dict[fasta_id]
    #         sequence_id = self.seq_id_dict[seq]
    #         rank_id = self.taxonomy.all_rank_w_id[rank]
    #         if taxonomy in self.taxonomy.tax_id_dict:
    #             taxonomy_id = self.taxonomy.tax_id_dict[taxonomy]
    #             vals = """(%s,  %s,  '%s',  '%s',  %s,  '%s')
    #                     """ % (sequence_id, taxonomy_id, distance, refssu_count, rank_id, refhvr_ids.rstrip())
    #             all_insert_sequence_uniq_info_ill_vals.append(vals)
    #     group_vals = self.utils.grouper(all_insert_sequence_uniq_info_ill_vals,
    #                                     len(all_insert_sequence_uniq_info_ill_vals))
    #
    #     fields = "%s_id, taxonomy_id, gast_distance, refssu_count, rank_id, refhvr_ids" % (
    #         self.table_names["sequence_table_name"])
    #     query_tmpl = make_sql_for_groups("sequence_uniq_info_ill", fields)
    #
    #     logger.debug("insert sequence_uniq_info_ill:")
    #     self.my_conn.run_groups(group_vals, query_tmpl)


class Constant:
    def __init__(self):

        self.chunk_size = 1000
        self.full_short_ordered_tables = ["classifier", "dna_region", "domain", "env_package", "illumina_adaptor", "illumina_index", "illumina_run_key", "illumina_adaptor_ref", "primer_suite", "rank", "run", "run_key", "sequencing_platform", "target_gene", "primer_suite"
                                         , "user", "project", "dataset", "run_info_ill", "required_metadata_info", "custom_metadata_fields"]
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

    upl.insert_metadata_info()
    sequence_obj = Seq(project_obj.project_id)
    upl.insert_sequence()
    upl.insert_pdr_info()

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



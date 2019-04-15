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


def make_sql_for_groups(table_name, fields_str):
    field_list = fields_str.split(",")
    my_sql_1 = "INSERT IGNORE INTO %s (%s) VALUES " % (table_name, fields_str)
    my_sql_2 = " ON DUPLICATE KEY UPDATE "
    for field_name in field_list[:-1]:
        my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
    my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (field_list[-1].strip(), field_list[-1].strip())
    return my_sql_1 + " %s " + my_sql_2


def make_sql_for_groups1(table_name, fields_str, unique_fields):
    field_list = fields_str.split(",")
    my_sql_1 = """INSERT IGNORE INTO %s (%s) SELECT i.* FROM """ % (table_name, fields_str)
    unique_1 = ['t1.%s is null' % x for x in unique_fields]
    my_sql_m1 = " (SELECT "
    my_sql_m2 = """) i
        LEFT JOIN
        %s t1 using(%s)
        WHERE
        %s
        """ % (table_name, ', '.join(unique_fields), ' AND '.join(unique_1))

    # UNION ALL SELECT %s AS %s

    my_sql_2 = " ON DUPLICATE KEY UPDATE "
    for field_name in field_list[:-1]:
        my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
    my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (field_list[-1].strip(), field_list[-1].strip())
    return my_sql_1 + my_sql_m1 + " %s " + my_sql_m2 + my_sql_2


class MyConnection:
    """
    Connection to env454
    Takes parameters from ~/.my.cnf, default host = "vampsdev", db="test"
    if different use my_conn = MyConnection(host, db)
    """

    def __init__(self, host = "bpcweb7", db = "test"):
        # , read_default_file=os.path.expanduser("~/.my.cnf"), port = 3306

        self.utils = util.Utils()
        self.conn = None
        self.cursor = None
        self.cursorD = None
        self.lastrowid = None

        try:
            self.utils.print_both("=" * 40)
            self.utils.print_both("host = " + str(host) + ", db = " + str(db))
            self.utils.print_both("=" * 40)
            read_default_file = os.path.expanduser("~/.my.cnf")
            port_env = 3306

            if self.utils.is_local():
                host = "127.0.0.1"
                read_default_file = "~/.my.cnf_local"
            self.conn = mysql.connect(host = host, db = db, read_default_file = read_default_file, port = port_env)
            self.cursor = self.conn.cursor()
            self.cursorD = self.conn.cursor(mysql.cursors.DictCursor)
        except (AttributeError, mysql.OperationalError):
            self.conn = mysql.connect(host = host, db = db, read_default_file = read_default_file, port = port_env)
            self.cursor = self.conn.cursor()
        except mysql.Error:
            e = sys.exc_info()[1]
            self.utils.print_both("Error %d: %s" % (e.args[0], e.args[1]))
            raise

    @staticmethod
    def connect(host, db, read_default_file, port_env):
        return mysql.connect(host = host, db = db, read_default_file = read_default_file, port = port_env)

    def execute_fetch_select(self, sql):
        if self.cursor:
            try:
                # sql = self.conn.escape(sql)
                self.cursor.execute(sql)
                return self.cursor.fetchall()
            except Exception:
                self.utils.print_both("ERROR: query = %s" % sql)
                raise

    """
    for msg in cur.fetchwarnings():
    print("Warning: {msg}".format(msg=msg[2]))

    """

    def show_warnings(self, sql):
        wrngs = self.conn.show_warnings()
        if wrngs:
            short_sql = sql[0:1000].split(" ")
            short_sql = " ".join(short_sql[0:12]) + "..."
            logger.debug("Show_warnings: ")
            logger.debug(short_sql)
            logger.debug(wrngs)

    def execute_no_fetch(self, sql):
        if self.cursor:
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except mysql.IntegrityError:
                logger.error(sql[1:1000])
                raise
            self.show_warnings(sql)
            try:
                return self.cursor._result.message
            except Exception:
                try:
                    return self.cursor._info
                except Exception:
                    return self.cursor.rowcount

    def execute_insert(self, table_name, field_name, val_list, ignore = "IGNORE"):
        sql = "INSERT %s INTO %s (%s) VALUES (%s) " % (ignore, table_name, field_name, val_list)
        sql = sql + " ON DUPLICATE KEY UPDATE %s = VALUES(%s);" % (field_name, field_name)
        try:
            if self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
                self.show_warnings(sql)
                return (self.cursor.rowcount, self.cursor.lastrowid)
        except Exception:
            self.utils.print_both("ERROR: query = %s" % sql)
            raise

    def get_all_name_id(self, table_name, id_name = "", field_name = "", where_part = ""):
        if field_name == "":
            field_name = table_name
        if id_name == "":
            id_name = table_name + '_id'
        my_sql = """SELECT %s, %s FROM %s %s""" % (field_name, id_name, table_name, where_part)
        #         self.utils.print_both(("my_sql from get_all_name_id = %s") % my_sql)
        res = self.execute_fetch_select(my_sql)

        if res:
            return res

    def run_groups(self, group_vals, query_tmpl, join_xpr = ', '):
        for group in group_vals:
            val_part = join_xpr.join([key for key in group if key is not None])
            my_sql = query_tmpl % val_part
            # if "sequence_uniq_info_ill" in my_sql:
                # print("MMM my_sql = ")
                # print(my_sql)
                # logger.debug("MMM my_sql = %s" % my_sql)
            insert_info = self.execute_no_fetch(my_sql)
            # logger.debug("insert info = %s" % insert_info)

    # def make_sql_w_duplicate(self, table_name, fields_str, unique_key_fields_arr):
    #     my_sql_1 = "INSERT IGNORE INTO %s (%s) VALUES " % (table_name, fields_str)
    #     my_sql_2 =  " ON DUPLICATE KEY UPDATE "
    #     for field_name in unique_key_fields_arr[:-1]:
    #         my_sql_2 = my_sql_2 + " %s = VALUES(%s), " % (field_name.strip(), field_name.strip())
    #     my_sql_2 = my_sql_2 + "  %s = VALUES(%s);" % (unique_key_fields_arr[-1].strip(), unique_key_fields_arr[-1].strip())
    #     return my_sql_1 + " %s " + my_sql_2

    def insert_bulk_data(self, key, values):
        query_tmpl = "INSERT IGNORE INTO %s (%s) VALUES (%s)"
        val_tmpl = "'%s'"
        my_sql = query_tmpl % (key, key, '), ('.join([val_tmpl % v for v in values]))
        my_sql = my_sql + " ON DUPLICATE KEY UPDATE %s = VALUES(%s);" % (key, key)

        self.execute_no_fetch(my_sql)

class dbUpload:
    """db upload methods"""
    Name = "dbUpload"
    """
    TODO: add tests and test case
    TODO: change hardcoded values to args:
        self.sequence_table_name = "sequence_ill",
        self.sequence_field_name = "sequence_comp"
    TODO: generalize all bulk uploads and all inserts? to not copy and paste
    TODO: add refssu_id
    TODO: change csv validaton for new fields
    Order:
        # put_run_info
        # insert_seq()
        # insert_pdr_info()
        # gast
        # insert_taxonomy()
        # insert_sequence_uniq_info_ill()

    """

    def __init__(self, runobj = None, db_name = None):

        self.db_name = db_name
        self.utils = util.Utils()
        self.runobj = runobj
        self.samples_dict = self.convert_samples_to_dict()
        self.rundate = self.runobj.run
        self.use_cluster = 1
        self.unique_fasta_files = []
        self.all_errors = []  # (+seq_errors)
        self.metadata_info_all = defaultdict(dict)

        if self.runobj.vamps_user_upload:
            site = self.runobj.site
            dir_prefix = self.runobj.user + '_' + self.runobj.run
        else:
            site = ''
            dir_prefix = self.runobj.run
        if self.runobj.lane_name:
            lane_name = self.runobj.lane_name
        else:
            lane_name = ''

        self.dirs = Dirs(self.runobj.vamps_user_upload, dir_prefix, self.runobj.platform, lane_name = lane_name,
                         site = site)

        self.analysis_dir = self.dirs.check_dir(self.dirs.analysis_dir)
        self.fasta_dir = self.dirs.check_dir(self.dirs.reads_overlap_dir)
        self.gast_dir = self.dirs.check_dir(self.dirs.gast_dir)

        self.filenames = []
        # logger.error("self.utils.is_local() LLL1 db upload")
        # logger.error(self.utils.is_local())
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

        self.get_conn()

        find_dict = {'host': self.runobj.database_host, 'db': self.runobj.database_name}
        self.db_marker = self.utils.find_in_nested_dict(C.db_cnf, find_dict)[0]
        try:
            self.table_names = self.table_names_dict[self.db_marker]
        except Exception:
            raise

        self.taxonomy = Taxonomy(self.my_conn)
        self.seq = Seq(self.taxonomy, self.table_names, self.fasta_dir)

        self.gast_dict = {}
        self.silva_taxonomy_info_per_seq_list = []

        self.unique_file_counts = self.dirs.unique_file_counts
        self.dirs.delete_file(self.unique_file_counts)
        self.run_id = None
        self.nonchimeric_suffix = "." + C.nonchimeric_suffix  # ".nonchimeric.fa"
        self.fa_unique_suffix = ".fa." + C.unique_suffix  # .fa.unique
        self.v6_unique_suffix = "MERGED_V6_PRIMERS_REMOVED." + C.unique_suffix
        self.suff_list = [self.nonchimeric_suffix, self.fa_unique_suffix, self.v6_unique_suffix]
        self.suffix_used = ""
        # self.all_dataset_ids = self.my_conn.get_all_name_id("dataset")
        self.used_project_ids = defaultdict(list)
        self.used_project_names = ""
        self.filenames = self.get_fasta_file_names()
        self.fa_files_cnts_in_dir = 0
        self.fa_files_cnts_in_csv = 0
        self.equal_amnt_files_txt = ""
        self.equal_amnt_files = self.check_files_csv()
        if self.db_marker == "vamps2":
            if not self.equal_amnt_files:
                self.equal_amnt_files_txt = """WARNING: There is different amount of files (%s vs. %s) in the csv and in %s
                """ % (self.fa_files_cnts_in_csv, self.fa_files_cnts_in_dir,
                       self.fasta_dir)

                logger.debug("WARNING: There is different amount of files in the csv and in %s" % self.fasta_dir)
            self.put_run_info()
            self.put_required_metadata()
        self.all_project_dataset_ids_dict = self.get_project_id_per_dataset_id()
        self.all_dataset_run_info_dict = self.get_dataset_per_run_info_id()

    def get_conn(self):

        if self.utils.is_local():
            is_local = "local"
        else:
            is_local = "production"

        try:
            host = self.runobj.database_host
            db = self.runobj.database_name
        except Exception:
            self.db_marker = "env454"
            host = C.db_cnf[self.db_marker][is_local]["host"]
            db = C.db_cnf[self.db_marker][is_local]["db"]

        self.my_conn = MyConnection(host, db)

    def reset_auto_increment(self):
        if self.db_marker == "vamps2":
            auto_increment_queries = ["ALTER TABLE dataset AUTO_INCREMENT = 1;", "ALTER TABLE project AUTO_INCREMENT = 1;", "ALTER TABLE rdp_taxonomy_info_per_seq AUTO_INCREMENT = 1;", "ALTER TABLE run_info_ill AUTO_INCREMENT = 1;", "ALTER TABLE silva_taxonomy AUTO_INCREMENT = 1;"]
        #     UNION: "ALTER TABLE sequence_pdr_info AUTO_INCREMENT = 1;", "ALTER TABLE sequence_uniq_info AUTO_INCREMENT = 1;", "ALTER TABLE sequence AUTO_INCREMENT = 1;", "ALTER TABLE silva_taxonomy_info_per_seq AUTO_INCREMENT = 1;",

        else:
            auto_increment_queries = ["ALTER TABLE sequence_pdr_info_ill AUTO_INCREMENT = 1;", "ALTER TABLE sequence_uniq_info_ill AUTO_INCREMENT = 1;", "ALTER TABLE sequence_ill AUTO_INCREMENT = 1;", "ALTER TABLE run_info_ill AUTO_INCREMENT = 1;", "ALTER TABLE dataset AUTO_INCREMENT = 1;", "ALTER TABLE project AUTO_INCREMENT = 1;"]

        for q in auto_increment_queries:
            self.my_conn.execute_fetch_select(q)

    def convert_samples_to_dict(self):
        dd = defaultdict(dict)
        for k, v in self.runobj.samples.items():
            dd[k] = dict(zip(v.__dict__.keys(), v.__dict__.values()))
        return dd

    def check_files_csv(self):
        try:
            self.fa_files_cnts_in_dir = len(self.filenames)
            self.fa_files_cnts_in_csv = len(self.runobj.run_keys)
            return self.fa_files_cnts_in_dir == self.fa_files_cnts_in_csv
        except Exception:
            logger.error("There is a problem with files in the csv and/or in %s" % self.fasta_dir)
            raise

    # TODO: Do once loop over all used run_info_ill_id in self.all_project_dataset_ids_dict
    def collect_project_ids(self, run_info_ill_id):
        # print("EEE self.all_dataset_run_info_dict")
        # print(self.all_dataset_run_info_dict)
        # print("RRR run_info_ill_id")
        # print(run_info_ill_id)
        try:
            dataset_id = self.all_dataset_run_info_dict[run_info_ill_id]
            self.used_project_ids[dataset_id] = self.all_project_dataset_ids_dict[dataset_id]
        except KeyError:
            logger.error("No such run info, please check a file name and the csv file")

    def get_projects_and_ids(self):
        if len(self.used_project_names) <= 0:
            self.used_project_names = list(set([content_row.project for key, content_row in self.runobj.samples.items()]))
        where_part = " WHERE project in ('%s')" % ", ".join(self.used_project_names)
        res = self.my_conn.get_all_name_id("project", "", "", where_part)
        try:
            projects, pr_ids = zip(*res)
            pr_ids_str = (str(w) for w in pr_ids)
            project_and_ids = "projects: %s; ids: %s" % (", ".join(projects), ", ".join(pr_ids_str))
            return project_and_ids
        except TypeError:
            return ""

    def get_fasta_file_names(self):
        files_names = self.dirs.get_all_files(self.fasta_dir)
        self.unique_fasta_files = [f for f in files_names.keys() if f.endswith(tuple(self.suff_list))]
        # needs return because how it's called from pipelineprocesor
        return self.unique_fasta_files

    @staticmethod
    def send_message(recipient, subject, body):
        try:
            process = Popen(['mail', '-s', subject, recipient], stdin = PIPE)
            process.communicate(body.encode())
        except Exception:
            error = sys.exc_info()[1]
            logger.error(error)

    def get_run_info_ill_id(self, filename_base):

        my_sql = """SELECT run_info_ill_id FROM run_info_ill
                    JOIN run using(run_id)
                    WHERE file_prefix = '%s'
                    and run = '%s';
        """ % (filename_base, self.rundate)

        res = self.my_conn.execute_fetch_select(my_sql)
        if res:
            return int(res[0][0])

    def get_project_id_per_dataset_id(self):
        env454_where_part = ""
        if self.db_marker == "env454":
            env454_where_part = """WHERE file_prefix in ('%s')""" % ("', '".join(self.runobj.run_keys))
        all_project_id_per_dataset_id_sql = """SELECT dataset_id, project_id FROM %s %s
                                            """ % (self.table_names["connect_pr_dat_table"], env454_where_part)

        res = self.my_conn.execute_fetch_select(all_project_id_per_dataset_id_sql)
        return dict([(r, d) for r, d in res])

    def get_dataset_per_run_info_id(self):
        all_dataset_run_info_sql = "SELECT run_info_ill_id, dataset_id FROM run_info_ill"
        res = self.my_conn.execute_fetch_select(all_dataset_run_info_sql)
        return dict([(r, d) for r, d in res])

    def get_id(self, table_name, value, and_part = ""):
        id_name = table_name + '_id'
        my_sql = """SELECT %s FROM %s WHERE %s = '%s' %s;""" % (id_name, table_name, table_name, value, and_part)
        res = self.my_conn.execute_fetch_select(my_sql)
        if res:
            return int(res[0][0])

    def make_gast_files_dict(self):
        return self.dirs.get_all_files(self.gast_dir, "gast")

    def gast_filename(self, filename):
        # todo: if filename in make_gast_files_dict, use it full path
        gast_file_names = self.make_gast_files_dict()

        for gast_file_name_path, tpls in gast_file_names.items():
            if any(t.endswith(filename) for t in tpls):
                return gast_file_name_path

    def get_gast_result(self, filename):
        gast_file_name = self.gast_filename(filename)
        self.utils.print_both("current gast_file_name = %s." % gast_file_name)

        try:
            with open(gast_file_name) as fd:
                gast_content = fd.readlines()
            self.gast_dict = dict([(l.split("\t")[0], l.split("\t")[1:]) for l in gast_content[1:]])
        #             gast_dict.remove([k for k in gast_dict if k[0] == 'taxonomy'][0])
        except IOError:
            e = sys.exc_info()[1]
            #            print(dir(e))
            # ['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__getslice__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', 'args', 'errno', 'filename', 'message', 'strerror']
            #            print("errno = %s" % e.errno)
            logger.debug("errno = %s" % e.errno)
            if e.errno == 2:
                # suppress "No such file or directory" error
                pass
        except TypeError:
            error = sys.exc_info()[1]
            err_msg = "Check if there is a gast file under %s for %s. \nSystem error: %s" % (
                self.gast_dir, filename, error)
            self.utils.print_both(err_msg)
            self.all_errors.append(err_msg)
            pass

    def put_run_info(self):

        run_keys = list(set([run_key.split('_')[1] for run_key in self.runobj.run_keys]))
        self.my_conn.insert_bulk_data('run_key', run_keys)
        dna_regions = list(set([self.runobj.samples[key].dna_region for key in self.runobj.samples]))
        self.my_conn.insert_bulk_data('dna_region', dna_regions)
        self.insert_rundate()
        self.used_project_names = self.insert_project()
        for key, value in self.runobj.samples.items():
            self.insert_dataset(value)
        self.get_all_metadata_info()
        self.insert_run_info()

    # def get_contact_v_info(self):
    #     """
    #     TODO: get info from Hilary? from vamps?
    #     """
    #     pass

    def insert_test_contact(self):
        my_sql = '''INSERT IGNORE INTO contact (contact, email, institution, vamps_name, first_name, last_name)
                VALUES ("guest user", "guest@guest.com", "guest institution", "guest", "guest", "user");'''
        return self.my_conn.execute_no_fetch(my_sql)

    def get_contact_id(self, data_owner):
        my_sql = """SELECT %s_id FROM %s WHERE %s = '%s';""" % (
            self.table_names["contact"], self.table_names["contact"], self.table_names["username"], data_owner)

        res = self.my_conn.execute_fetch_select(my_sql)
        if res:
            return int(res[0][0])

    def insert_rundate(self):
        my_sql = """INSERT IGNORE INTO run (run, run_prefix, platform) VALUES
            ('%s', 'illumin', '%s');""" % (self.rundate, self.runobj.platform)
        return self.my_conn.execute_no_fetch(my_sql)

    # Needs refactoring!
    def insert_project(self):
        all_vals = set()
        all_templ = set()
        all_project_names = set()
        vals = ""
        for key, content_row in self.runobj.samples.items():
            contact_id = self.get_contact_id(content_row.data_owner)
            if not contact_id:
                err_msg = """ERROR: There is no such contact info on %s,
                    please check if the user %s has an account on VAMPS""" % (self.db_marker, content_row.data_owner)
                self.all_errors.append(err_msg)
                logger.error(err_msg)
                sys.exit(err_msg)

            all_project_names.add(content_row.project)
            fields = "project, title, project_description, rev_project_name, funding"
            if self.db_marker == "vamps2":
                is_permanent = 1
                fields += ", owner_user_id, updated_at, permanent"
                vals = """('%s', '%s', '%s', reverse('%s'), '%s', '%s', NOW(), %s)
                """ % (
                    content_row.project, content_row.project_title, content_row.project_description, content_row.project,
                    content_row.funding, contact_id, is_permanent)

            elif self.db_marker == "env454":
                fields += ", env_sample_source_id, contact_id"
                vals = """('%s', '%s', '%s', reverse('%s'), '%s', '%s', %s)
                    """ % (
                    content_row.project, content_row.project_title, content_row.project_description,
                    content_row.project,
                    content_row.funding, content_row.env_sample_source_id, contact_id)
                #         TODO: change! what if we have more self.db_marker?

            all_vals.add(vals)
            all_templ.add(make_sql_for_groups("project", fields))

        # todo: use in used_projects and project_ids
        logger.debug("projects: %s" % all_project_names)

        if len(all_templ) > 1:
            err_msg = "WHY many templates? %s" % all_templ
            self.all_errors.append(err_msg)
            logger.error(err_msg)
            sys.exit(err_msg)

        for v in set(all_vals):
            query_tmpl = list(all_templ)[0]
            self.my_conn.execute_no_fetch(query_tmpl % v)

        return list(all_project_names)

    def insert_dataset(self, content_row):
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
        return self.my_conn.execute_no_fetch(my_sql)

    def convert_env_sample_source(self, env_sample_source):
        if (env_sample_source == "miscellaneous_natural_or_artificial_environment"):
            env_sample_source_replaced = "miscellaneous"
        else:
            env_sample_source_replaced = env_sample_source.replace("_", " ")
        return env_sample_source_replaced

    def get_all_metadata_info(self):
        # get_all_metadata_info todo: get all repeated first into dicts. insert_size, lane, overlap, platform, primer_suite_id, read_length, run_id, seq_operator, domain_id, sequencing_platform_id, target_gene_id, updated_at
        missing_terms = []
        unknown_term_id = []
        if self.db_marker == "vamps2":
            missing_terms = ["env_biome_id", "env_feature_id", "env_material_id", "geo_loc_name_id"]
            # and ontology_id = 1
            my_sql = "SELECT %s FROM %s WHERE %s = '%s';" % ("term_id", "term", "term_name", "unknown")
            # logger.debug("my_sql from get_all_metadata_info: %s" % my_sql)
            unknown_term_id = self.my_conn.execute_fetch_select(my_sql)

        domain_by_adj = dict(zip(C.domain_adj, C.domains))
        domain_by_adj['Fungal'] = 'Eukarya'
        # ,  'Fungal'
        for key, d_val in self.samples_dict.items():
            metadata_info = {k: v for k, v in d_val.items()}

            # add ids
            content_row = self.runobj.samples[key]
            metadata_info['contact_id'] = self.get_contact_id(content_row.data_owner)
            if not metadata_info['contact_id']:
                err_msg = """ERROR: There is no such contact info on %s,
                    please check if the user %s has an account on VAMPS""" % (self.db_marker, content_row.data_owner)
                self.all_errors.append(err_msg)
                logger.error(err_msg)
                sys.exit(err_msg)

            metadata_info['dataset_id'] = self.get_id('dataset', content_row.dataset)
            metadata_info['dna_region_id'] = self.get_id('dna_region', content_row.dna_region)
            metadata_info[
                'file_prefix'] = content_row.barcode_index + "_" + content_row.run_key + "_" + content_row.lane  # use self.runobj.idx_keys?
            metadata_info['illumina_index_id'] = self.get_id('illumina_index', content_row.barcode_index)
            if '_' in metadata_info['overlap']:
                metadata_info['overlap'] = metadata_info['overlap'].split("_")[1]  # hs_compete, ms_partial
            metadata_info['platform'] = self.runobj.platform
            metadata_info['primer_suite_id'] = self.get_id('primer_suite', content_row.primer_suite)
            metadata_info['project_id'] = self.get_id('project', content_row.project)
            metadata_info['run'] = self.rundate
            metadata_info['run_id'] = self.run_id
            if not self.run_id:
                metadata_info['run_id'] = self.get_id('run', self.rundate)
            metadata_info['run_key_id'] = self.get_id('run_key', content_row.run_key)

            if self.db_marker == "vamps2":
                metadata_info['adapter_sequence_id'] = metadata_info['run_key_id']

                and_part = ' and project_id = %s' % metadata_info['project_id']
                metadata_info['dataset_id'] = self.get_id('dataset', content_row.dataset, and_part = and_part)

                metadata_info['domain_id'] = self.get_id('domain', domain_by_adj[content_row.taxonomic_domain])
                env_sample_source = self.get_env_sample_source(content_row)
                converted_env_sample_source = self.convert_env_sample_source(env_sample_source)
                metadata_info['env_package_id'] = self.get_id("env_package", converted_env_sample_source)

                platform = self.runobj.platform
                if self.runobj.platform in C.illumina_list:
                    platform = 'Illumina'
                metadata_info['sequencing_platform_id'] = self.get_id('sequencing_platform', platform)
                target_gene = '16s'
                if content_row.taxonomic_domain.lower().startswith(("euk", "its", "fung")):
                    target_gene = '18s'
                metadata_info['target_gene_id'] = self.get_id('target_gene', target_gene)
                metadata_info['updated_at'] = self.runobj.configPath['general']['date']
                for term_name in missing_terms:
                    metadata_info[term_name] = unknown_term_id[0][0]

            self.metadata_info_all[key] = metadata_info

    def get_env_sample_source(self, content_row):
        env_sample_source = self.my_conn.execute_fetch_select(
            "SELECT env_source_name FROM env_sample_source WHERE env_sample_source_id = %s" % (
                content_row.env_sample_source_id))[0][0]
        if not env_sample_source:
            env_sample_source = "unknown"
        return env_sample_source

    def insert_metadata(self, field_names_str, table_name, update_field_name):
        field_names_arr = field_names_str.split(", ")
        vals_part = '"%s", ' * len(field_names_arr)
        all_metadata_vals = []
        for file_prefix, metadata_dict in self.metadata_info_all.items():
            values_arr = [str(metadata_dict[f]) for f in field_names_arr]
            vals = vals_part % tuple(values_arr) + ' NOW()'
            all_metadata_vals.append('(%s)' % vals)

        group_vals = self.utils.grouper(all_metadata_vals, 1)
        query_tmpl = make_sql_for_groups(table_name, field_names_str + ", %s" % update_field_name)
        logger.debug("insert %s" % table_name)

        self.my_conn.run_groups(group_vals, query_tmpl, join_xpr = ', ')

    def insert_run_info(self):
        table_name = "run_info_ill"

        field_names_str = "adaptor, amp_operator, barcode, dataset_id, dna_region_id, file_prefix, illumina_index_id, insert_size, lane, overlap, platform, primer_suite_id, read_length, run_id, run_key_id, seq_operator, tubelabel"
        if self.db_marker == "env454":
            field_names_str += ", project_id"

        self.insert_metadata(field_names_str, table_name, "updated")

    def put_required_metadata(self):
        table_name = "required_metadata_info"

        field_names_str = "adapter_sequence_id, dataset_id, dna_region_id, domain_id, env_biome_id, env_feature_id, env_material_id, env_package_id, geo_loc_name_id, illumina_index_id, primer_suite_id, run_id, sequencing_platform_id, target_gene_id"

        self.insert_metadata(field_names_str, table_name, "updated_at")

    # def insert_primer(self):
    #     pass

    def del_sequence_pdr_info_by_project_dataset(self, projects = "", datasets = "", primer_suite = ""):
        my_sql1 = """DELETE FROM %s
                    USING %s JOIN run_info_ill USING (run_info_ill_id)
                    JOIN run USING(run_id)
                    JOIN project using(project_id)
                    JOIN dataset using(dataset_id)
                    JOIN primer_suite using(primer_suite_id)
                    WHERE primer_suite = "%s"
                    AND run = "%s"
                """ % (
            self.table_names["sequence_pdr_info_table_name"], self.table_names["sequence_pdr_info_table_name"],
            primer_suite, self.rundate)
        my_sql2 = " AND project in (" + projects + ")"
        my_sql3 = " AND dataset in (" + datasets + ")"

        if projects != "":
            my_sql1 += my_sql2
        if datasets != "":
            my_sql1 += my_sql3
        self.my_conn.execute_no_fetch(my_sql1)

    def count_sequence_pdr_info(self):
        results = {}
        join_add = ""
        primer_suites = self.get_primer_suite_name()
        lane = self.get_lane().pop()

        if self.db_marker == "vamps2":
            join_add = """ JOIN dataset using(dataset_id)
                       JOIN run_info_ill USING(run_info_ill_id, dataset_id) """
        elif self.db_marker == "env454":
            join_add = """ JOIN run_info_ill USING(run_info_ill_id) """

        for primer_suite in primer_suites:
            primer_suite_lane = primer_suite + ", lane " + lane
            my_sql = """SELECT count(%s_id)
                        FROM %s
                          %s
                          JOIN run USING(run_id)
                          JOIN primer_suite using(primer_suite_id)
                        WHERE run = '%s'
                          AND lane = %s
                          AND primer_suite = '%s';
                          """ % (
                self.table_names["sequence_pdr_info_table_name"], self.table_names["sequence_pdr_info_table_name"],
                join_add, self.rundate, lane, primer_suite)
            res = self.my_conn.execute_fetch_select(my_sql)
            try:
                if int(res[0][0]) > 0:
                    results[primer_suite_lane] = int(res[0][0])
            #                     results.append(int(res[0][0]))
            except Exception:
                self.utils.print_both("Unexpected error from 'count_sequence_pdr_info': %s" % sys.exc_info()[0])
                raise
        return results

    def get_primer_suite_name(self):
        primer_suites = [v.primer_suite for v in self.runobj.samples.values()]
        return list(set(primer_suites))

    # def get_dataset_names(self):
    #     datasets = [v.dataset for v in self.runobj.samples.values()]
    #     return '", "'.join(set(datasets))

    def get_lane(self):
        lane = [v.lane for v in self.runobj.samples.values()]
        return set(lane)

    # def count_seq_from_file(self):
    #     try:
    #         with open(self.unique_file_counts) as fd:
    #             file_seq_orig = dict(line.strip().split(None, 1) for line in fd)
    #         file_seq_orig_count = sum([int(x) for x in file_seq_orig.values()])
    #         return file_seq_orig_count
    #     except IOError as e:
    #         self.utils.print_both("Can't open file %s, error = %s" % (self.unique_file_counts, e))
    #     except Exception:
    #         self.utils.print_both("Unexpected error from 'count_seq_from_file': %s" % sys.exc_info()[0])
    #         raise

    def count_seq_from_files_grep(self):
        #         grep '>' *-PERFECT_reads.fa.unique
        #       or
        #         cd /xraid2-2/g454/run_new_pipeline/illumina/20130607/lane_5_A/analysis/reads_overlap/; grep '>' *_MERGED-MAX-MISMATCH-3.unique.nonchimeric.fa | wc -l; date
        try:
            self.suffix_used = list(set([ext for f in self.unique_fasta_files for ext in self.suff_list if f.endswith(ext)]))[0]
        except Exception:
            logger.error(
                "self.unique_fasta_files = %s, self.suff_list = %s" % (self.unique_fasta_files, self.suff_list))
            self.suffix_used = ""
        #         print(self.suffix_used)
        suffix = self.fasta_dir + "/*" + self.suffix_used
        program_name = "grep"
        call_params = " '>' " + suffix
        command_line = program_name + call_params
        p1 = Popen(command_line, stdout = PIPE, shell = True)
        p2 = Popen(split("wc -l"), stdin = p1.stdout, stdout = PIPE)
        #         output = p2.stdout.read().split(" ")[0].strip()
        output, err = p2.communicate()
        #         print(output)
        return int(output.strip())

    def check_seq_upload(self):
        file_seq_db_counts = self.count_sequence_pdr_info()
        file_seq_orig_count = self.count_seq_from_files_grep()
        msgs = []
        for pr_suite, file_seq_db_count in file_seq_db_counts.items():
            if file_seq_orig_count == file_seq_db_count:
                msg = "All sequences from files made it to %s for %s %s: %s == %s\n" % (
                    self.db_name, self.rundate, pr_suite, file_seq_orig_count, file_seq_db_count)
            else:
                msg = "Warning: Amount of sequences from files not equal to the one in the db for %s %s: %s != %s\n" % (
                    self.rundate, pr_suite, file_seq_orig_count, file_seq_db_count)
            logger.debug(msg)
            msgs.append(msg)
        return ", ".join(msgs)

    def put_seq_statistics_in_file(self, filename, seq_in_file):
        self.utils.write_seq_frequencies_in_file(self.unique_file_counts, filename, seq_in_file)

    def insert_taxonomy(self):
        # TODO: mv to Taxonomy?
        self.taxonomy.get_taxonomy_from_gast(self.gast_dict)
        if self.db_marker == "vamps2":
            self.taxonomy.insert_split_taxonomy()
        elif self.db_marker == "env454":
            self.taxonomy.insert_whole_taxonomy()
            self.taxonomy.get_taxonomy_id_dict()

    def insert_pdr_info(self, run_info_ill_id):
        all_insert_pdr_info_vals = self.seq.prepare_pdr_info_values(run_info_ill_id, self.all_dataset_run_info_dict,
                                                                    self.db_name, self.db_marker)

        group_vals = self.utils.grouper(all_insert_pdr_info_vals, len(all_insert_pdr_info_vals))
        sequence_table_name = self.table_names["sequence_table_name"]
        fields = ""
        if self.db_marker == "vamps2":
            fields = "dataset_id, run_info_ill_id, %s_id, seq_count, classifier_id" % sequence_table_name
        elif self.db_marker == "env454":
            fields = "run_info_ill_id, %s_id, seq_count" % sequence_table_name
        table_name = self.table_names["sequence_pdr_info_table_name"]
        # query_tmpl = make_sql_for_groups(table_name, fields)
        # print("q1: insert_pdr_info")
        # print(query_tmpl)
        unique_fields = ['dataset_id', 'run_info_ill_id', 'seq_count', 'sequence_id']
        if self.db_marker == "env454":
            unique_fields = ['run_info_ill_id', 'sequence_ill_id']
        query_tmpl1 = make_sql_for_groups1(table_name, fields, unique_fields)
        # print("q1a: insert_pdr_info")
        # print(query_tmpl1)

        logger.debug("insert sequence_pdr_info:")
        join_xpr = ' UNION ALL SELECT '
        self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)

    def insert_sequence_uniq_info(self):
        if self.db_marker == "vamps2":
            self.insert_silva_taxonomy_info_per_seq()
            self.seq.insert_sequence_uniq_info2()
        elif self.db_marker == "env454":
            self.seq.insert_sequence_uniq_info_ill(self.gast_dict)

    def insert_silva_taxonomy_info_per_seq(self):

        for fasta_id, gast_entry in self.gast_dict.items():
            curr_seq = self.seq.fasta_dict[fasta_id]
            sequence_id = self.seq.seq_id_dict[curr_seq]
            silva_taxonomy_id = self.taxonomy.silva_taxonomy_id_per_taxonomy_dict[gast_entry[0]]
            gast_distance = gast_entry[1]
            rank_id = self.taxonomy.all_rank_w_id[gast_entry[2]]
            refssu_id = 0
            refssu_count = 0
            # self.silva_taxonomy_info_per_seq_list = [[8559950L, 2436599, '0.03900', 0, 0, 83],...
            #         (taxonomy, gast_distance, rank, refssu_count, vote, minrank, taxa_counts, max_pcts, na_pcts, refhvr_ids) = self.gast_dict
            # vals = "(%s,  %s,  '%s',  '%s',  %s,  '%s')" % (
            #     sequence_id, silva_taxonomy_id, gast_distance, refssu_id, refssu_count, rank_id)
            vals = "%s AS sequence_id, %s AS silva_taxonomy_id, '%s' AS gast_distance, '%s' AS refssu_id, %s AS refssu_count, '%s' AS rank_id" % (
                sequence_id, silva_taxonomy_id, gast_distance, refssu_id, refssu_count, rank_id)
            self.silva_taxonomy_info_per_seq_list.append(vals)
        fields = "sequence_id, silva_taxonomy_id, gast_distance, refssu_id, refssu_count, rank_id"

        unique_fields = ['sequence_id']
        query_tmpl1 = make_sql_for_groups1("silva_taxonomy_info_per_seq", fields, unique_fields)

        # query_tmpl = make_sql_for_groups("silva_taxonomy_info_per_seq", fields)
        group_vals = self.utils.grouper(self.silva_taxonomy_info_per_seq_list,
                                        len(self.silva_taxonomy_info_per_seq_list))
        logger.debug("insert silva_taxonomy_info_per_seq:")
        join_xpr = ' UNION ALL SELECT '
        self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)


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
    def __init__(self, taxonomy, table_names, fasta_dir):

        self.utils = util.Utils()
        self.taxonomy = taxonomy
        self.my_conn = self.taxonomy.my_conn
        self.table_names = table_names
        self.fasta_dir = fasta_dir
        self.seq_id_dict = {}
        self.fasta_dict = {}
        self.seq_id_w_silva_taxonomy_info_per_seq_id = []

        self.sequences = ""

        self.seq_errors = []

    def prepare_fasta_dict(self, filename):
        read_fasta = fastalib.ReadFasta(filename)
        seq_list = self.make_seq_upper(read_fasta.sequences)
        self.fasta_dict = dict(zip(read_fasta.ids, seq_list))
        read_fasta.close()
        return seq_list

    @staticmethod
    def make_seq_upper(seq_list):
        sequences = [seq.upper() for seq in seq_list]  # here we make uppercase for VAMPS compartibility
        return sequences

    def insert_seq(self, sequences):
        seq_field = self.table_names["sequence_field_name"]
        val_tmpl = " COMPRESS('%s') AS %s "
        all_seq = set([val_tmpl % (seq, seq_field) for seq in sequences])
        # group_vals = self.utils.grouper(all_seq, 10)
        group_vals = self.utils.grouper(all_seq, len(all_seq))
        # query_tmpl = make_sql_for_groups(self.table_names["sequence_table_name"],
        #                                  self.table_names["sequence_field_name"])
        logger.debug("insert sequences:")

        unique_fields = ['sequence_comp']
        query_tmpl1 = make_sql_for_groups1(self.table_names["sequence_table_name"],
                                            self.table_names["sequence_field_name"], unique_fields)
        # print("q2a: sequences")
        # print(query_tmpl1)
        # self.my_conn.run_groups(group_vals, query_tmpl)
        # self.my_conn.run_groups(group_vals, query_tmpl1, ' UNION ALL SELECT ')
        join_xpr = ' UNION ALL SELECT '
        self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)

    def get_seq_id_dict(self, sequences):
        # TODO: ONCE IN CLASS

        sequence_field_name = self.table_names["sequence_field_name"]
        sequence_table_name = self.table_names["sequence_table_name"]
        id_name = self.table_names["sequence_table_name"] + "_id"
        query_tmpl = """SELECT %s, uncompress(%s) FROM %s WHERE %s in (COMPRESS(%s))"""
        val_tmpl = "'%s'"
        try:
            group_seq = self.utils.grouper(sequences, len(sequences))
            for group in group_seq:
                # key for conv.escape_string(key) in group if key is not None
                seq_part = '), COMPRESS('.join([val_tmpl % key for key in group if key is not None])
                my_sql = query_tmpl % (id_name, sequence_field_name, sequence_table_name, sequence_field_name, seq_part)
                res = self.my_conn.execute_fetch_select(my_sql)
                one_seq_id_dict = dict((y.decode().upper(), int(x)) for x, y in res)

                self.seq_id_dict.update(one_seq_id_dict)
        except Exception:
            if len(sequences) == 0:
                self.utils.print_both(
                    "ERROR: There are no sequences, please check if there are correct fasta files in the directory %s" % self.fasta_dir)
            raise

    def prepare_pdr_info_values(self, run_info_ill_id, all_dataset_run_info_dict, db_name, current_db_host_name):

        all_insert_pdr_info_vals = []

        for fasta_id, seq in self.fasta_dict.items():
            if not run_info_ill_id:
                err_msg = "ERROR: There is no run info yet, please check if it's uploaded to %s" % db_name
                self.utils.print_both(err_msg)
                self.seq_errors.append(err_msg)
                break
            try:
                sequence_id = self.seq_id_dict[seq]

                seq_count = int(fasta_id.split('|')[-1].split(':')[-1])
                vals = ""
                sequence_id_field = self.table_names["sequence_table_name"] + "_id"

                if current_db_host_name == "vamps2":
                    try:
                        dataset_id = all_dataset_run_info_dict[run_info_ill_id]
                        # vals = "(%s, %s, %s, %s)" % (dataset_id, sequence_id, seq_count, C.classifier_id)
                        vals = "%s AS dataset_id, %s AS run_info_ill_id, %s AS %s, %s AS seq_count, %s AS classifier_id" % (dataset_id, run_info_ill_id, sequence_id, sequence_id_field, seq_count, C.classifier_id)
                    except KeyError:
                        logger.error("No such run info, please check a file name and the csv file")
                        logger.debug("From prepare_pdr_info_values, all_dataset_run_info_dict: %s" % all_dataset_run_info_dict)

                elif current_db_host_name == "env454":
                    # vals = "(%s, %s, %s)" % (run_info_ill_id, sequence_id, seq_count)
                    vals = "%s AS run_info_ill_id, %s AS %s, %s AS seq_count" % (run_info_ill_id, sequence_id, sequence_id_field, seq_count)

                all_insert_pdr_info_vals.append(vals)
                fasta_id = ""
                seq = ""
                seq_count = 0
                sequence_id = ""
            except Exception:
                logger.error("FFF0 fasta_id %s" % fasta_id)
                logger.error("SSS0 seq %s" % seq)
                raise
        return all_insert_pdr_info_vals

    def get_seq_id_w_silva_taxonomy_info_per_seq_id(self):
        logger.debug("get_seq_id_w_silva_taxonomy_info_per_seq_id:")
        sequence_ids_strs = [str(i) for i in self.seq_id_dict.values()]
        field_names = "sequence_id, silva_taxonomy_info_per_seq_id"
        where_part = 'WHERE sequence_id in (%s)'
        query_tmpl = """SELECT %s FROM %s %s""" % (field_names, "silva_taxonomy_info_per_seq", where_part)
        group_vals = self.utils.grouper(sequence_ids_strs,
                                        len(sequence_ids_strs))
        for group in group_vals:
            val_part = ", ".join([key for key in group if key is not None])
            my_sql = query_tmpl % val_part
            self.seq_id_w_silva_taxonomy_info_per_seq_id.extend(self.my_conn.execute_fetch_select(my_sql))

    def insert_sequence_uniq_info2(self):
        self.get_seq_id_w_silva_taxonomy_info_per_seq_id()
        fields = "sequence_id, silva_taxonomy_info_per_seq_id"
        # sequence_uniq_info_values = ["(%s,  %s)" % (i1, i2) for i1, i2 in self.seq_id_w_silva_taxonomy_info_per_seq_id]
        sequence_uniq_info_values = ["%s AS sequence_id, %s AS get_seq_id_w_silva_taxonomy_info_per_seq_id" % (i1, i2) for i1, i2 in self.seq_id_w_silva_taxonomy_info_per_seq_id]
        # query_tmpl = make_sql_for_groups("sequence_uniq_info", fields)
        group_vals = self.utils.grouper(sequence_uniq_info_values, len(sequence_uniq_info_values))
        logger.debug("insert sequence_uniq_info_ill:")
        # print("q3: insert_sequence_uniq_info2")
        # print(query_tmpl)
        unique_fields = ['sequence_id']
        query_tmpl1 = make_sql_for_groups1("sequence_uniq_info", fields, unique_fields)
        # print("q3a: insert_sequence_uniq_info2")
        # print(query_tmpl1)
        join_xpr = ' UNION ALL SELECT '

        self.my_conn.run_groups(group_vals, query_tmpl1, join_xpr)

    def insert_sequence_uniq_info_ill(self, gast_dict):
        all_insert_sequence_uniq_info_ill_vals = []
        for fasta_id, gast in gast_dict.items():
            (taxonomy, distance, rank, refssu_count, vote, minrank, taxa_counts, max_pcts, na_pcts, refhvr_ids) = gast
            seq = self.fasta_dict[fasta_id]
            sequence_id = self.seq_id_dict[seq]
            rank_id = self.taxonomy.all_rank_w_id[rank]
            if taxonomy in self.taxonomy.tax_id_dict:
                taxonomy_id = self.taxonomy.tax_id_dict[taxonomy]
                vals = """(%s,  %s,  '%s',  '%s',  %s,  '%s')
                        """ % (sequence_id, taxonomy_id, distance, refssu_count, rank_id, refhvr_ids.rstrip())
                all_insert_sequence_uniq_info_ill_vals.append(vals)
        group_vals = self.utils.grouper(all_insert_sequence_uniq_info_ill_vals,
                                        len(all_insert_sequence_uniq_info_ill_vals))

        fields = "%s_id, taxonomy_id, gast_distance, refssu_count, rank_id, refhvr_ids" % (
            self.table_names["sequence_table_name"])
        query_tmpl = make_sql_for_groups("sequence_uniq_info_ill", fields)

        logger.debug("insert sequence_uniq_info_ill:")
        self.my_conn.run_groups(group_vals, query_tmpl)

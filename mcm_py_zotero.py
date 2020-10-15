#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyzotero import zotero
from collections import defaultdict
import util
from mcm_upload_util import Upload, File_retrival, DataManaging
import argparse
import csv


"""
    [account_type] => group
    [account_id] => 1415490
    [start] => 
    [api_key] => U4CPfWiKzcs7iyJV9IdPnEZU
"""

library_id = "1415490"
library_type = "group"
api_key = "U4CPfWiKzcs7iyJV9IdPnEZU"

zot = zotero.Zotero(library_id, library_type, api_key)


class Output(Upload):
  def __init__(self):
    Upload.__init__(self)
    self.zotero_to_sql_fields = {
      'creators'    : 'role.role', # creator
      'name'        : 'person.person',  # creator, #creator_other
      'firstName'   : 'person.first_name',  # creator, #creator_other
      'lastName'    : 'person.last_name',  # creator, #creator_other
      'abstractNote': 'description.description',
      'bookTitle'   : 'title.title',
      'title'       : 'title.title',
      'date'        : 'season.season',  # 'date_exact', 'date_season', 'date_season_yyyy',
      'language'    : 'language.language',
      'publicationTitle': 'publisher.publisher', # ? 'title.title' ?
      'publisher'   : 'publisher.publisher',
      'rights'      : 'rights.rights',
      'volume'      : 'source.source',
    }

    self.key_to_csv_field = {
      "identifier"                 : "Identifier",
      "title"                      : "Title",
      "content"                    : "Content",
      "content_url"                : "Content URL",
      "content_url_audio"          : "Content URL (Audio)",
      "content_url_transcript"     : "Content URL (Transcript)",
      "creator"                    : "Creator",
      "creator_other"              : "Creator.Other",
      "subject_aplace"             : "Subject.Place",
      "coverage_lat"               : "Coverage.Lat",
      "coverage_long"              : "Coverage.Long",
      "subject_associated_places"  : "Subject.Associated.Places",
      "subject_people"             : "Subject.People",
      "subject_academic_field"     : "Subject.Academic.Field",
      "subject_other"              : "Subject.Other",
      "subject_season"             : "Subject.Season",
      "season"                : "Date.Season",
      "date_season"                : "Date.Season",
      "date_season_yyyy"           : "Date.Season (YYYY)",
      "date_exact"                 : "Date.Exact",
      "date_digital"               : "Date.Digital",
      "description"                : "Description",
      "format"                     : "Format",
      "digitization_specifications": "Digitization Specifications",
      "contributor"                : "Contributor",
      "type"                       : "Type",
      "country"                    : "Country",
      "language"                   : "Language",
      "relation"                   : "Relation",
      "source"                     : "Source",
      "publisher"                  : "Publisher",
      "publisher_location"         : "Publisher Location",
      "bibliographic_citation"     : "Bibliographic Citation",
      "Rights"                     : "rights"
    }


    args = self.check_args()
    self.data_managing = DataManaging()
    self.metadata_type_table_name = "type"
    self.identifier_first_character = "Z"
    self.metadata_type = "Bibliographic Item"
    self.metadata_type_id = self.get_metadata_type_id()

    self.entry_rows_dict = defaultdict()
    self.out_dict_of_vals = defaultdict()
    self.roles = defaultdict()
    if args.output_file:
      self.out_file_name = args.output_file
      self.make_out_dict_of_vals()
      self.out_to_tsv()
    else:
      self.make_upload_queries()
      self.insert_entry_row()
    print("DONE uploading Zotero")

  def check_args(self):
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file_name',
                        required = False, action = 'store', dest = 'output_file',
                        help = '''Output file name''')
    return parser.parse_args()


  def out_to_tsv(self):
    csv_columns = list(self.key_to_csv_field.values())

    try:
      with open(self.out_file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        for data in self.out_dict_of_vals:
          writer.writerow(data)
    except IOError:
      print("I/O error")

  def insert_person_combination_and_get_id(self, person_list):
    persons_str = "; ".join(sorted(person_list))
    table_name = "person"
    field_name = "person"
    return self.get_id_by_serch_or_insert(table_name, field_name, persons_str)

  def correct_keys(self, val_dict):
    temp_dict = defaultdict()
    for k, v in val_dict.items():
      if k[:-3] in self.many_values_to_one_field.keys():
        k_new = ""
        if k == "person_id":
          k_new = "creator_id"
        elif k == "season_id":
          k_new = "date_season_id"
        temp_dict[k_new] = v
      else:
        temp_dict[k] = v

    return temp_dict

  def get_metadata_type_id(self):
    metadata_type_ins_res = self.mysql_utils.execute_insert_mariadb(self.metadata_type_table_name, self.metadata_type_table_name,
                                                          self.metadata_type)
    metadata_type_id = metadata_type_ins_res[1]
    if metadata_type_id == 0:
      metadata_type_id = self.mysql_utils.get_id_esc(self.metadata_type_table_name + "_id", self.metadata_type_table_name, self.metadata_type_table_name, self.metadata_type)
    return metadata_type_id

  def add_metadata_type(self, val_dict):
    val_dict[self.metadata_type_table_name + "_id"] = self.metadata_type_id
    return val_dict

  def check_or_create_identifier(self, val_dict):
    if 'identifier' not in val_dict.keys():
      (db_id, curr_identifier) = self.data_managing.check_or_create_identifier(self.metadata_type, self.identifier_first_character)
      val_dict[self.data_managing.identifier_table_name + "_id"] = db_id
      return val_dict

  def insert_entry_row(self):
    """
    *) get all "entry" table fields except primary key - get_entry_table_field_names
    *) for data from zotero find correct field names for id (do that in class Export)
    *) for all fields in "entry" table which are not in zotero dump find the "empty" id
    *) for each field form a query
    *) ? search if exists:
         select_q = '''SELECT entry_id FROM entry WHERE {}'''.format(all_ids_row)
    *) if not exists insert
    """
    for key, val_dict in self.entry_rows_dict.items():
      if len(val_dict) > 0:
        """
        self.entry_rows_dict = {defaultdict: 5} defaultdict(None, {'JSQB7M8J': defaultdict(None, {'title_id': 4791, 'person': [{'person_id': 1121, 'role_id': 1}], 'publisher_id': 14, 'source_id': 802, 'season_id': 457}), 'NKVCAI2K': defaultdict(None, {}), '4Q3GMMWU': defaultdict(None, {}),...
        """
        current_output_dict = self.correct_keys(val_dict)
        current_output_dict = self.check_or_create_identifier(current_output_dict)
        current_output_dict = self.add_metadata_type(current_output_dict)
        dict_w_all_ids = self.find_empty_ids(current_output_dict)
        self.mysql_utils.execute_many_fields_one_record(self.entry_table_name, list(dict_w_all_ids.keys()),
                                                   tuple(dict_w_all_ids.values()))

  def make_full_name(self, val_d):
    return "{}, {}".format(val_d['lastName'], val_d['firstName'])

  def update_first_last_names(self, val_d, db_id):
    names_tuple = (val_d['lastName'], val_d['firstName'])
    (table_name, last_name) = self.zotero_to_sql_fields['lastName'].split(".")
    (table_name, first_name) = self.zotero_to_sql_fields['firstName'].split(".")

    update_q = '''UPDATE {}
      SET {} = %s, {} = %s 
      WHERE {} = {}'''.format(table_name, last_name, first_name, table_name + '_id', db_id)
    self.mysql_utils.execute_no_fetch(update_q, names_tuple)

  def get_person_id(self, full_name):
    table_name = "person"
    field_name = "person"
    db_id = self.get_id_by_serch_or_insert(table_name, field_name, full_name)
    return db_id

  def get_id_by_serch_or_insert(self, table_name, field_name, value):
    field_name_id = field_name + "_id"
    try:
      db_id = self.mysql_utils.get_id_esc(field_name_id, table_name, field_name, value)
    except IndexError:
      try:
        mysql_res = self.mysql_utils.execute_insert_mariadb(table_name, field_name, value)
        db_id = self.mysql_utils.get_id_esc(field_name_id, table_name, field_name, value)
      except IndexError: # A weird one with a single quote in utf8 (came from a tsv) vs. latin (came from Zotero): man’s vs. man's
        db_id = self.single_quote_encoding_err_handle(table_name, field_name, value)
    return db_id

  def single_quote_encoding_err_handle(self, table_name, field_name, value):
    value_part = value.split("'")[0] + "%"
    id_query = "SELECT {} FROM {} WHERE {} like %s".format(field_name + "_id", table_name, field_name)
    id_result_full = self.mysql_utils.execute_fetch_select(id_query, value_part)
    db_id = list(utils.extract(id_result_full))[0]
    return db_id

  def update_person(self, val_dict, z_key, table_name, field_name):
    person_id_list = []
    current_persons_list = []

    for d in val_dict:
      full_name = self.make_full_name(d)

      person_db_id = self.get_person_id(full_name)
      self.update_first_last_names(d, person_db_id)

      current_role = d['creatorType']
      try:
        role_db_id1 = self.roles[current_role]
      except KeyError:
        role_db_id1 = self.get_id_by_serch_or_insert(table_name, field_name, current_role)
        self.roles[current_role] = role_db_id1
      person_id_list.append({"person_id": person_db_id, "role_id": role_db_id1})
      current_persons_list.append(full_name)

      self.entry_rows_dict[z_key]["role_id"] = role_db_id1  # TODO: check if different roles could be in one dict

    all_cur_persons_id = self.insert_person_combination_and_get_id(current_persons_list)
    self.entry_rows_dict[z_key]["person_id"] = all_cur_persons_id

  def make_out_dict_of_vals(self):
    for z_entry in export.all_items_dump:
      z_key = z_entry['key']
      self.out_dict_of_vals[z_key] = defaultdict()
      for key, val in z_entry['data'].items():
        if val:
          try:
            db_tbl_field_name = self.zotero_to_sql_fields[key]
            (table_name, field_name) = db_tbl_field_name.split(".")
            if isinstance(val, list):
              # self.update_person(data_val_dict, z_key, table_name, field_name)  # TODO: change parameters
              current_authors = self.flatten_person(val)
              self.out_dict_of_vals[z_key]["Creator"] = current_authors
            else:
              tsv_field_name = self.key_to_csv_field[field_name]
              self.out_dict_of_vals[z_key][tsv_field_name] = val
          except KeyError:
            pass

  def flatten_person(self, val_dict):
    current_persons_list = []

    for d in val_dict:
      full_name = self.make_full_name(d)
      current_persons_list.append(full_name)
      # make dict of creator_types to csv fields correspondens
      # current_role = d['creatorType']
      # current_persons_dict[current_role] = full_name

      # self.out_dict_of_vals[z_key]["creator"] = full_name
    return "; ".join(current_persons_list)

  def make_entry_rows_dict_of_ids(self, key, data_val_dict, z_key):
    try:
      db_tbl_field_name = self.zotero_to_sql_fields[key]
      (table_name, field_name) = db_tbl_field_name.split(".")

      if isinstance(data_val_dict, list):
        self.update_person(data_val_dict, z_key, table_name, field_name) # TODO: change parameters
      else:
        db_id = self.get_id_by_serch_or_insert(table_name, field_name, data_val_dict)
        self.entry_rows_dict[z_key][field_name + "_id"] = db_id
    except KeyError:
      pass # zotero field is not in the db field names list

  def make_upload_queries(self):
    for z_entry in export.all_items_dump:
      z_key = z_entry['key']
      self.entry_rows_dict[z_key] = defaultdict()
      for k, v in z_entry['data'].items():
        if v:
          self.make_entry_rows_dict_of_ids(k, v, z_key)


class DownloadFilesFromZotero(File_retrival):
  def __init__(self):
    File_retrival.__init__(self)
    self.download_all_from_zotero()

    print("END of File_retrival = download_files_from_zotero")

  def download_all_from_zotero(self):
    """'attachment': {'href': 'https://api.zotero.org/groups/1415490/items/M5BQR9VK', 'type': 'application/json', 'attachmentType': 'audio/mpeg', 'attachmentSize': 24740700}"""
    for entry in export.all_items_dump:
      try:
        attachment_d = entry['links']['attachment']
        addr = attachment_d['href']
        att_type = attachment_d['attachmentType']
        att_size = attachment_d['attachmentSize']
        item_id = addr.rsplit('/', 1)[1]

        zot.dump(item_id, path = self.files_path)
      except KeyError:
        """ No attachment """
        pass


class Export:
  def __init__(self):

    # USE this for real:
    # self.all_items_dump = self.dump_all_items()
    # debug short
    self.all_items_dump = zot.top(limit = 5)
    # self.decoded_data_list = []

    self.all_items_fields = set()
    self.get_all_zotero_fields()

  def get_all_items_to_file(self):
    dump_all_items = open('dump_all_items.txt', 'w')
    all_text = self.decode(zot.everything(zot.top()))
    print(all_text, file = dump_all_items)
    dump_all_items.close()

  def get_all_zotero_fields(self):
    for item in self.all_items_dump:
      self.all_items_fields = self.all_items_fields | item['data'].keys()

  def dump_all_items(self):
    return zot.everything(zot.top())


if __name__ == '__main__':
  utils = util.Utils()

  export = Export()
  file_from_url = DownloadFilesFromZotero()
  import_to_mysql = Output()


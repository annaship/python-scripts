#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import os
from pyzotero import zotero
from collections import defaultdict
import util
from mcm_upload_util import Upload, FileRetrival, DataManaging
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
collectionIDs = ['37TI82V3', 'AQNRKZB2', 'AMJZ6VM2', 'DLLAHRNY', 'BN6W93P3', 'ZGX6YQIQ', 'KG7KJ3QE']

zot = zotero.Zotero(library_id, library_type, api_key)


class Output(Upload):
  def __init__(self):
    Upload.__init__(self)
    self.zotero_to_sql_fields = {
      # 'accessed'    : 'season.season', #date_digital
      'url'                   : 'content_url.content_url',
      'bibliographic_citation': 'bibliographic_citation.bibliographic_citation',
      'source'                : 'source.source',  # 'Volume'('Issue'): 'Pages'
      'format'                : 'format.format',
      'subject_other'         : 'subject_other.subject_other',
      'abstractNote'          : 'description.description',
      # 'bookTitle'   : 'title.title',
      'creators'              : 'role.role',  # creator
      'date'                  : 'season.season',  # 'date_exact', 'date_season', 'date_season_yyyy',
      'firstName'             : 'person.first_name',  # creator, #creator_other
      'language'              : 'language.language',
      'lastName'              : 'person.last_name',  # creator, #creator_other
      'name'                  : 'person.person',  # creator, #creator_other
      # 'publicationTitle': 'publisher.publisher', # ? 'title.title' ?
      'publisher'             : 'publisher.publisher',
      'rights'                : 'rights.rights',
      'title'                 : 'title.title',
      # 'volume'      : 'source.source',
    }

    self.substitute_keys = {
      "person_id"     : "creator_id",
      "season_id"     : "date_season_id",
      "content_url_id": "content_url_id",
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
      "subject_place"              : "Subject.Place",
      "coverage_lat"               : "Coverage.Lat",
      "coverage_long"              : "Coverage.Long",
      "subject_associated_places"  : "Subject.Associated.Places",
      "subject_people"             : "Subject.People",
      "subject_academic_field"     : "Subject.Academic.Field",
      "subject_other"              : "Subject.Other",
      "subject_season"             : "Subject.Season",
      "season"                     : "Date.Season",
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
      "rights"                     : "Rights"
    }

    self.data_managing = DataManaging()
    self.metadata_type_table_name = "type"
    self.identifier_first_character = "Z"
    self.metadata_type = "Bibliographic Item"
    self.metadata_type_id = self.get_metadata_type_id()

    self.entry_rows_dict = defaultdict()
    self.out_list_of_dict_of_vals = []
    self.out_list_of_dict_of_vals_z_keys = []
    self.roles = defaultdict()
    if args.output_file:
      self.out_file_name = args.output_file
      print("Downloading Zotero entries as a tsv file {}".format(self.out_file_name))

      self.make_out_dict_of_vals()
      self.out_to_tsv_file()
      print("DONE downloading Zotero")
    elif not args.no_db_upload:
      print("Uploading Zotero entries into the database")

      self.upload_zotero_keys()
      self.make_upload_queries()
      self.insert_entry_row()
      print("DONE uploading Zotero")

  def upload_zotero_keys(self):
    """Upload all zotero keys and keep reference with MCM type identifier in order to have only one identifier per z-key"""
    all_z_keys = [z_entry['key'] for z_entry in export.all_items_dump]
    self.simple_mass_upload('zotero_key', 'zotero_key', all_z_keys)

  def out_to_tsv_file(self):

    csv_columns = list(self.key_to_csv_field.values())
    csv_columns.insert(0, 'z_key')

    try:
      with open(self.out_file_name, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter = "\t", fieldnames = csv_columns, quoting = csv.QUOTE_ALL)
        writer.writeheader()
        for data in self.out_list_of_dict_of_vals:
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
        try:
          k_new = self.substitute_keys[k]
        except KeyError:
          k_new = ""
        temp_dict[k_new] = v
      else:
        temp_dict[k] = v

    return temp_dict

  def get_metadata_type_id(self):
    metadata_type_ins_res = self.mysql_utils.execute_insert_mariadb(self.metadata_type_table_name,
                                                                    self.metadata_type_table_name,
                                                                    self.metadata_type)
    metadata_type_id = metadata_type_ins_res[1]
    if metadata_type_id == 0:
      metadata_type_id = self.mysql_utils.get_id_esc(self.metadata_type_table_name + "_id",
                                                     self.metadata_type_table_name, self.metadata_type_table_name,
                                                     self.metadata_type)
    return metadata_type_id

  def add_metadata_type(self, val_dict):
    val_dict[self.metadata_type_table_name + "_id"] = self.metadata_type_id
    return val_dict

  def check_or_create_identifier(self, z_key, val_dict):
    identifier_id = self.check_if_exists(z_key)
    if int(identifier_id) <= 0:
      (identifier_id, curr_identifier) = self.data_managing.check_or_create_identifier(self.identifier_first_character,
                                                                                       "")
      self.insert_identifier_id_into_z_key(z_key, identifier_id)
    val_dict[self.data_managing.identifier_table_name + "_id"] = identifier_id
    return val_dict

  def insert_identifier_id_into_z_key(self, z_key, identifier_id):
    zotero_key_table_name = "zotero_key"
    identifier_id_name = self.data_managing.identifier_table_name + "_id"  # 'identifier_id'

    update_q = '''UPDATE {}
      SET {} = %s 
      WHERE {} = %s
      '''.format(zotero_key_table_name, identifier_id_name, zotero_key_table_name)

    self.mysql_utils.execute_no_fetch(update_q, [identifier_id, z_key])
    "Update zotero_key set identifier_id = identifier_id where zotero_key = zotero_key"

  def check_if_exists(self, z_key):
    identifier_id_name = self.data_managing.identifier_table_name + "_id"  # 'identifier_id'
    zotero_key_table_name = "zotero_key"
    try:
      identifier_id = self.mysql_utils.get_id_esc(identifier_id_name, zotero_key_table_name, [zotero_key_table_name],
                                                  [z_key])
    except IndexError:
      identifier_id = 0
    return identifier_id

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
    for z_key, val_dict in self.entry_rows_dict.items():
      if len(val_dict) > 0:
        """
        val_dict = {defaultdict: 8} defaultdict(None, {'source_id': 305, 'format_id': 2, 'bibliographic_citation_id': 2, 'title_id': 3, 'role_id': 2, 'person_id': 2, 'description_id': 2, 'season_id': 2})
        """
        current_output_dict = self.correct_keys(val_dict)
        current_output_dict = self.add_metadata_type(current_output_dict)
        current_output_dict = self.find_empty_ids(current_output_dict)
        current_output_dict = self.check_or_create_identifier(z_key, current_output_dict)
        all_fields = list(current_output_dict.keys())
        q_addition = self.format_update_duplicates(all_fields)
        self.mysql_utils.execute_many_fields_one_record(self.entry_table_name, all_fields,
                                                        tuple(current_output_dict.values()), addition = q_addition)

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
      except IndexError:  # A weird one with a single quote in utf8 (came from a tsv) vs. latin (came from Zotero): man’s vs. man's
        db_id = self.single_quote_encoding_err_handle(table_name, field_name, value)
    return db_id

  def single_quote_encoding_err_handle(self, table_name, field_name, value):
    value_part = value.split("'")[0] + "%"
    id_query = "SELECT {} FROM {} WHERE {} LIKE %s".format(field_name + "_id", table_name, field_name)
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

      self.entry_rows_dict[z_key]["role_id"] = role_db_id1

    all_cur_persons_id = self.insert_person_combination_and_get_id(current_persons_list)
    self.entry_rows_dict[z_key]["person_id"] = all_cur_persons_id

  def make_out_dict_of_vals(self):
    for z_entry in export.all_items_dump:
      temp_dict = defaultdict()
      temp_dict['z_key'] = z_entry['key']
      for key, val in z_entry['data'].items():
        if val:
          try:
            db_tbl_field_name = self.zotero_to_sql_fields[key]
            (table_name, field_name) = db_tbl_field_name.split(".")
            if isinstance(val, list):
              current_authors = self.flatten_person(val)
              temp_dict["Creator"] = current_authors
            else:
              tsv_field_name = self.key_to_csv_field[field_name]
              temp_dict[tsv_field_name] = val
          except KeyError:
            pass
      if temp_dict['z_key'] not in self.out_list_of_dict_of_vals_z_keys:
        self.out_list_of_dict_of_vals_z_keys.append(temp_dict['z_key'])
        if len(temp_dict) > 0:
          self.out_list_of_dict_of_vals.append(temp_dict)

  def flatten_person(self, val_dict):
    current_persons_list = []

    for d in val_dict:
      full_name = self.make_full_name(d)
      current_persons_list.append(full_name)
    return "; ".join(current_persons_list)

  def make_combined_values_from_z(self, z_entry_data):
    keys_from_z_entry_data = ['bookTitle',
                              'creators',
                              'issue',
                              'pages',
                              'publicationTitle',
                              'series',
                              'tags',
                              'tags',
                              'title',
                              'url',
                              'volume']

    combined_values_from_z = defaultdict()
    exist_from_z_entry_data = defaultdict()

    for key in keys_from_z_entry_data:
      if key in z_entry_data.keys() and len(z_entry_data[key]) > 0:
        exist_from_z_entry_data[key] = z_entry_data[key]

    issue = ""
    if 'issue' in exist_from_z_entry_data.keys():
      issue = "({})".format(exist_from_z_entry_data['issue'])
    vol_iss = ""
    if 'volume' in exist_from_z_entry_data.keys() and issue:
      vol_iss = "{}{}: ".format(exist_from_z_entry_data['volume'], issue)
    if 'pages' in exist_from_z_entry_data.keys() and vol_iss:
      combined_values_from_z['source'] = "{}{} ".format(vol_iss, exist_from_z_entry_data['pages'])

    if 'title' in exist_from_z_entry_data.keys():
      combined_values_from_z['format'] = "PDF "

    sec_title = ""
    if 'bookTitle' in exist_from_z_entry_data.keys():
      sec_title = exist_from_z_entry_data['bookTitle']
    if 'publicationTitle' in exist_from_z_entry_data.keys():
      sec_title = exist_from_z_entry_data['publicationTitle']

    creators = ""
    try:
      creators = self.flatten_person(z_entry_data['creators'])
    except KeyError:
      pass

    try:
      combined_values_from_z['bibliographic_citation'] = """{} {}. {}{}. {}{}""".format(creators,
                                                                                        z_entry_data['title'],
                                                                                        sec_title,
                                                                                        z_entry_data['series'],
                                                                                        combined_values_from_z[
                                                                                          'source'],
                                                                                        z_entry_data['url'])
    except KeyError:
      pass

    if 'tags' in exist_from_z_entry_data.keys():
      tags = [d['tag'] for d in exist_from_z_entry_data['tags']]
      combined_values_from_z['subject_other'] = ", ".join(tags)

    """
    z_entry_data['tags'][
      {'tag': "chlorophyll <span class='italic'>a</span>", 'type': 1}, {'tag': 'conductivity', 'type': 1}, {
        'tag': 'nutrients', 'type': 1
      }, {'tag': 'pH', 'type': 1}, {'tag': 'pond ecosystems', 'type': 1}, {'tag': 'temporal change', 'type': 1}]
  
    z_entry_data['tags'][{'tag': '#broken_attachments'}, {'tag': '#duplicate_attachments'}]"""

    return combined_values_from_z

  def make_entry_rows_dict_of_ids(self, key, data_val_dict, z_key):
    try:
      db_tbl_field_name = self.zotero_to_sql_fields[key]
      (table_name, field_name) = db_tbl_field_name.split(".")
      if isinstance(data_val_dict, list):
        self.update_person(data_val_dict, z_key, table_name, field_name)
      else:
        db_id = self.get_id_by_serch_or_insert(table_name, field_name, data_val_dict)
        self.entry_rows_dict[z_key][field_name + "_id"] = db_id
    except KeyError:
      pass  # zotero field is not in the db field names list

  def make_upload_queries(self):
    for z_entry in export.all_items_dump:
      z_key = z_entry['key']
      self.entry_rows_dict[z_key] = defaultdict()
      combined_values_from_z = self.make_combined_values_from_z(z_entry['data'])
      dict_to_use = {**combined_values_from_z, **z_entry['data']}
      for k, v in dict_to_use.items():
        if v:
          self.make_entry_rows_dict_of_ids(k, v, z_key)


class DownloadFilesFromZotero(FileRetrival):
  def __init__(self):
    FileRetrival.__init__(self)
    self.download_all_from_zotero()

    print("END of FileRetrival = download_files_from_zotero")

  def download_all_from_zotero(self):
    """'attachment': {'href': 'https://api.zotero.org/groups/1415490/items/M5BQR9VK', 'type': 'application/json', 'attachmentType': 'audio/mpeg', 'attachmentSize': 24740700}"""
    for entry in export.all_items_dump:
      try:
        attachment_d = entry['links']['attachment']
        addr = attachment_d['href']
        item_id = addr.rsplit('/', 1)[1]

        files_path = self.get_files_path('zotero_attachments')
        zot.dump(item_id, path = files_path)
      except KeyError:
        """ No attachment """
        pass


class Export:
  def __init__(self):
    self.all_items_dump = []
    all_keys = self.get_all_coll_key()

    if args.get_5_zotero_entries:
      # debug short
      self.all_items_dump = zot.top(limit = 5)

    else:
      # self.all_items_dump = self.dump_all_items()
      # USE this for real:
      for collection_key in all_keys:
        items = zot.everything(zot.collection_items(collection_key))
        self.all_items_dump += items

    if args.raw_zotero_entries:
      self.dump_raw_zotero_entries()

  def dump_raw_zotero_entries(self):
    print("Downloading each Zotero entry into a separate tsv file")
    files_util = FileRetrival()
    self.files_path = files_util.get_files_path("raw_zotero_entries")
    self.all_items_fields = set()
    self.get_all_zotero_fields()
    self.get_all_items_to_tsv_file()
    print("DONE: downloading each Zotero entry into a separate tsv file")

  def get_all_coll_key(self):
    all_keys = []
    for collectionID in collectionIDs:
      z = zot.all_collections(collectionID)
      all_keys += [x["key"] for x in z]
    return all_keys

  def get_all_items_to_file(self):
    dump_all_items = open('dump_all_items.txt', 'w')
    all_text = self.decode(zot.everything(zot.top()))
    print(all_text, file = dump_all_items)
    dump_all_items.close()

  def get_all_items_to_tsv_file(self):
    fieldnames = set()
    for d in self.all_items_dump:
      fieldnames.update(d['data'].keys())
      my_dict = d['data']
      flat_dict = utils.flatten_dict(my_dict)
      self.write_flat_dict_to_tsv(flat_dict)

  def write_flat_dict_to_tsv(self, flat_dict):
    keys, values = [], []
    for key, value in flat_dict.items():
      keys.append(key)
      values.append(value)

    dump_all_items_tsv_file_name_base = 'zotero_item'
    f_name = "{}/{}_{}.tsv".format(self.files_path, dump_all_items_tsv_file_name_base, flat_dict['key'])

    with open(f_name, "w") as outfile:
      csvwriter = csv.writer(outfile, delimiter = '\t')
      csvwriter.writerow(keys)
      csvwriter.writerow(values)

  def get_all_zotero_fields(self):
    for item in self.all_items_dump:
      self.all_items_fields = self.all_items_fields | item['data'].keys()

  def dump_all_items(self):
    return zot.everything(zot.top())


if __name__ == '__main__':
  utils = util.Utils()


  def check_args():
    myusage = """
        By default will write all Zotero entries into the database.
        
        Command line example: python3 %(prog)s -f /tmp/temp.tsv

    """
    parser = argparse.ArgumentParser(description = myusage)

    parser.add_argument('-f', '--file_name',
                        required = False, action = 'store', dest = 'output_file',
                        help = '''Output file name. Zotero entries go into the file, not into the database.''')
    parser.add_argument('-d', '--download_attachments',
                        required = False, action = 'store_true', dest = 'download_attachments',
                        help = '''Download Zotero attachments into sites/default/files/zotero_attachments''')
    parser.add_argument('-r', '--raw_zotero_entries',
                        required = False, action = 'store_true', dest = 'raw_zotero_entries',
                        help = '''Dump all Zotero entries into individual tsv files in sites/default/files/raw_zotero_entries.''')
    parser.add_argument('-n', '--no_db_upload',
                        required = False, action = 'store_true', dest = 'no_db_upload',
                        help = '''Do not upload data into the database.''')
    parser.add_argument('-na', '--get_5_zotero_entries',
                        required = False, action = 'store_true', dest = 'get_5_zotero_entries',
                        help = '''Get only 5 Zotero entries (not all) for debugging.''')

    return parser.parse_args()


  args = check_args()

  export = Export()
  if args.download_attachments:
    print("Downloading Zotero attachments")
    file_from_url = DownloadFilesFromZotero()
    print("Done downloading Zotero attachments")

  import_to_mysql = Output()

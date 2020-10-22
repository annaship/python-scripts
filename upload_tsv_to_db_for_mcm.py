#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
*) upload the whole csv into one table, separate, add ids
*) whole_tsv_dump is temporary, cleared after each upload
"""
import sys
import util
from mcm_upload_util import Upload, FileRetrival, DataManaging

import argparse


class Metadata:
  # parse tsv

  metadata_to_field = {
    "Identifier"                 : "identifier",
    "Title"                      : "title",
    "Content"                    : "content",
    "Content URL"                : "content_url",
    "Content URL (Audio)"        : "content_url_audio",
    "Content URL (Transcript)": "content_url_transcript",
    "Creator"                    : "creator",
    "Creator.Other"              : "creator_other",
    "Subject.Place"              : "subject_place",
    "Coverage.Lat"               : "coverage_lat",
    "Coverage.Long"              : "coverage_long",
    "Subject.Associated.Places"  : "subject_associated_places",
    "Subject.People"             : "subject_people",
    "Subject.Academic.Field"     : "subject_academic_field",
    "Subject.Other"              : "subject_other",
    "Subject.Season"             : "subject_season",
    "Date.Season"                : "date_season",
    "Date.Season (YYYY)"         : "date_season_yyyy",
    "Date.Exact"                 : "date_exact",
    "Date.Digital"               : "date_digital",
    "Description"                : "description",
    "Format"                     : "format",
    "Digitization Specifications": "digitization_specifications",
    "Contributor"                : "contributor",
    "Type"                       : "type",
    "Country"                    : "country",
    "Language"                   : "language",
    "Relation"                   : "relation",
    "Source"                     : "source",
    "Publisher"                  : "publisher",
    "Publisher Location"         : "publisher_location",
    "Bibliographic Citation"     : "bibliographic_citation",
    "Rights"                     : "rights"
  }

  default_tsv_template_url = "https://docs.google.com/spreadsheets/d/1lTNeLTV3vV4BwzsbmODQXwkaC_vqg-eFelRfYEloB00/edit#gid=0"

  def __init__(self, my_args):
    self.file_downloads = FileRetrival()
    self.data_managing = DataManaging()
    self.tsv_file_content_list = []
    self.tsv_file_content_dict = {}

    (input_file, delimiter) = self.url_or_dest(my_args)
    self.get_data_from_tsv(input_file, delimiter)
    self.tsv_file_fields = self.tsv_file_content_list[0]
    self.transposed_vals = list(map(list, zip(*self.tsv_file_content_list[1])))

    self.not_empty_tsv_content_dict = self.check_for_empty_fields()

    self.not_empty_tsv_content_dict = self.change_keys_in_tsv_content_dict_clean_custom(
      self.not_empty_tsv_content_dict)
    self.tsv_file_fields = list(self.not_empty_tsv_content_dict.keys())

    self.tsv_file_content_dict_no_empty = self.format_not_empty_dict()
    self.check_for_empty_keys()

    self.tsv_file_content_dict_ok = self.clean_keys_in_tsv_file_content_dict()

    self.add_missing_fields()
    self.add_missing_identifier()
    # print("STOP")

  def add_missing_identifier(self):
    for idx, d in enumerate(self.tsv_file_content_dict_ok):
      if not d[self.data_managing.identifier_table_name]:
        type = d['type']
        identifiers_from_tsv = self.not_empty_tsv_content_dict[self.data_managing.identifier_table_name]
        (db_id, curr_identifier) = self.data_managing.check_or_create_identifier(type, identifiers_from_tsv)
        d[self.data_managing.identifier_table_name] = curr_identifier
        self.not_empty_tsv_content_dict[self.data_managing.identifier_table_name][idx] = curr_identifier

  def get_google_file_id_from_url(self, url):
    # 'https://docs.google.com/spreadsheets/d/1CW0f2tVWAy6-ZH6h5cnHTlkYmVKFN-79pqPve7PMkUc/edit#gid=1112829154'
    try:
      google_file = url.split('spreadsheets/d')[1].split('/')[1]
      return google_file
    except IndexError:
      print("Please provide a valid google spreadsheet url")
      sys.exit()

    # '1CW0f2tVWAy6-ZH6h5cnHTlkYmVKFN-79pqPve7PMkUc'
    """'https://docs.google.com/spreadsheets/d/1CW0f2tVWAy6-ZH6h5cnHTlkYmVKFN-79pqPve7PMkUc/edit#gid=1112829154'.split('spreadsheets/d', 1)
    {list: 2} 
      0 = {str} 'https://docs.google.com/'
      1 = {str} '/1CW0f2tVWAy6-ZH6h5cnHTlkYmVKFN-79pqPve7PMkUc/edit#gid=1112829154'
    """

  def url_or_dest(self, args):
    if args.input_file:
      input_file_name = args.input_file
      delimiter = "\t"
    else:
      # if not args.input_file and not args.input_file_url:
      input_url = self.default_tsv_template_url
      # utils.print_both("The default google spreadsheet will be used.")
      if args.input_file_url:
        input_url = args.input_file_url
      delimiter = ","
      file_id = self.get_google_file_id_from_url(input_url)
      output_format = "csv"
      doc_url = 'https://docs.google.com/spreadsheet/ccc?key={}&output={}'.format(file_id, output_format)

      # doc_url = 'https://docs.google.com/spreadsheet/ccc?key=1CW0f2tVWAy6-ZH6h5cnHTlkYmVKFN-79pqPve7PMkUc&output=tsv'

      input_file_name = self.file_downloads.download_file(doc_url, file_id)
    return (input_file_name, delimiter)

  def add_missing_fields(self):
    missing_fields = utils.subtraction(self.metadata_to_field.values(), self.tsv_file_fields)
    for curr_d in self.tsv_file_content_dict_ok:
      for f in missing_fields:
        curr_d[f] = ""

  def clean_keys_in_tsv_file_content_dict(self):
    res_d = []
    for curr_d in self.tsv_file_content_dict:
      clean_d = self.change_keys_in_tsv_content_dict_clean_custom(curr_d)
      res_d.append(clean_d)
    return res_d

  def check_for_empty_keys(self):
    all_fields = self.tsv_file_content_list[0]
    if "" in all_fields:
      utils.print_both("ERROR: Column (field names) shouldn't be empty!")
      sys.exit()

  def get_data_from_tsv(self, input_file, delimiter= "\t"):
    self.tsv_file_content_list = utils.read_csv_into_list(input_file, delimiter)
    self.tsv_file_content_dict = utils.read_csv_into_dict(input_file, delimiter)

  def format_not_empty_dict(self):
    temp_list_of_dict = []
    keys = list(self.not_empty_tsv_content_dict.keys())
    transposed_values = list(map(list, zip(*self.not_empty_tsv_content_dict.values())))
    for line in transposed_values:
      temp_dict = {}
      for idx, v in enumerate(line):
        key = keys[idx]
        temp_dict[key] = v
      temp_list_of_dict.append(temp_dict)
    return temp_list_of_dict

  def check_for_empty_fields(self):
    removed_fields = []
    clean_matrix = []
    good_fields = []
    for idx, vals_l in enumerate(self.transposed_vals):
      all_val_for1_field = set(vals_l)
      field_name = self.tsv_file_fields[idx]
      if any(all_val_for1_field):
        good_fields.append(field_name)
        clean_matrix.append(vals_l)
      else:
        removed_fields.append(field_name)
    not_empty_tsv_content_dict = dict(zip(good_fields, clean_matrix)) or {}

    return not_empty_tsv_content_dict

  def change_keys_in_tsv_content_dict_clean_custom(self, my_dict):
    return {field_name.replace(".", "_").replace(" ", "_").replace("(", "").replace(")", "").lower(): val
            for field_name, val in my_dict.items()}


class DownloadFilesFromDropbox(FileRetrival):
  def __init__(self, metadata):
    FileRetrival.__init__(self, metadata)
    # TODO: add args quiet to supress the counter
    self.download_all_from_content_url()

    utils.print_both("END of FileRetrival = DownloadFilesFromDropbox")


class UploadMetadata(Upload):
  def __init__(self, my_metadata):
    Upload.__init__(self, my_metadata)
    self.drop_temp_table()
    self.create_temp_table()

    self.upload_simple_tables()
    print("=== upload_all_from_tsv_into_temp_table ===")
    self.upload_all_from_tsv_into_temp_table()
    self.mass_update_simple_ids()

    self.upload_many_values_to_one_field()
    self.update_many_values_to_one_field_ids()

    print("=== Upload entries ===")
    self.upload_other_tables()

    utils.print_both("END of metadata upload")


if __name__ == '__main__':

  utils = util.Utils()
  myusage = """
      By default (no arguments) will upload data from "mcmurdohistory_metadata template" (https://docs.google.com/spreadsheets/d/1lTNeLTV3vV4BwzsbmODQXwkaC_vqg-eFelRfYEloB00/edit#gid=0) into the database.
      
      If a tab separated file provided it will be uploaded into the database instead.
      Command line example: python3 %(prog)s -f Interviews.tsv

  """
  parser = argparse.ArgumentParser(description = myusage)
  # parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
                      required = False, action = 'store', dest = 'input_file',
                      help = '''Input tsv file name''')
  parser.add_argument('-u', '--url',
                      required = False, action = 'store', dest = 'input_file_url',
                      help = '''Input file URL (on Google docs)''')
  parser.add_argument('-nd', '--no_dropbox_download',
                      required = False, action = 'store_true', dest = 'no_dropbox_download',
                      help = '''Do not download Dropbox files from "Content URL..." columns.''')
  # parser.add_argument("-ve", "--verbatim",
  #                     required = False, action = "store_true", dest = "is_verbatim",
  #                     help = """Print an additional information""")
  # self.download_file(url)

  args = parser.parse_args()
  # if not args.input_file and not args.input_file_url:
  #   default_tsv_template_url = "https://docs.google.com/spreadsheets/d/1lTNeLTV3vV4BwzsbmODQXwkaC_vqg-eFelRfYEloB00/edit#gid=0"
  #   print("Please provide a tsv file name or its URL on Google docs")
  #   sys.exit()

  utils.print_both('args = ')
  utils.print_both(args)

  # is_verbatim = args.is_verbatim

  metadata = Metadata(args)
  if not args.no_dropbox_download:
    file_from_url = DownloadFilesFromDropbox(metadata)
  upload_metadata = UploadMetadata(metadata)

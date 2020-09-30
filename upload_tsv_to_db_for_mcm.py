#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
*) upload the whole csv into one table, separate, add ids
*) whole_tsv_dump is temporary, cleared after each upload
"""
import sys
import util
from mcm_upload_util import Upload, File_retrival

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

  def __init__(self, args):
    self.tsv_file_content_list = []
    self.tsv_file_content_dict = {}

    input_file = self.url_or_dest(args)
    self.get_data_from_tsv(input_file)
    self.tsv_file_fields = self.tsv_file_content_list[0]
    self.transposed_vals = list(map(list, zip(*self.tsv_file_content_list[1])))

    self.not_empty_tsv_content_dict = self.check_for_empty_fields()

    self.not_empty_tsv_content_dict = self.change_keys_in_tsv_content_dict_clean_custom(
      self.not_empty_tsv_content_dict)
    self.tsv_file_fields = list(self.not_empty_tsv_content_dict.keys())

    self.tsv_file_content_dict_no_empty = self.format_not_empty_dict()
    self.check_for_empty_keys()

    self.tsv_file_content_dict_clean_keys = self.clean_keys_in_tsv_file_content_dict()

    self.add_missing_fields()

  def url_or_dest(self, args):
    input = args.input_file
    if args.input_file_url:
      input = args.input_file_url

  def add_missing_fields(self):
    missing_fields = utils.subtraction(self.metadata_to_field.values(), self.tsv_file_fields)
    for curr_d in self.tsv_file_content_dict_clean_keys:
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

  def get_data_from_tsv(self, input_file):
    self.tsv_file_content_list = utils.read_tsv_into_list(input_file, "\t")
    self.tsv_file_content_dict = utils.read_tsv_into_dict(input_file, "\t")

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


class DownloadFilesFromDropbox(File_retrival):
  def __init__(self, metadata):
    File_retrival.__init__(self, metadata)
    self.download_all()

    utils.print_both("END of File_retrival = DownloadFilesFromDropbox")


class UploadMetadata(Upload):
  def __init__(self, metadata):
    Upload.__init__(self, metadata)
    self.drop_temp_table()
    self.create_temp_table()

    self.upload_simple_tables()
    self.upload_all_from_tsv_into_temp_table()
    self.mass_update_simple_ids()

    self.upload_many_values_to_one_field()
    self.update_many_values_to_one_field_ids()

    self.upload_other_tables()

    utils.print_both("END of metadata upload")


if __name__ == '__main__':

  utils = util.Utils()

  parser = argparse.ArgumentParser()

  parser.add_argument('-f', '--file_name',
                      required = False, action = 'store', dest = 'input_file',
                      help = '''Input file name''')
  parser.add_argument('-u', '--url',
                      required = False, action = 'store', dest = 'input_file_url',
                      help = '''Input file URL (on Google docs)''')
  parser.add_argument("-ve", "--verbatim",
                      required = False, action = "store_true", dest = "is_verbatim",
                      help = """Print an additional information""")
  # self.download_file(url)

  args = parser.parse_args()
  if not args.input_file and not args.input_file_url:
    print("Please provide a tsv file name or its URL on Google docs")
    sys.exit()

  print('args = ')
  print(args)

  is_verbatim = args.is_verbatim

  metadata = Metadata(args)
  upload_metadata = Upload_metadata(metadata)


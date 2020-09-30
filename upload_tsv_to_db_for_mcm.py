#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
TODO: add type as a required parameter (photo etc)
*) upload the whole csv into one table, separate, add ids
*) whole_tsv_dump should be temporary, clear after each upload
"""
import sys
import util
from mcm_upload_util import Upload, File_retrival


# try:
#   import mysqlclient as mysql
# except ImportError:
#   try:
#     import pymysql as mysql
#   except ImportError:
#     import MySQLdb as mysql

import argparse
from collections import defaultdict


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

    # print("self.tsv_file_content_dict")
    # return missing_fields_correct_names
      # name_w_id = field_name_no_id + "_id"
      # sql_res_d[name_no_id] = self.select_empty_id(name_w_id, field_name_no_id)
      # Upload.select_empty_id(name_w_id, field_name_no_id)

  def clean_keys_in_tsv_file_content_dict(self):
    res_d = []
    for curr_d in self.tsv_file_content_dict:
      clean_d = self.change_keys_in_tsv_content_dict_clean_custom(curr_d)
      res_d.append(clean_d)
    return res_d

  def check_for_empty_keys(self):
    all_fields = self.tsv_file_content_list[0]
    if "" in all_fields:
      print("ERROR: Column (field names) shouldn't be empty!")
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

class download_files_from_dropbox(File_retrival):
  def __init__(self, metadata):
    File_retrival.__init__(self, metadata)
    self.download_all()

    print("END of File_retrival = download_files_from_dropbox")


class Upload_metadata(Upload):
  def __init__(self, metadata):
    Upload.__init__(self, metadata)
    # self.mysql_utils = Upload.mysql_utils
    self.drop_temp_table()
    self.create_temp_table()

    # self.upload_empty()
    self.upload_simple_tables()
    self.upload_all_from_tsv_into_temp_table()
    self.mass_update_simple_ids()

    self.upload_many_values_to_one_field()
    self.update_many_values_to_one_field_ids()

    self.upload_other_tables()

    print("END of metadata upload")


# class File_retrival:
#   def __init__(self):
#     self.download_all()
#     # url = 'https://www.facebook.com/favicon.ico'
#     # r = requests.get(url, allow_redirects=True)
#     # if url.find('/'):
#     #   print(url.rsplit('/', 1)[1])
#     #
#     # print(r.headers.get('content-type'))
#     # print(r.apparent_encoding)
#
#     # if self.is_downloadable(url):
#     #   open('facebook.ico', 'wb').write(r.content)
#
#   def download_from_dropbox(self):
#     import dropbox
#     acc_token = "sl.Aik6Wa8t_-q5lEqrDDNH2rpx1XNJhYjAVKJCcbay03Pp3Lo_HoOLBiOT-iDJWQ3bKHM-1xe_adPkJjJIvnWlGKq8hSaDHRGF90XWhr0kaW2Q3s4bE-fQ7odiWs1lCFfyv5YGhvA"
#     dbx = dropbox.Dropbox(acc_token)
#     for entry in dbx.files_list_folder('').entries:
#       print(entry.name)
#
#     # with open("Prime_Numbers.txt", "wb") as f:
#     #   metadata, res = dbx.files_download(path = "/Homework/math/Prime_Numbers.txt")
#     #   f.write(res.content)
#
#   def get_current_urls(self, entry_d):
#     url_fields = ['content_url', 'content_url_audio', 'content_url_transcript']
#     urls = []
#     for url_field in url_fields:
#       try:
#         url = entry_d[url_field]
#         if url and len(url) > 0:
#           urls.append(url)
#       except KeyError:
#         pass
#     return urls
#
#   def change_dl(self, urls):
#     return [url.replace('?dl=0', '?dl=1', 1) for url in urls]
#     # for url in urls:
#     #   url.replace('?dl=0', '?dl=1', 1)
#
#   def download_all(self):
#     url_fields = ['content_url', 'content_url_audio', 'content_url_transcript']
#     for entry_d in metadata.tsv_file_content_dict_no_empty:
#       urls = self.get_current_urls(entry_d)
#       urls = self.change_dl(urls)
#       for url in urls:
#         # file_name = self.get_file_name(url)
#         # print(url)
#         self.download_file(url)
#
#   def get_file_name(self, url):
#     # TODO: add server's path, get name if no /
#     file_name = ""
#     path = "/Users/ashipunova/work/MCM"
#     if url.find('/'):
#       file_name = url.rsplit('/', 1)[1].split('?', 1)[0]
#     return os.path.join(path, file_name)
#
#   def download_file(self, url):
#     r = requests.get(url, allow_redirects=True)
#     file_name = self.get_file_name(url)
#     open(file_name, 'wb').write(r.content)
#
#   def is_downloadable(self, url):
#     """
#     https://aviaryan.com/blog/gsoc/downloading-files-from-urls
#     Does the url contain a downloadable resource
#     """
#     h = requests.head(url, allow_redirects = True)
#     header = h.headers
#     content_type = header.get('content-type')
#     if 'text' in content_type.lower():
#       return False
#     if 'html' in content_type.lower():
#       return False
#
#     content_length = header.get('content-length', None)
#     if content_length and content_length > 2e8:  # 200 mb approx
#       return False
#
#     return True


if __name__ == '__main__':
  # /Users/ashipunova/work/MCM/mysql_schema/Bibliography_test.tsv

  utils = util.Utils()

  # if utils.is_local():
  #   db_schema = 'mcm_history'
  #   mysql_utils = util.Mysql_util(host = 'localhost', db = db_schema, read_default_group = 'clienthome')
  #   print("host = 'localhost', db = {}".format(db_schema))
  # else:
  #   db_schema = 'mcmurdohistory_metadata'
  #   host = '127.0.0.1'
  #   mysql_utils = util.Mysql_util(host = host, db = db_schema, read_default_group = 'client')
  #   # mysql_utils = util.Mysql_util(host = 'taylor.unm.edu', db = db_schema, read_default_group = 'client')
  #   print("host = {}, db {}".format(host, db_schema))

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

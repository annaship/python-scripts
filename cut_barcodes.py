#! /usr/bin/env python

import IlluminaUtils.lib.fastqlib as fq
import os
import sys
import argparse
# from argparse import RawTextHelpFormatter

def get_files(walk_dir_name, ext = ""):
    files = {}
    filenames = []
    for dirname, dirnames, filenames in os.walk(walk_dir_name, followlinks=True):
        if ext:
            filenames = [f for f in filenames if f.endswith(ext)]
        
        for file_name in filenames:
            full_name = os.path.join(dirname, file_name)
            (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
            files[full_name] = (dirname, file_base, file_extension)
    return files

def parse_args():

    parser = argparse.ArgumentParser(description = """Cuts the first 5 characters from sequences and quality lines.
Input: gzipped fastq files.
Output: the new shortened fastq entries and a log file with original file name and the cut 5nt sequences.""", formatter_class = argparse.RawTextHelpFormatter)

    parser.add_argument('-d', '--dir_name',
                        required = True, action = 'store', dest = 'start_dir',
                        help = """Start directory name""")
    parser.add_argument("-ve", "--verbatim",
                        required = False, action = "store_true", dest = "is_verbatim",
                        help = """Print an additional information""")
    parser.add_argument("-e", "--extension",
                        required = False, action = "store", dest = "extension",
                        help = """File(s) extension""")
                        

    args = parser.parse_args()
    print('args = ')
    print(args)
    return args

def go_trhough_fastq():
    barcode_log = set()

    for file_name in fq_files:
        if (is_verbatim):
            print(file_name)

        try:
            f_input = fq.FastQSource(file_name, True)
            f_output = fq.FastQOutput(file_name + ".out")
            while f_input.next(raw = True):
                e = f_input.entry
                barcode_log.add("%s: %s\n" % (file_name, e.sequence[0:5]))
                cut_barcodes(e, f_output)

        except RuntimeError:
            if (is_verbatim):
                print(sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info())
            print("Check if there are no '.out' files and remove if any.")
            next

    print_barcode_log(barcode_log)


def cut_barcodes(e, f_output):
    e.sequence = e.sequence[5:]
    e.qual_scores = e.qual_scores[5:]
    f_output.store_entry(e)

def print_barcode_log(barcode_log):
    log_f_name = "barcode_files.log"
    log_f = open(log_f_name, "w")
    to_print = "".join(list(barcode_log))
    log_f.write(str(to_print))

if __name__ == '__main__':

    args = parse_args()

    is_verbatim = args.is_verbatim

    start_dir = args.start_dir
    print("Start from %s" % start_dir)

    # min = a if a < b else b

    ext = args.extension if args.extension else "test4_2.fastq.gz"

    print("Getting file names")
    fq_files = get_files(start_dir, ext)
    print("Found %s fastq.gz files" % (len(fq_files)))

    go_trhough_fastq()
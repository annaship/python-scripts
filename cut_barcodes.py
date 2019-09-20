import IlluminaUtils.lib.fastqlib as fq
import os
import sys
import argparse

def get_files(walk_dir_name, ext = ""):
    files = {}
    filenames = []
    for dirname, dirnames, filenames in os.walk(walk_dir_name, followlinks = True):
        if ext:
            filenames = [f for f in filenames if f.endswith(ext)]

        for file_name in filenames:
            full_name = os.path.join(dirname, file_name)
            (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
            files[full_name] = (dirname, file_base, file_extension)
    return files

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir_name',
                        required = True, action = 'store', dest = 'start_dir',
                        help = """Start directory name""")
    parser.add_argument("-ve", "--verbatim",
                        required = False, action = "store_true", dest = "is_verbatim",
                        help = """Print an additional information""")

    args = parser.parse_args()
    print('args = ')
    print(args)
    return args

def go_trhough_fastq():
    for file_name in fq_files:
        if (is_verbatim):
            print(file_name)

        try:
            f_input = fq.FastQSource(file_name, True)
            f_output = fq.FastQOutput(file_name + ".out")
            while f_input.next(raw = True):
                e = f_input.entry
                cut_barcodes(e, f_output)
                print_barcode_log(e, file_name)

        except RuntimeError:
            if (is_verbatim):
                print(sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info())
            print("Check if there are no '.out' files and remove if any.")
            next

def cut_barcodes(e, f_output):
    e.sequence = e.sequence[5:]
    e.qual_scores = e.qual_scores[5:]
    f_output.store_entry(e)

def print_barcode_log(e, file_name):
    log_f_name = "barcode_files.log"
    log_f = open(log_f_name, "a")
    log_f.write("%s: %s\n" % (file_name, e.sequence[0:5]))


if __name__ == '__main__':

    args = parse_args()

    is_verbatim = args.is_verbatim

    start_dir = args.start_dir
    print("Start from %s" % start_dir)
    print("Getting file names")
    fq_files = get_files(start_dir, ".fastq.gz")
    print("Found %s fastq.gz files" % (len(fq_files)))

    go_trhough_fastq()
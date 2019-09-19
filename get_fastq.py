import IlluminaUtils.lib.fastqlib as fq
import os
import sys

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

def check_if_verb():
  try: 
    if sys.argv[2] == "-v":
      return True
  except IndexError:
    return False
  except: 
    print("Unexpected error:", sys.exc_info()[0])
    return False
  return False

def check_len(e, file_name):
    seq_len = len(e.sequence)
    qual_scores_len = len(e.qual_scores)
    # print(e.header_line)
    if (seq_len != qual_scores_len):
        print("WARNING, sequence and qual_scores_line have different length in %s" % file_name)
        all_dirs.add(fq_files[file_name][0])

def cut_barcode(e):
    e.qual_scores = e.qual_scores[5:]
    e.sequence = e.sequence[5:]
    return e


def add_to_output_log(barcode, file_name):
    log_entry = "%s: %s\n" % (file_name, barcode)

if __name__ == '__main__':

    start_dir = sys.argv[1]
    print("Start from %s" % start_dir)
    print("Getting file names")

    all_dirs = set()

    fq_files = get_files(start_dir, ".fastq.gz")
    print("Found %s fastq.gz files" % (len(fq_files)))

    check_if_verb = check_if_verb()

    out_f_name = "barcode_file.txt"
    out_file = open(out_f_name, "w")

    for file_name in fq_files:
      if (check_if_verb):
        print(file_name)

      try:
        f_input  = fq.FastQSource(file_name, True)
        f_output = fq.FastQOutput(file_name + ".out")

        while f_input.next():
          f_input.next()
          e = f_input.entry
          check_len(e, file_name)
          barcode = e.sequence[0:4]
          new_e = cut_barcode(e)
          f_output.store_entry(new_e)

          add_to_output_log(barcode, file_name)
      except RuntimeError:
        if (check_if_verb):
          print(sys.exc_info()[0])
      except:
        print("Unexpected error:", sys.exc_info()[0])
        next

    print(all_dirs)



import IlluminaUtils.lib.fastalib as fa
import os
import sys

usage = """python count_seq_len_fa.py DIRNAME [-ve]"""

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
    if sys.argv[2] == "-ve":
      return True
  except IndexError:
    return False
  except: 
    print "Unexpected error:", sys.exc_info()[0]
    return False
  return False


start_dir = sys.argv[1]
print "Start from %s" % start_dir
print "Getting file names"

all_dirs = set()

#fa_files = get_files("/xraid2-2/sequencing/Illumina", ".fastq.gz")
# "/xraid2-2/sequencing/Illumina/20151014ns"
fa_files = get_files(start_dir, ".fa")
print "Found %s fa files" % (len(fa_files))

check_if_verb = check_if_verb()

for file_name in fa_files:
  if (check_if_verb):
    print file_name

  try:
    f_input  = fa.ReadFasta(file_name)
    
    for idx, seq in enumerate(f_input.sequences):
      seq_len = len(seq)
      if seq_len < 200:
        print f_input.ids[idx]
        print seq
        print "WARNING, sequence length in %s = %s. It's less than 200!" % (file_name, seq_len)
        all_dirs.add(fa_files[file_name][0])
  except RuntimeError:
    if (check_if_verb):
      print sys.exc_info()[0]
  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
    next

print "Current directory:"
print all_dirs



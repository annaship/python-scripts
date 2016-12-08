import IlluminaUtils.lib.fastqlib as fq
import os
import sys

def open_write_close(file_name, text):
    file = open(file_name, "w")
    file.write(text)
    file.close()
    
def check_if_verb():
  try: 
    if sys.argv[2] == "-v":
      return True
  except IndexError:
    return False
  except: 
    print "Unexpected error:", sys.exc_info()[0]
    return False
  return False


in_file_name = sys.argv[1]
good_runkey = ["ACGCA", "CGCTC", "CTAGC", "GACTC", "GAGAC", "GTATC", "TCAGC"]
text = ""

input  = fq.FastQSource(in_file_name, compressed = True)
output = fq.FastQOutput('unknown_good_runkey.fastq')

while input.next(trim_to = 251):
    # print input.entry.sequence[4:9]
    if input.entry.sequence[4:9] in good_runkey and input.entry.Q_mean > 20:
        # print input.entry.header_line
        # print "input.entry.sequence[4:9] in good_runkey = %s" % (input.entry.sequence[4:9] in good_runkey)
        # print "input.entry.sequence[4:9] = %s in good_runkey" % (input.entry.sequence[4:9])
        
        output.store_entry(input.entry)

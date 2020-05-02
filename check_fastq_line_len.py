import IlluminaUtils.lib.fastqlib as fq
import os
import sys

class Files():
    def __init__(self, args):
        pass
        
class Reads():
    def __init__(self, args):
        self.compressed  = args.compressed
        if args.ext is None and self.compressed == True:
            self.ext     = "1_R1.fastq.gz"
        elif args.ext is not None:
            self.ext     = args.ext
        else:
            self.ext     = "1_R1.fastq"
        print "extension = %s" % self.ext
        self.start_dir   = args.start_dir
        self.quality_len = args.quality_len
        self.verbatim    = args.verbatim
        print "Start from %s" % self.start_dir

    def get_files(self):
        files = {}
        filenames = []
        for dirname, dirnames, filenames in os.walk(self.start_dir, followlinks=True):
            if self.ext:
                filenames = [f for f in filenames if f.endswith(self.ext)]

            for file_name in filenames:
                full_name = os.path.join(dirname, file_name)
                (file_base, file_extension) = os.path.splitext(os.path.join(dirname, file_name))
                files[full_name] = (dirname, file_base, file_extension)
        return files

    def check_if_verb(self):
      try:
        if self.verbatim:
          return True
      except IndexError:
        return False
      except:
        raise
        # print "Unexpected error:", sys.exc_info()[0]
        # return False
      return False

    def compare_w_score(self, f_input, file_name, all_dirs):
      for _ in range(50):
        f_input.next(raw = True)
        e = f_input.entry
        
        seq_len = len(e.sequence)
        qual_scores_len = len(e.qual_scores)
        try:
            if self.quality_len:
                print "\n=======\nCOMPARE_W_SCORE"
                print "seq_len = %s" % (seq_len)
                print "qual_scores_len = %s" % (qual_scores_len)
        except IndexError:
            pass
        except:
            raise
        # print e.header_line
        if (seq_len != qual_scores_len):
          print "WARNING, sequence and qual_scores_line have different length in %s for %s" % (file_name, e.header_line)
          print "seq_len = %s" % (seq_len)
          print "qual_scores_len = %s" % (qual_scores_len)
          
          all_dirs.add(fq_files[file_name][0])


    def get_seq_len(self, f_input, file_name, all_dirs):
      seq_lens = []
      for _ in range(50):
        f_input.next(raw = True)
        e = f_input.entry
        seq_len = len(e.sequence)
        seq_lens.append(seq_len)
        # print seq_len
      print "sorted seq_lens:"
      print sorted(set(seq_lens))



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='''Check fastq files reads and quality lines length.
    Command line example: python %(prog)s -d/--dir DIRNAME -e/--extension -v --compressed/-c
    ''')
    # todo: add user_config
    # parser.add_argument('--user_config', metavar = 'CONFIG_FILE',
    #                                     help = 'User configuration to run')
    parser.add_argument('--dir', '-d', required = True, action='store', dest='start_dir',
                        help = 'A start directory path.')
    parser.add_argument('--extension', '-e', required = False, action='store', dest='ext',
                        help = 'An extension to look for. Default is a "1_R1.fastq".')
    parser.add_argument('--compressed', '-c', action = "store_true", default = False,
                        help = 'Use if fastq compressed. Default is a %(default)s.')
    parser.add_argument('--quality_len', '-q', action = "store_true", default = False,
                        help = 'Print out the quality and read length. Default is a %(default)s.')
    parser.add_argument('--verbatim', '-v', action = "store_true", default = False,
                        help = 'Print outs.')

    args = parser.parse_args()
    print args

    reads = Reads(args)
    if not os.path.exists(args.start_dir):
        # try:
        print "Input fastq file with the '%s' extension does not exist in %s" % (reads.ext, reads.start_dir)
        # except AttributeError:
        #     print "Input fastq file with a '%s' extension does not exist in ." % (args.ext)
        sys.exit()

    all_dirs = set()

    #fq_files = get_files("/xraid2-2/sequencing/Illumina", ".fastq.gz")
    # "/xraid2-2/sequencing/Illumina/20151014ns"
    print "Getting file names"
    fq_files = reads.get_files()
    print "Found %s %s" % (len(fq_files), reads.ext)

    check_if_verb = reads.check_if_verb()

    for file_name in fq_files:
      if (check_if_verb):
        print file_name

      try:
        f_input  = fq.FastQSource(file_name, args.compressed)
        reads.compare_w_score(f_input, file_name, all_dirs)
        reads.get_seq_len(f_input, file_name, all_dirs)
      except RuntimeError:
        if (check_if_verb):
          print sys.exc_info()[0]
      except:
        raise
        # print "Unexpected error:", sys.exc_info()[0]
        # next

    print "Directories: %s" % all_dirs
    
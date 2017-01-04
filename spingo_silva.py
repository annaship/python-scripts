#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

class Taxonomy:
    def __init__(self):
        output_text = {}

    """
    time head -2 silva.all1.tax_fa | sed 's/^/>/' | sed 's/\t#\t/\n/' | tr "\t" ";" | awk 'BEGIN {FS=";"; OFS="\t"}  {if ($0 ~ /^>/) print $1, $(NF-1)"_" $NF, $(NF-1), "NA", $(NF-2); else print}'
    """
    
    def fill_out_empty_ranks(self, taxon_split):
        for i in range(8):
            try:
                print "III = %s" % (i)
                if not taxon_split[i]:
                    # taxon_split[i] = "NA"
                    print "not taxon_split[i]"
                    print taxon_split[i]
            except IndexError:
                taxon_split.append("NA")
                
                pass
                # taxon_split[i+1] = "NA"
            except:
                raise
        
    
    def format_header(self, header):
        # print header
        # AF251436.1.1466   Bacteria;Actinobacteria;Acidimicrobiia;Acidimicrobiales;Acidimicrobiaceae;Ferrimicrobium;acidiphilum
        
        id, taxon = header.split("\t")
        # print id
        # print taxon
        
        taxon_split = taxon.split(";")
        print len(taxon_split)
            
        self.fill_out_empty_ranks(taxon_split)    

        for i in reversed(taxon_split):
            print i

    def parse_taxonomy(self, filename):
      with open(filename, "r") as infile:
          for line in infile:
              # current_output_text = ""
              line = line.strip()
              if not line: continue #Skip empty
              # print line
              header, sequence = line.split("\t#\t")
              # current_output_text = ">" + line.replace("\t#\t", "\n")
              # print header
              # print sequence
              self.format_header(header)
          
              # JQ817537.1.1383 Archaea #   A
          #     if line == "[Term]":
          #         if currentGOTerm: yield processGOTerm(currentGOTerm)
          #         currentGOTerm = defaultdict(list)
          #     elif line == "[Typedef]":
          #         #Skip [Typedef sections]
          #         currentGOTerm = None
          #     else: #Not [Term]
          #         #Only process if we're inside a [Term] environment
          #         if currentGOTerm is None: continue
          #         key, sep, val = line.partition(":")
          #         currentGOTerm[key].append(val.strip())
          # #Add last term
          # if currentGOTerm is not None:
          #     yield processGOTerm(currentGOTerm)


if __name__ == '__main__':


    taxonomy = Taxonomy()
    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(description='''Demultiplex Illumina fastq. Will make fastq files per barcode from "in_barcode_file_name".
    # Command line example: time python demultiplex_use.py --in_barcode_file_name "prep_template.txt" --in_fastq_file_name S1_L001_R1_001.fastq.gz --out_dir results --compressed
    # 
    # ''')
    # todo: add user_config
    # parser.add_argument('--user_config', metavar = 'CONFIG_FILE',
    #                                     help = 'User configuration to run')
    # parser.add_argument('--in_barcode_file_name', required = True,
    #                                     help = 'Comma delimited file with sample names in the first column and its barcodes in the second.')
    # 


    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")

    args = parser.parse_args()
    print "args = "
    print args

    
    taxonomy.parse_taxonomy(args.input_file)
    
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

class Taxonomy:
    def __init__(self):
        output_text = {}
        ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]

    """
    time head -2 silva.all1.tax_fa | sed 's/^/>/' | sed 's/\t#\t/\n/' | tr "\t" ";" | awk 'BEGIN {FS=";"; OFS="\t"}  {if ($0 ~ /^>/) print $1, $(NF-1)"_" $NF, $(NF-1), "NA", $(NF-2); else print}'
    """
    
    def fill_out_empty_ranks(self, taxon_split):
        return [taxon_split.append("NA") for i in range(8) if (len(taxon_split) < i+1)]

    def get_binomial(self, taxon_split):
        try:
            return taxon_split[5] + "_" + taxon_split[6]
        except IndexError:
            return "NA"
        except:
            raise

    def get_genus(self, taxon_split):
        try:
            return taxon_split[5]
        except IndexError:
            return "NA"
        except:
            raise
        
    
    def format_header(self, header):
        # print header
        # AF251436.1.1466   Bacteria;Actinobacteria;Acidimicrobiia;Acidimicrobiales;Acidimicrobiaceae;Ferrimicrobium;acidiphilum
        # goal:
        # >S001014081   Ilumatobacter_fluminis  Ilumatobacter   NA  Acidimicrobiaceae
        
        id, taxon = header.split("\t")
        # print id
        # print taxon
        
        taxon_split = taxon.split(";")
        # print len(taxon_split)

        binomial = self.get_binomial(taxon_split)
        # print "binomial = %s" % binomial
        
        genus = self.get_genus(taxon_split)            
        # print "genus = %s" % genus
            
        self.fill_out_empty_ranks(taxon_split)

        # print taxon_split[:5]
        
        reverse_from_family = [i for i in reversed(taxon_split[:5])]

        return ">" + id + "\t" + binomial + "\t" + genus + "\tNA\t" + "\t".join(reverse_from_family)

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
                out_header = self.format_header(header)
                print out_header
                print sequence




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
    parser.add_argument("-r", "--rank",
        required = True, action = "store", dest = "rank_level",
        help = """The highest taxonomic rank""")

    args = parser.parse_args()
    # print "args = "
    # print args

    
    taxonomy.parse_taxonomy(args.input_file)
    
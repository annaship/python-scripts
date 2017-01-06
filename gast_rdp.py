#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

class Taxonomy:
    """
    From
    >S000655540 uncultured bacterium; L2Sp-13	Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ilumatobacter;genus
    to
    AAAA02010377.14668.16277        Bacteria;Proteobacteria;Alphaproteobacteria;Rickettsiales       1
    
    """
    def __init__(self):
        pass        

    def format_header(self, header):
        pass

    def parse_taxonomy(self, args):
        filename = args.input_file
        with open(filename, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line: continue #Skip empty
                print line
                header, taxon_string = line.split("\t")
                print "header"
                print header
                print "sequence"
                print sequence
                
                # out_header = self.format_header(header)
                # print out_header
                # print sequence


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
    # parser.add_argument("-r", "--rank",
    #     required = False, action = "store", dest = "rank_level", default = 'domain',
    #     help = """The highest taxonomic rank (one of %s)""" % ", ".join(ranks))

    args = parser.parse_args()
    # print "args = "
    # print args

    
    taxonomy.parse_taxonomy(args)
    
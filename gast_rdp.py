#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import gzip

class Taxonomy:
    """
    From release11_2_Bacteria_unaligned.fa.gz
    >S000655540 uncultured bacterium; L2Sp-13	Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ilumatobacter;genus
    to silva.tax
    AAAA02010377.14668.16277        Bacteria;Proteobacteria;Alphaproteobacteria;Rickettsiales       1

    """
    def __init__(self):
        self.parsed_line = {}

    def parse_header(self, header):
        # print "header"
        # print header
        id = header.split(" ")[0]
        try:
            self.parsed_line[id]["binomial_plus"] = " ".join(header.split(" ")[1:]).replace("; ", ";")
        except KeyError:
            self.parsed_line[id] = {}
            self.parsed_line[id]["binomial_plus"] = " ".join(header.split(" ")[1:]).replace("; ", ";")
        except:
            raise
        return id

        # print "self.parsed_line"
        # print self.parsed_line

    def parse_taxon_string(self, taxon_string):
        taxon_string_arr = taxon_string.split(";")[::2][1:]
        return ";".join([x.strip('"').strip("'") for x in taxon_string_arr])

    def parse_taxonomy(self, args):
        filename = args.input_file
        with gzip.open(filename, 'rb') as infile:
        #
        # with open(filename, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line: continue #Skip empty
                # print line
                header, taxon_string = line.split("\t")
                # print "taxon_string"
                # print taxon_string
                """
                header
                >S000655554 uncultured bacterium; L2Sp-28
                taxon_string
                Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ilumatobacter;genus

                """
                id = self.parse_header(header)
                taxonomy_only = self.parse_taxon_string(taxon_string)
                # print taxonomy_only
                self.parsed_line[id]["taxonomy_only"] = taxonomy_only
                
                # print "all"
                # print self.parsed_line
                # out_header = self.format_header(header)
                # print out_header
                # print sequence
    def print_taxonomy(self):
        for k,v in self.parsed_line.items():
            # print "self.parsed_line: k = %s, v = %s" % (k, v)
            print "%s\t%s;%s\t1" % (k, v['taxonomy_only'], v['binomial_plus'])


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
    taxonomy.print_taxonomy()

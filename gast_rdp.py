#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import gzip
import IlluminaUtils.lib.fastalib as fa

"""TODO: write into file separately seq and tax"""

class Files:
    def __init__(self, args):
        self.filename   = args.input_file
        # self.infile     = self.open_file()
        self.compressed = args.compressed
        self.out_file_names = {"fa": "gast_rdp.fa", "tax": "gast_rdp.tax"}
        self.out_files = {}

    def open_file(self):
        if self.compressed:
            return gzip.open(self.filename, 'rb')
        else:
            return open(self.filename, "r")

    def open_output_files(self):
      print "open_output_files"
      for k, v in self.out_file_names.items():
        self.out_files[k] = open(v, "w")

class Parser:
    def __init__(self, files):
        self.parsed_line = {}
        self.filename  = files.filename
        self.number_of_sequences = 0
        self.out_files = files.out_files
        
    def parse_input(self):
        fasta = fa.SequenceSource(self.filename)
        while fasta.next():
            fasta.seq = fasta.seq.upper()
            self.number_of_sequences += 1
            self.parse_taxonomy(fasta.id)

    def parse_header(self, header):
        # print "header"
        # print header
        id = header.split(" ")[0]
        try:
            self.parsed_line[id]["binomial_plus"] = " ".join(header.split("\t")[1:]).replace("; ", ";")
        except KeyError:
            self.parsed_line[id] = {}
            self.parsed_line[id]["binomial_plus"] = " ".join(header.split("\t")[1:]).replace("; ", ";")
        except:
            raise
        return id

        # print "self.parsed_line"
        # print self.parsed_line

    def parse_taxon_string(self, taxon_string):
        taxon_string_arr = taxon_string.split(";")[::2][1:]
        return ";".join([x.strip('"').strip("'") for x in taxon_string_arr])

    def parse_taxonomy(self, header_line):
        header, taxon_string = header_line.split("\t")
        """
        header
        >S000655554 uncultured bacterium; L2Sp-28
        taxon_string
        Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ilumatobacter;genus

        """
        id = self.parse_header(header)
        taxonomy_only = self.parse_taxon_string(taxon_string)
        self.parsed_line[id]["taxonomy_only"] = taxonomy_only

    def print_taxonomy(self):
        for k,v in self.parsed_line.items():
            self.out_files["tax"].write('>%s\t%s;%s\t1\n' % (k, v['taxonomy_only'], v['binomial_plus']))
            # print "self.parsed_line: k = %s, v = %s" % (k, v)
            print ">%s\t%s;%s\t1" % (k, v['taxonomy_only'], v['binomial_plus'])
        self.out_files["tax"].close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='''Takes > lines from rdp files, makes gast_silva like files.
    From release11_2_Bacteria_unaligned.fa.gz
    >S000655540 uncultured bacterium; L2Sp-13	Lineage=Root;rootrank;Bacteria;domain;"Actinobacteria";phylum;Actinobacteria;class;Acidimicrobidae;subclass;Acidimicrobiales;order;"Acidimicrobineae";suborder;Acidimicrobiaceae;family;Ilumatobacter;genus
    to silva.tax
    AAAA02010377.14668.16277        Bacteria;Proteobacteria;Alphaproteobacteria;Rickettsiales       1
    ''')

    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")
    parser.add_argument('--compressed', '-c', action = "store_true", default = False,
                                        help = 'Use if fastq compressed. Default is a %(default)s.')

    args = parser.parse_args()
    # print "args = "
    # print args

    files = Files(args)
    files.open_output_files()
    parser = Parser(files)

    parser.parse_input()
    parser.print_taxonomy()

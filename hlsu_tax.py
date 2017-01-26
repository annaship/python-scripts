#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

class Taxonomy:
    def __init__(self):
        self.output_text = {}
        self.ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]
        self.rank_level = ""
        
    """
    time head -2 silva.all1.tax_fa | sed 's/^/>/' | sed 's/\t#\t/\n/' | tr "\t" ";" | awk 'BEGIN {FS=";"; OFS="\t"}  {if ($0 ~ /^>/) print $1, $(NF-1)"_" $NF, $(NF-1), "NA", $(NF-2); else print}'
    """
    
    def fill_out_empty_ranks(self, taxon_split):
        return [taxon_split.append("NA") for i in range(8) if (len(taxon_split) < i+1)]

    def get_binomial(self, taxon_split):
        print "taxon_split from get_binomial"
        print taxon_split
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
        # print header LSUcultures334_taxonomy.txt
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;Prymnesium_parvum_f._patelliferum
        # goal:
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;parvum;f._patelliferum
        
        id, taxon = header.split("\t")
        print "id = %s" % id
        print "taxon = %s" % taxon
        
        taxon_split = taxon.split(";")
        print "len(taxon_split)"
        print len(taxon_split)

        binomial = self.get_binomial(taxon_split)
        # print "binomial = %s" % binomial
        
        genus = self.get_genus(taxon_split)            
        # print "genus = %s" % genus
            
        self.fill_out_empty_ranks(taxon_split)

        # print taxon_split[:5]
        
        # print "self.rank_level = "
        # print self.rank_level
        
        # rank_number = int(self.ranks.index(self.rank_level.lower()))
        # print "rank_number = "
        # print rank_number
        # reverse_from_family1 = [i for i in reversed(taxon_split[:rank_number + 1])]
        # reverse_from_family = reverse_from_family1[4 - rank_number]
        # reverse_from_family = [i for i in reversed(taxon_split[:5])]
        # print "reverse_from_family = "
        # print reverse_from_family

        return ">" + id + "\t" + binomial + "\t" + genus + "\tNA\t" + reverse_from_family
        # "\t".join(reverse_from_family)

    def parse_taxonomy(self, args):
        filename = args.input_file
        # self.rank_level = args.rank_level
        with open(filename, "r") as infile:
            for line in infile:
                # current_output_text = ""
                line = line.strip()
                if not line: continue #Skip empty
                print "line.split() in parse_taxonomy"
                print line.split()
                header, sequence = line.split()
                # current_output_text = ">" + line.replace("\t#\t", "\n")
                print "header = %s" % header
                print "sequence = %s" % sequence
                # out_header = self.format_header(header)
                # print "out_header = %s" % out_header
                # print "sequence = %s" % sequence


if __name__ == '__main__':


    taxonomy = Taxonomy()
    ranks = taxonomy.ranks
    parser = argparse.ArgumentParser()


    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")

    args = parser.parse_args()
    # print "args = "
    # print args

    
    taxonomy.parse_taxonomy(args)
    
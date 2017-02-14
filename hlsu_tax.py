#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import collections

class Taxonomy:
    def __init__(self):
        self.output_text = {}
        self.ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]
        self.rank_level = ""
        # self.all_tax_ranks = collections.defaultdict()
        self.all_tax_ranks = {}


    def clean_binomial(self):
        #'JX660799': {'domain': 'Eukaryota', 'family': 'Phaeocystaceae', 'order': 'Phaeocystales', 'phylum': 'Haptophyta', 'species': 'Phaeocystis_sp._JD-2012', 'genus': 'Phaeocystis', 'class': 'Haptophyceae'}
        for ref_id, tax_dict in self.all_tax_ranks.items():
            if tax_dict["species"].startswith(tax_dict["genus"]):
                tax_dict["species"] = tax_dict["species"].replace(tax_dict["genus"] + "_", "")
        # 'JX660799': {'domain': 'Eukaryota', 'family': 'Phaeocystaceae', 'order': 'Phaeocystales', 'phylum': 'Haptophyta', 'species': 'sp._JD-2012', 'genus': 'Phaeocystis', 'class': 'Haptophyceae'}
        
    def rank_compare(self, rank1, rank2):
        print self.ranks.index(rank1)
        return self.ranks.index(rank1) - self.ranks.index(rank2)
        

    def print_out_results(self, args):
        filename = args.output_file
        outfile = open(filename, "w")
        for ref_id, tax_dict in self.all_tax_ranks.items():
            out_line =  ref_id + "\t"
            
            """
            print tax_dict
            {'domain': 'Eukaryota', 'family': 'Prymnesiaceae', 'order': 'Prymnesiales', 'phylum': 'Haptophyta', 'species': 'palpebrale', 'genus': 'Prymnesium', 'class': 'Haptophyceae'}
            
            """
            """
            print sorted(tax_dict.items(), key=lambda (k,v): self.ranks.index(k))
            [('domain', 'Eukaryota'), ('phylum', 'Haptophyta'), ('class', 'Haptophyceae'), ('order', 'Phaeocystales'), ('family', 'Phaeocystaceae'), ('genus', 'Phaeocystis'), ('species', 'sp._JD-2012')]
            """
            out_line += ";".join([v for (k,v) in sorted(tax_dict.items(), key=lambda (k,v): self.ranks.index(k))])
            out_line += "\t1\n"
            outfile.write(out_line)
            
    def parse_line(self, line):
        # print header LSUcultures334_taxonomy.txt
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;Prymnesium_parvum_f._patelliferum  1
        # goal:
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;parvum;f._patelliferum
        # print line
        ref_id, taxon_string, num = line.split()
        
        taxon_split = taxon_string.split(";")

        current_tax_dict = {}
        for idx, rank in enumerate(self.ranks):
            current_tax_dict[rank] = taxon_split[idx]
        
        self.all_tax_ranks[ref_id] = current_tax_dict

    def parse_taxonomy(self, args):
        filename = args.input_file
        with open(filename, "r") as infile:
            for line in infile:
                line = line.strip()
                if not line: continue #Skip empty
                self.parse_line(line)
        
    def check_duplicates_in_line(self):
        for idx, rank in enumerate(reversed(self.ranks)):
            print "idx = %s, rank = %s" % (idx, rank)
            for ref_id, tax_dict in self.all_tax_ranks.items():
                try:
                    if tax_dict[rank] == tax_dict[self.ranks[idx+1]]:
                        print "ref_id = %s, rank = %s, tax_dict[rank] = %s, tax_dict[self.ranks[idx+1]] = %s" % (ref_id, rank, tax_dict[rank], tax_dict[self.ranks[idx+1]])
                        tax_dict[rank] = "empty_" + rank
                        print tax_dict
                except KeyError:
                    print "ERR"
                    print ref_id, tax_dict
                except:
                    raise
        


if __name__ == '__main__':


    taxonomy = Taxonomy()
    ranks = taxonomy.ranks
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")
    parser.add_argument("-o", "--out",
        required = True, action = "store", dest = "output_file",
        help = """Output file name""")

    args = parser.parse_args()

    
    taxonomy.parse_taxonomy(args)
    taxonomy.clean_binomial()
    taxonomy.check_duplicates_in_line()
    taxonomy.print_out_results(args)
    
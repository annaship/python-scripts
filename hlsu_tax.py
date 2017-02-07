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
        # self.rank_level = args.rank_level
        outfile = open(filename, "w")
        for ref_id, tax_dict in self.all_tax_ranks.items():
            out_line =  ref_id + "\t"
            
            """
            print tax_dict
            {'domain': 'Eukaryota', 'family': 'Prymnesiaceae', 'order': 'Prymnesiales', 'phylum': 'Haptophyta', 'species': 'palpebrale', 'genus': 'Prymnesium', 'class': 'Haptophyceae'}
            
            >>> students = ['dave', 'john', 'jane']
            >>> grades = {'john': 'F', 'jane':'A', 'dave': 'C'}
            >>> sorted(students, key=grades.__getitem__)
            ['jane', 'dave', 'john']
            
            
            https://docs.python.org/2.7/howto/sorting.html
            """
            
            # print sorted(tax_dict.values())
            # print sorted(tax_dict.values(), key=attrgetter('rank')
            # self.ranks.index(tax_dict.keys()))
            # a = sorted(zip(tax_dict.keys()), self.ranks)
            # [x for (y,x) in sorted(zip(Y,X))]
            
            # for k, v in tax_dict.items():
            print sorted(tax_dict.items(), key=lambda (k,v): self.ranks.index(k))
                
            #     print sorted(tax_dict.values(), cmp=self.rank_compare())
            #
            # a = ";".join(tax_dict.itervalues())
            #
            # # ";".join("=".join((str(k),str(v))) for k,v in mydict.items())
            # s = sorted(tax_dict, key=attrgetter('age'))
            # # a = [";".join(tax_dict[rank]) for rank in self.ranks]
            
            # listTwo = tax_dict.keys()
            # listOne = self.ranks
            # print type(a)
            # print a
            # print type(b)
            # print b
            # print zip(X,Y)
            # print sorted(zip(X,Y), key=lambda pair: pair[1])
            # a = [x for (x,y) in sorted(zip(X,Y))]
            # , key=lambda pair: pair[0])

            # print a.sort(key=lambda (x,y): b.index(x))
            # print sorted(listTwo, key=lambda x: listOne.index(x))
            
            # print "AAA"
            # print a

            

            for rank in self.ranks:
                 # + binomial + "\t" + genus + "\tNA\t" + reverse_from_family
                 out_line += tax_dict[rank] + ";"
            outfile.write(out_line + "\n")
            
    def parse_line(self, line):
        # print header LSUcultures334_taxonomy.txt
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;Prymnesium_parvum_f._patelliferum  1
        # goal:
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;parvum;f._patelliferum
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
    taxonomy.print_out_results(args)
    
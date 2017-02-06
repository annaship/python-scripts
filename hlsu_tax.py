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
        # print "taxon_split[5] from get_binomial"
        # print taxon_split[5]
        
        try:
            print "from get_binomial"
            print "superkingdom (%s)\nphylum (%s)\nclass (%s)\norder (%s)\nfamily (%s)\ngenus (%s)\nbinomial (%s)" % (taxon_split[0], taxon_split[1], taxon_split[2], taxon_split[3], taxon_split[4], taxon_split[5], taxon_split[6])
            
            binomial_all = taxon_split[6].split("_")
            genus = binomial_all[0]
            if taxon_split[5] != genus:
                print "OHOHOH taxon_split[5] (%s) != genus (%s)" % (taxon_split[5], genus)
                
            species = binomial_all[1]
            strain = " ".join(binomial_all[2:])
            print "GGG genus = %s, species = %s, strain = %s" % (genus, species, strain)
            return genus, species, strain
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
        
    
    def format_header(self, line):
        # print header LSUcultures334_taxonomy.txt
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;Prymnesium_parvum_f._patelliferum  1
        # goal:
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;parvum;f._patelliferum
        print "LLL line from format_header"
        print line
        ref_id, taxon_string, num = line.split()
        print "ref_id = %s" % ref_id
        print "taxon_string = %s" % taxon_string
        
        taxon_split = taxon_string.split(";")
        print "len(taxon_split)"
        print len(taxon_split)

        # binomial = 
        self.get_binomial(taxon_split)
        # print "binomial = %s" % binomial
        #
        # genus = self.get_genus(taxon_split)
        # print "genus = %s" % genus
            
        # self.fill_out_empty_ranks(taxon_split)

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

        # return ">" + id + "\t" + binomial + "\t" + genus + "\tNA\t" + reverse_from_family
        # "\t".join(reverse_from_family)

    def parse_taxonomy(self, args):
        filename = args.input_file
        # self.rank_level = args.rank_level
        with open(filename, "r") as infile:
            for line in infile:
                # current_output_text = ""
                line = line.strip()
                if not line: continue #Skip empty
                out_header = self.format_header(line)
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
    
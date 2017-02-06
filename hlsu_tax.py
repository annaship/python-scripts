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
            #
            # for idx, rank in enumerate(self.ranks):
            #     current_tax_dict[rank] = taxon_split[idx]
                
            # print 'YYY: current_tax_dict'
            # print current_tax_dict

            binomial_all = taxon_split[6].split("_")
            genus = binomial_all[0]
            if taxon_split[5] != genus:
                print "OHOHOH taxon_split[5] (%s) != genus (%s)" % (taxon_split[5], genus)
                
            species = binomial_all[1]
            strain = " ".join(binomial_all[2:])
            print "GGG genus = %s, species = %s, strain = %s" % (genus, species, strain)
            return genus, species, strain
            
            print 
        except IndexError:
            return "NA"
        except:
            raise

    def get_genus(self, taxon_split):
        try:
            return taxon_split[6]
        except IndexError:
            return "NA"
        except:
            raise
        
    def clean_binomial(self):
        # print 'YYY: all_tax_ranks'
        # print self.all_tax_ranks
        #'JX660799': {'domain': 'Eukaryota', 'family': 'Phaeocystaceae', 'order': 'Phaeocystales', 'phylum': 'Haptophyta', 'species': 'Phaeocystis_sp._JD-2012', 'genus': 'Phaeocystis', 'class': 'Haptophyceae'}
        for ref_id, tax_dict in self.all_tax_ranks.items():
            if tax_dict["species"].startswith(tax_dict["genus"]):
                tax_dict["species"] = tax_dict["species"].replace(tax_dict["genus"] + "_", "")

    def parse_line(self, line):
        # print header LSUcultures334_taxonomy.txt
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;Prymnesium_parvum_f._patelliferum  1
        # goal:
        # AF289038	Eukaryota;Haptophyceae;Prymnesiales;Prymnesiaceae;Prymnesium;parvum;f._patelliferum
        ref_id, taxon_string, num = line.split()
        
        taxon_split = taxon_string.split(";")
        # if len(taxon_split) != 7:
        #     print "len(taxon_split)"
        #     print len(taxon_split)

        current_tax_dict = {}
        for idx, rank in enumerate(self.ranks):
            current_tax_dict[rank] = taxon_split[idx]
        
        self.all_tax_ranks[ref_id] = current_tax_dict
        
        # self.get_binomial(taxon_split)
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
                # out_header =
                self.parse_line(line)
                
                # print "out_header = %s" % out_header
                # print "sequence = %s" % sequence
        # print 'YYY: all_tax_ranks'
        # print self.all_tax_ranks
        
        


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
    taxonomy.clean_binomial()
    print 'YYY: all_tax_ranks'
    print taxonomy.all_tax_ranks
    
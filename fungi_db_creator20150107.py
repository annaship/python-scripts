#! /opt/local/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011, Marine Biological Laboratory
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
# ver 2 2013 Jul 19 - convert taxonomy table
# ver 3 2013 Jul 31 - convert taxonomy table, remove all trailing garbage, leave insertae_cedis
# 1)
# GU295056        k__Fungi;p__Ascomycota;c__Sordariomycetes;o__Incertae_sedis;f__Glomerellaceae;g__Glomerella;s__Colletotrichum_gloeosporioides
# 
# 2)
# GU319887        k__Fungi;p__unidentified;c__unidentified;o__unidentified;f__unidentified;g__unidentified;s__fungal_sp_QP_2010
# 
# 3)
# FJ820581        k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Thelephora;s__unculturedfungus

import argparse

def uniq_array(arr): 
   # order preserving
   noDupes = []
   [noDupes.append(i) for i in arr if not noDupes.count(i)]
   return noDupes
   
def make_taxa_dict(tax_infile):
    taxonomy = {}
    
    for line in open(tax_infile):
        tax_line = {}
        
        line = line.strip()
        tax_line_split = line.split("|")
        try:
            split_tax = tax_line_split[1].split(';')
        except:
            print "line = %s" % line
            # print "tax_line_split[1] = %s" % tax_line_split[1]
            print "tax_line_split = %s" % tax_line_split
            raise
        id_tax    = tax_line_split[0].lstrip(">")
        tax_line["class"]          = ""
        tax_line["order"]          = ""
        tax_line["family"]         = ""
        tax_line["genus"]          = ""
        tax_line["species"]        = ""
        for taxon in split_tax:
            # http://species.wikimedia.org/wiki/Fungi
            # Phyla: Ascomycota - Basidiomycota - Blastocladiomycota - Chytridiomycota - Glomeromycota - Microsporidia - Neocallimastigomycota - Zygomycota - Fungi incertae sedis
            # FJ820581        k__Fungi;p__Basidiomycota;c__Agaricomycetes;o__Thelephorales;f__Thelephoraceae;g__Thelephora;s__unculturedfungus
            tax_line["kingdom_phylum"] = ""
            tax_line["kingdom"]        = "Fungi"
            if taxon.startswith("p__"):
                tax_line["phylum"]  = taxon.split("__")[1]                
            if taxon.startswith("c__"):
                tax_line["class"]   = taxon.split("__")[1]
            if taxon.startswith("o__"):
                tax_line["order"]   = taxon.split("__")[1]
            if taxon.startswith("f__"):
                tax_line["family"]  = taxon.split("__")[1]
            if taxon.startswith("g__"):
                tax_line["genus"]   = taxon.split("__")[1]
            if taxon.startswith("s__"):
                tax_line["species"] = taxon.split("__")[1]
        taxonomy[id_tax] = tax_line
    return taxonomy
    
def remove_empty(tax_line, name, bad_value):
    if tax_line[name] in bad_value:
        tax_line[name] = ''
    return tax_line[name]
    
def remove_empty_from_end(ordered_names, old_taxonomy, bad_value):
    taxonomy_with_wholes = {}
    ordered_names_from_phylum = ordered_names[2:] #no kingdom and kingdom_phylum
    for tax_id, tax_line in old_taxonomy.items():
        for name in reversed(ordered_names):
            res_taxa = remove_empty(tax_line, name, bad_value)
            if res_taxa != '':
                break
        taxonomy_with_wholes[tax_id] = tax_line
    return taxonomy_with_wholes
    
def make_kingdom_phylum(tax_line, bad_value):
    tax_line["kingdom_phylum"] = "Fungi"
    if (tax_line["phylum"] != "") and (tax_line["phylum"] not in bad_value[1:]):
        tax_line["kingdom_phylum"] = tax_line["kingdom"] + "_" + tax_line["phylum"]
    return tax_line
    
# def separate_binomial_name(tax_line):
#     # uncultured_species(tax_line["species"])
#     if (tax_line["species"].find(" ") > 0):
#         species = tax_line["species"].split(" ")
#         genus   = tax_line["genus"]
#         if (species[0] == genus):
#             tax_line["species"] = ' '.join(species[1:])
#     return tax_line
    
def clean_binomial_name(tax_line, tax_id, dbl_gen_out_f, odd_names_out_f):
    if (tax_line["species"].find(" ") > 0):
        species = tax_line["species"].split(" ")
        rest = ' '.join(species[1:])
        
        if (species[0] == tax_line["genus"]):
            tax_line["species"] = rest
        # elif ((species[0] in tax_line.values()) and (rest == "sp")):
        elif ((species[0] in tax_line.values()) and ((rest == "sp") or rest.startswith("sp ") or rest.startswith("sp."))):
            tax_line["species"] = ''
        elif (species[0][0].isupper() and tax_line["genus"][0].isupper()):     
            # print "species[0][0] = %s" % species[0][0]
            # todo:
            # change to list, sort, write
            dbl_gen_out_f.write(tax_id + "\n")
        else:
          # change to list, sort, write
            odd_names_out_f.write(tax_id + "\n")
          
            # pass
            # print 'tax_line["genus"] = %s, tax_line["species"] = %s' % (tax_line["genus"], tax_line["species"])
    return tax_line
    
def incertae_sedis(tax_line):
    for rank, taxon in tax_line.items():
        if (taxon == 'Incertae sedis'):
            tax_line[rank] = 'Incertae_sedis'
    return tax_line

def remove_utf_16(tax_line):
  # translations = (
  #     (u'\N{LATIN SMALL LETTER E WITH DIAERESIS}', u'e'),
  #     (u'\N{MULTIPLICATION SIGN}', u'x '),
  #     # et cetera
  #     )
  # 
  # test = u'M\N{LATIN SMALL LETTER O WITH DIAERESIS}ller von M\N{LATIN SMALL LETTER U WITH DIAERESIS}nchen'
  # 
  # out = test
  # for from_str, to_str in translations:
  #     out = out.replace(from_str, to_str)
  # print out
  
  # 235 0xEB  22571,96
    e = 'ë'
    x = '×'
    # table = {
    # LATIN SMALL LETTER E WITH DIAERESIS
              # 0xe4: u'ae',
              # ord(u'ë'): u'e',
              # ord(u'ü'): u'ue',
              # ord(u'×'): None,
            # }
  
    for rank, taxon in tax_line.items():
      try:
        # tax_line[rank].replace(e.encode('utf-8'), 'e')
        tax_line[rank].replace(e.decode('utf-8'), 'e')
        tax_line[rank].replace(x.decode('utf-8'), 'x')
        # print e.encode('utf-8')
        
        # t = tax_line[rank].decode('cp1252')
        # tax_line[rank] = t.translate(table)
      except:
        # print tax_line
        pass
        # tax_line[rank].replace(u'ë', 'e')
        # tax_line[rank].replace(unichr(235), 'e')
        # '×siegelii'
        # tax_line[rank].replace(u'×', '')
            
    return tax_line

def make_new_taxonomy(tax_line_w_k_ph, ordered_names):
    new_line = []
    new_line = "Eukarya"
    for name in ordered_names[2:]:
        if tax_line_w_k_ph[name] != "":
            new_line += (";" + tax_line_w_k_ph[name])
    return new_line
        
def change_id(tax_id):
    return "its1_" + tax_id
    
def uncultured_species(species):
    # uncultured Acaulosporaceae
    try: 
        species.index("uncultured")
        print "species = %s" % species
        try:        
            a = species.index([A-Z])
            print a
            b = species[a:]
            print b
        except:
            pass
    except:
        pass

def process(args):
    tax_infile    = args.tax_infile
    taxout_fh     = open(args.tax_outfile,'w')
    dbl_gen_out_f = open('dbl_gen_ids.txt','w')
    odd_names_out_f = open('odd_names_ids.txt','w')    
    ordered_names = "kingdom", "phylum", "kingdom_phylum", "class", "order", "family", "genus", "species"
    bad_value     = "Fungi", "unculturedfungus", "uncultured fungus", "unidentified", "sp", "sp.", "unidentified_sp.", "unidentified sp."
    # "unculturedsoil_fungus", "uncultured soil fungus", "unculturedcompost_fungus", "uncultured compost fungus", "uncultured ectomycorrhizal fungus"
    old_taxonomy  = make_taxa_dict(tax_infile)
    separated_species_taxonomy = {}
    for tax_id, tax_line in old_taxonomy.items():
        # separated_species_taxonomy[tax_id] = separate_binomial_name(tax_line)
        separated_species_taxonomy[tax_id] = clean_binomial_name(tax_line, tax_id, dbl_gen_out_f, odd_names_out_f)
        
    taxonomy_with_wholes = remove_empty_from_end(ordered_names, separated_species_taxonomy, bad_value)
    for tax_id, tax_line in taxonomy_with_wholes.items():    
        tax_line = incertae_sedis(tax_line)
        # tax_line = remove_utf_16(tax_line)
        tax_line_w_k_ph = make_kingdom_phylum(tax_line, bad_value)        
        taxout_fh.write(change_id(tax_id) + "\t"  + make_new_taxonomy(tax_line_w_k_ph, ordered_names) + "\t" + "1" + "\n")


 
if __name__ == '__main__':
    THE_DEFAULT_BASE_OUTPUT = '.'

    usage = "usage: %prog [options] arg1"
    parser = argparse.ArgumentParser(description='ref fasta/tax file creator')
    parser.add_argument('-it', '--tax_in', required=True, dest = "tax_infile",
                                                 help = '')   
    #parser.add_argument('-if', '--fasta_in', required=True, dest = "fasta_infile",
    #                                             help = '')
    parser.add_argument('-ot', '--tax_out', required=False, dest = "tax_outfile",   default='outfile.tax',
                                                 help = '')
    #parser.add_argument('-of', '--fasta_out', required=False, dest = "fasta_outfile", default='outfile.fasta',
    #                                             help = '')                                            
    args = parser.parse_args() 
    
     

    # now do all the work
    process(args)


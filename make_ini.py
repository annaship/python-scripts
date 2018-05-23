#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

r_keys = ["AACAGTAT", "ACCATACT", "ACCTCCCA", "AGAGAGGC", "AGCTGACG", "AGGCTTCA", "ATAGGTGG", "ATCGCACC", "ATGCCAGC", "CAACTTCA", "CACTCACT", "CAGCGGCA", "CCGACAAA", "CCGCACCG", "CGACATTC", "CGTCCCAC", "CTGTTAGT", "GAAACTGG", "GAGTTTGA", "GCAATGGA", "GCCTGTTC", "GGTAATGA", "GTAGTCGA", "GTGCTGAT", "TAAGGGAG", "TACGATAC", "TCAAAGCT", "TCCCGATG", "TCCGTGCG", "TCGAACAC", "TGGGACCT", "TGTTTCCC"]

def open_write_close(script_file_name, text):
    ini_file = open(script_file_name, "w")
    ini_file.write(text)
    ini_file.close()

def create_inis():   
    input_directory = "/groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results"
    output_directory = "/groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap"
    # input_directory = "/Users/ashipunova/BPC/today/stefan_linda/results"
    # output_directory = "/Users/ashipunova/BPC/today/stefan_linda/results/reads_overlap"
    email = "ashipunova@mbl.edu"

    for r_key in r_keys:
        text = """[general]
project_name = %s
researcher_email = %s
input_directory = %s
output_directory = %s

[files]
pair_1 = %s
pair_2 = %s
            """ % (r_key, email, input_directory, output_directory, r_key + "_R1.fastq", r_key + "_R2.fastq")

        text += """
# following section is optional
[prefixes]
pair_1_prefix = ^ATTGAGTGCCAGC[AC]GCCGCGGTAA
pair_2_prefix = ^GGACTAC[ACT][ACG]GGGT[AT]TCTAAT
            """
        ini_file_name = os.path.join(input_directory,  r_key + ".ini")
        print(ini_file_name)
        open_write_close(ini_file_name, text)

if __name__ == '__main__':
    create_inis()

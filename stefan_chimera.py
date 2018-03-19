#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

r_keys = ["AACAGTAT", "ACCATACT", "ACCTCCCA", "AGAGAGGC", "AGCTGACG", "AGGCTTCA", "ATAGGTGG", "ATCGCACC", "ATGCCAGC", "CAACTTCA", "CACTCACT", "CAGCGGCA", "CCGACAAA", "CCGCACCG", "CGACATTC", "CGTCCCAC", "CTGTTAGT", "GAAACTGG", "GAGTTTGA", "GCAATGGA", "GCCTGTTC", "GGTAATGA", "GTAGTCGA", "GTGCTGAT", "TAAGGGAG", "TACGATAC", "TCAAAGCT", "TCCCGATG", "TCCGTGCG", "TCGAACAC", "TGGGACCT", "TGTTTCCC"]

def open_write_close(script_file_name, text):
    ini_file = open(script_file_name, "w")
    ini_file.write(text)
    ini_file.close()

def get_chimeric_ids(self):
    ids = set()
    chimera_file_names = self.get_chimera_file_names(self.outdir)
    file_ratio = self.check_chimeric_stats()

    for file_name in chimera_file_names:
#             logger.debug("from get_chimeric_ids: file_name = %s" % file_name)
        if file_name.endswith(self.chimeric_suffix):
            both_or_denovo = self.get_chimeras_suffix(file_ratio, file_name)
#                 TODO: run ones for each file_base = ".".join(file_name.split(".")[0:3]) (for txt and db)
            if file_name.endswith(both_or_denovo):
                file_name_path = os.path.join(self.outdir, file_name)
                self.utils.print_both("Get ids from %s" % file_name_path)
                read_fasta     = fa.ReadFasta(file_name_path)
                ids.update(set(read_fasta.ids))
    return ids

def move_out_chimeric(self):
    chimeric_ids = get_chimeric_ids()
    for idx_key in input_file_names:
        fasta_file_path    = os.path.join(indir, input_file_names[idx_key])
        read_fasta         = fa.ReadFasta(fasta_file_path)
        read_fasta.close()

        non_chimeric_file  = fasta_file_path + nonchimeric_suffix
        non_chimeric_fasta = fa.FastaOutput(non_chimeric_file)

        fasta              = fa.SequenceSource(fasta_file_path, lazy_init = False)
        while fasta.next():
            if not fasta.id in chimeric_ids:
                non_chimeric_fasta.store(fasta, store_frequencies = False)
        non_chimeric_fasta.close()

if __name__ == '__main__':
    create_inis()

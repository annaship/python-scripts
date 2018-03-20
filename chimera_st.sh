#!/bin/sh

r_keys="AACAGTAT ACCATACT ACCTCCCA AGAGAGGC AGCTGACG AGGCTTCA ATAGGTGG ATCGCACC ATGCCAGC CAACTTCA CACTCACT CAGCGGCA CCGACAAA CCGCACCG CGACATTC CGTCCCAC CTGTTAGT GAAACTGG GAGTTTGA GCAATGGA GCCTGTTC GGTAATGA GTAGTCGA GTGCTGAT TAAGGGAG TACGATAC TCAAAGCT TCCCGATG TCCGTGCG TCGAACAC TGGGACCT TGTTTCCC"


for rkey in $r_keys
do
  echo "rkey = $rkey"  
  
    vsearch -uchime_denovo /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chg -uchimeout /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.txt -nonchimeras  /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.txt.nonchimeric.fa -chimeras /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.txt.chimeric.fa -notrunclabels

    vsearch -uchime_ref /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chg -uchimeout /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.db -nonchimeras  /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.db.nonchimeric.fa -chimeras /groups/vampsweb/new_vamps_maintenance_scripts/data/processing/results/reads_overlap/"$rkey"_MERGED-MAX-MISMATCH-3.unique.chimeras.db.chimeric.fa -notrunclabels -strand plus -db /groups/g454/blastdbs/rRNA16S.gold.fasta
done

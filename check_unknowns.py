#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ver 2 (class)

import os
import sys
import argparse
from collections import defaultdict


class Check_tax:
    def __init__(self):
        self.current_dataset = ""
        self.dataset_dict = defaultdict(list)

    def parse_line(self, filename):
        with open(filename, "r") as infile:
            current_dataset = None
            for line in infile:
                line = line.strip("|")
                line_fields = line.split(" | ")
                self.datasets_to_dict(line_fields)
        self.check_unknowns()


    def datasets_to_dict(self, line_fields):
        for field in line_fields:
            try:
                self.dataset_dict[line_fields[1].strip("|").strip()].append(line_fields[2].strip().strip("|").strip())
            except IndexError:
                pass
            except:
                raise
                
    def check_unknowns(self):
        for dataset, tax in self.dataset_dict.items():
            tax_set = set(tax)
            tax_str = ", ".join(tax_set)
            if len(tax_set) < 4 and tax_str == "Unknown":
                print "dataset = %s, tax = %s" % (dataset, tax_str)


if __name__ == '__main__':
    check_tax = Check_tax()

    parser = argparse.ArgumentParser()

    parser.add_argument("-d", "--dir",
        required = False, action = "store", dest = "start_dir", default = '.',
        help = """Input directory name, default - current""")
    parser.add_argument("-i", "--in",
        required = True, action = "store", dest = "input_file",
        help = """Input file name""")


    args = parser.parse_args()
    print "args = "
    print args


    check_tax.parse_line(args.input_file)

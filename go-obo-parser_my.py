#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A constant-space parser for the GeneOntology OBO v1.2 format

Version 1.0

added database utility by Anna Shipunova 2016-10-27
"""
from __future__ import with_statement
from collections import defaultdict
import itertools
import os

__author__    = "Uli Koehler"
__copyright__ = "Copyright 2013 Uli Koehler"
__license__   = "Apache v2.0"

def processGOTerm(goTerm):
    """
    In an object representing a GO term, replace single-element lists with
    their only member.
    Returns the modified object as a dictionary.
    """
    ret = dict(goTerm) #Input is a defaultdict, might express unexpected behaviour
    for key, value in ret.iteritems():
        if len(value) == 1:
            ret[key] = value[0]
    return ret

def parseGOOBO(filename):
    """
    Parses a Gene Ontology dump in OBO v1.2 format.
    Yields each
    Keyword arguments:
        filename: The filename to read
    """

    with open(filename, "r") as infile:
        currentGOTerm = None
        for line in infile:
            line = line.strip()
            if not line: continue #Skip empty
            if line == "[Term]":
                if currentGOTerm: yield processGOTerm(currentGOTerm)
                currentGOTerm = defaultdict(list)
            elif line == "[Typedef]":
                #Skip [Typedef sections]
                currentGOTerm = None
            else: #Not [Term]
                #Only process if we're inside a [Term] environment
                if currentGOTerm is None: continue
                key, sep, val = line.partition(":")
                currentGOTerm[key].append(val.strip())
        #Add last term
        if currentGOTerm is not None:
            yield processGOTerm(currentGOTerm)

def create_insert_term_query(goTerm):
    """
    insert into term (ontology_id, term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
    (1, )

        {'is_a': ['CHEBI:25585 ! nonmetal atom', 'CHEBI:33300 ! pnictogen'], 'id': 'CHEBI:25555', 'name': 'nitrogen atom'}

    """
    insert_term_query_1 = ""

    try:
        term_name = goTerm['name']
        identifier = goTerm['id']
        if 'def' in goTerm:
            definition = clean_definition(goTerm['def'])
        else:
            definition = ""

        if ('is_obsolete' in goTerm) and (goTerm['is_obsolete'] == "true") :
            is_obsolete = 1
        else:
            is_obsolete = 0

        if 'is_a' in goTerm:
            is_root_term = 0
            is_leaf      = 1
        else:
            is_root_term = 1
            is_leaf      = 0


        insert_term_query_1 = """(2, "%s", "%s", "%s", "%s", "%s", "%s")\n""" % (term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
    except KeyError:
        pass
    except:
        raise
    return insert_term_query_1

def get_term_path(goTerm, parents):
    term_identifier = goTerm['id']
    # 'is_a': ['CHEBI:25585 ! nonmetal atom', 'CHEBI:33300 ! pnictogen']
    # print "EEE: type(goTerm['is_a']) = %s" % type(goTerm['is_a'])
    if (type(goTerm['is_a']) == 'str'):
        parents[term_identifier] = ent.split(' ! ')
    elif (type(goTerm['is_a']) == 'list'):
        for ent in goTerm['is_a']:
            # print "TTT"
            # print ent
            a = ent.split(' ! ')
            # print "AAA"
            # print a
            parents[term_identifier].append(ent.split(' ! '))
    # print "PPP parents"
    # print parents

def clean_definition(definition):
    cl_def = definition.strip(' []').replace('"', '').replace('\\', '')
    return ''.join([i if ord(i) < 128 else ' ' for i in cl_def])

def write_file(header, query, target):

    target.write(header)
    target.write("\n")
    target.write(query)
    target.close()


def combine_insert_term_query(all_term_dict_l):
    insert_term_query = [create_insert_term_query(goTerm) for goTerm in all_term_dict_l]
    max_lines = 7000
    for chunk in chunks(insert_term_query, max_lines):
        print_out_term_query(", ".join(chunk))
    return insert_term_query

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
def print_out_term_query(to_print):
    first_line = """
    INSERT IGNORE INTO term (ontology_id, term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
      VALUES
    """

    i = 0
    while os.path.exists("out%s.sql" % i):
        i += 1
    target = open("out%s.sql" % i, "w")
    
    write_file(first_line, to_print, target)
    
    
def combine_insert_term_query2(all_term_dict_l):
    insert_term_query = ""
    first_line = """
    INSERT IGNORE INTO term (ontology_id, term_name, identifier, definition, is_obsolete, is_root_term, is_leaf)
      VALUES
    """
    cnts = 0
    cnts_max = 0
    max_lines = 50
    i = 0
    
    for goTerm in all_term_dict_l:
        # print goTerm
        
        cnts += 1
        cnts_max += 1
        insert_term_query += create_insert_term_query(goTerm)
        if cnts_max == max_lines:
            while os.path.exists("out%s.sql" % i):
                i += 1

            target = open("out%s.sql" % i, "w")
            
            write_file(first_line, insert_term_query, target)
            cnts_max = 0
        if cnts < len(all_term_dict_l):
            insert_term_query += ", "
            next
    return insert_term_query

if __name__ == "__main__":
    """Print out the number of GO objects in the given GO OBO file"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='The input file in GO OBO v1.2 format.')
    args = parser.parse_args()
    all_term_dict = parseGOOBO(args.infile)
    all_term_dict_l = list(all_term_dict)

    insert_term_query = combine_insert_term_query(all_term_dict_l)


    parents = {}

    for goTerm in all_term_dict_l:
        # print goTerm

        if 'is_a' in goTerm:
            get_term_path(goTerm, parents)

    # print "NNN insert_term_query = %s" % insert_term_query
    # print insert_term_query
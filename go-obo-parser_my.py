#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A constant-space parser for the GeneOntology OBO v1.2 format

Version 1.0

added database utility by Anna Shipunova 2016-10-27
"""
from __future__ import with_statement
from collections import defaultdict

__author__    = "Uli Koehler"
__copyright__ = "Copyright 2013 Uli Koehler"
__license__   = "Apache v2.0"

def processGOTerm(goTerm):
    """
    In an object representing a GO term, replace single-element lists with
    their only member.
    Returns the modified object as a dictionary.
    """
    return {key: value[0] for key, value in goTerm.items()}

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
    insert into term (ontology_id, term_name, identifier, definition, namespace, is_obsolete, is_root_term, is_leaf)
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
        namespace = 'envo'
        if 'is_a' in goTerm:
            is_root_term = 0
            is_leaf      = 1
        else:
            is_root_term = 1
            is_leaf      = 0
    
        insert_term_query_1 = "(1, '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (term_name, identifier, definition, namespace, "0", is_root_term, is_leaf)
    except KeyError:
        pass
    except:
        raise
    return insert_term_query_1
    
def get_term_path(goTerm, parents):
    term_identifier = goTerm['id']
    # 'is_a': ['CHEBI:25585 ! nonmetal atom', 'CHEBI:33300 ! pnictogen']
    print "EEE: type(goTerm['is_a']) = %s" % type(goTerm['is_a'])
    if (type(goTerm['is_a']) == 'str'):
        parents[term_identifier] = ent.split(' ! ')
    elif (type(goTerm['is_a']) == 'list'):
        for ent in goTerm['is_a']:
            print "TTT"
            print ent
            a = ent.split(' ! ')
            print "AAA"
            print a
            parents[term_identifier].append(ent.split(' ! '))
    print "PPP parents"
    print parents
        
def clean_definition(definition):
    # definition
    pass

if __name__ == "__main__":
    """Print out the number of GO objects in the given GO OBO file"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='The input file in GO OBO v1.2 format.')
    args = parser.parse_args()
    #Iterate over GO terms
    # termCounter = 0
    all_term_dict = parseGOOBO(args.infile)
    print "HHH: all_term_dict type = %s" % type(all_term_dict)
    # for goTerm in all_term_dict:
    #     termCounter += 1
    #     print goTerm
    # print "Found %d GO terms" % termCounter
    
    
    insert_term_query = """
    insert into term (ontology_id, term_name, identifier, definition, namespace, is_obsolete, is_root_term, is_leaf)
      values (
    """
    for goTerm in all_term_dict:
        # print goTerm
        insert_term_query += create_insert_term_query(goTerm)
    insert_term_query += ");"
    
    parents = {}
    print "SSS start get_term_path"
    for goTerm in all_term_dict:
        print goTerm
        
        if 'is_a' in goTerm:
            get_term_path(goTerm, parents)
    
    print "NNN insert_term_query = %s" % insert_term_query
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
            
    # print "RET = "
    # print ret
    #
    # print "RET2 = "
    # print {key: value[0] for key, value in ret.items() if len(value) == 1}
    #
    return ret
    """
    EEE: type(goTerm['is_a']) = <type 'str'>
    PPP parents
    {}
    {'is_a': ['CHEBI:33693 ! oxygen hydride', 'CHEBI:37176 ! mononuclear parent hydride', 'CHEBI:52625 ! inorganic hydroxy compound'], 'id': 'CHEBI:15377', 'name': 'water'}
    
    """
    

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
    
        insert_term_query_1 = """(1, "%s", "%s", "%s", "%s", "%s", "%s", "%s"), \n""" % (term_name, identifier, definition, namespace, "0", is_root_term, is_leaf)
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
    # print "definition = %s" % definition
    
    cl_def = definition.strip(' []').replace('"', '')
    return ''.join([i if ord(i) < 128 else ' ' for i in cl_def])
    # print "aa = %s" % aa

if __name__ == "__main__":
    """Print out the number of GO objects in the given GO OBO file"""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='The input file in GO OBO v1.2 format.')
    args = parser.parse_args()
    #Iterate over GO terms
    # termCounter = 0
    # all_term_dict_res = parseGOOBO(args.infile)
    all_term_dict, all_term_dict_2 = itertools.tee(parseGOOBO(args.infile))
    
    # print "HHH: all_term_dict type = %s" % type(all_term_dict)
    # for goTerm in all_term_dict:
    #     termCounter += 1
    #     print goTerm
    # print "Found %d GO terms" % termCounter
    
    
    insert_term_query = """
    insert into term (ontology_id, term_name, identifier, definition, namespace, is_obsolete, is_root_term, is_leaf)
      values 
    """
    
    for goTerm in all_term_dict:
        # print goTerm
        insert_term_query += create_insert_term_query(goTerm)
    
    parents = {}
    # print "SSS start get_term_path"
    for goTerm in all_term_dict_2:
        # print goTerm
        
        if 'is_a' in goTerm:
            get_term_path(goTerm, parents)
    
    # print "NNN insert_term_query = %s" % insert_term_query
    print insert_term_query
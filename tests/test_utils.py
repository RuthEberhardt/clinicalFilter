"""
Copyright (c) 2021 Genome Research Limited
Author: Ruth Eberhardt <re3@sanger.ac.uk>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

# methods to create person, family and variant objects to use in tests

from variants.snv import SNV
from variants.cnv import CNV
from family.families import Person
from family.families import Family
from variants.trio_genotype import add_trio_genotypes

def create_test_person(family_id, person_id, dad_id, mum_id, sex, affected, path):
    person = Person(family_id, person_id, dad_id, mum_id, sex, affected, path)
    return person

def create_test_family(child, mum, dad):
    family = Family(child, mum, dad)
    return family

def create_test_snv(vardata):
    '''create an SNV from a variant hash'''
    Var = SNV
    var = Var(vardata)
    return var

def create_test_cnv(vardata):
    '''create an SNV from a variant hash'''
    Var = CNV
    var = Var(vardata)
    return var

def create_test_candidate_vars(single_vars, compound_hets):
    '''create candidate variants hash from variant data'''
    candidates = {'single_variants': {}, 'compound_hets': {}}

    for vid in single_vars.keys():
        variant = SNV
        var = variant(single_vars[vid]['variant'])
        candidates['single_variants'][vid] = {}
        candidates['single_variants'][vid]['variant'] = var
        candidates['single_variants'][vid]['mode'] = single_vars[vid]['mode']

    for gn in compound_hets.keys():
        candidates['compound_hets'][gn] = {}
        for cvid in compound_hets[gn].keys():
            Var = SNV
            var = Var(compound_hets[gn][cvid]['variant'])
            candidates['compound_hets'][gn][cvid]['variant'] = var
            candidates['compound_hets'][gn][cvid]['mode'] = compound_hets[gn][cvid]['mode']

    return candidates

def create_test_variants_per_gene(variants, family):
    '''create variants_per_gene from variant data'''
    familyvariants = {'child':{}, 'mum':{}, 'dad':{}}
    variants_per_gene = {}
    for vid in variants['child'].keys():
        variant = SNV
        var = variant(variants['child'][vid])
        familyvariants['child'][vid] = var
    if 'mum' in variants.keys():
        for vid in variants['mum'].keys():
            variant = SNV
            var = variant(variants['mum'][vid])
            familyvariants['mum'][vid] = var
    if 'dad' in variants.keys():
        for vid in variants['dad'].keys():
            variant = SNV
            var = variant(variants['dad'][vid])
            familyvariants['dad'][vid] = var
    add_trio_genotypes(family, familyvariants)

    for vid in familyvariants['child'].keys():
        hgncid = familyvariants['child'][vid].hgnc_id
        if hgncid not in variants_per_gene.keys():
            variants_per_gene[hgncid] = {}
        variants_per_gene[hgncid][vid] = {}
        variants_per_gene[hgncid][vid]['child'] = familyvariants['child'][vid]
        if vid in familyvariants['mum'].keys():
            variants_per_gene[hgncid][vid]['mum'] = familyvariants['mum'][
                vid]
        if vid in familyvariants['dad'].keys():
            variants_per_gene[hgncid][vid]['dad'] = familyvariants['dad'][
                vid]

    return(variants_per_gene)




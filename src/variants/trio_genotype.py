"""
copyright
"""
import logging
from variants.variant import Variant

def add_trio_genotypes(family, variants):
    '''add trio genotypes to all child variants for a family'''
    if family.has_both_parents():
        #if parents are present we assume positions not present are ref/ref
        add_trio_genotypes_both_parents(variants)
    elif family.has_mum():
        add_trio_genotypes_mum_only(variants)
    elif family.has_dad():
        add_trio_genotypes_dad_only(variants)
    elif family.has_no_parents():
        add_trio_genotypes_no_parents(variants)
    else:
        print(
            "Error: should not get here as family must either have both, one \
             or no parents")
        logging.error("Can't calculate trio genotypes - family error")
        exit(1)

def add_trio_genotypes_both_parents(variants):
    '''add trio genotypes in a dict of variants where there are both parents'''
    for v in variants['child'].keys():
        if variants['child'][v].is_snv():
            childgeno = variants['child'][v].genotype
            mumgeno = '0'
            dadgeno = '0'
            if v in variants['mum'].keys():
                mumgeno = variants['mum'][v].genotype
            if v in variants['dad'].keys():
                dadgeno = variants['dad'][v].genotype
            triogenotype = childgeno + mumgeno + dadgeno
            variants['child'][v].set_triogenotype(triogenotype)
        elif variants['child'][v].is_cnv():
            #for a CNV trio genotype is determined from cifer inheritance
            childgeno = variants['child'][v].alt[1:4]
            if variants['child'][v].cnv_inh == 'not_inherited':
                parentgeno = 'REFREF'
            elif variants['child'][v].cnv_inh == 'maternal_inh':
                parentgeno = childgeno + 'REF'
            elif variants['child'][v].cnv_inh == 'paternal_inh':
                parentgeno = 'REF' + childgeno
            elif variants['child'][v].cnv_inh == 'biparental_inh':
                parentgeno = childgeno + childgeno
            else:
                logging.info(v + " Error: trio genotype for CNV can't be determined, CNV inh = " + variants['child'][v].cnv_inh)
                parentgeno = '??'
            triogenotype = childgeno + parentgeno
            variants['child'][v].set_triogenotype(triogenotype)
        else:
            print("Error: unrecognised variant type " + v)
            exit(1)

def add_trio_genotypes_no_parents(variants):
    '''add trio genotypes in a dict of variants where there are no parents'''
    for v in variants['child'].keys():
        if variants['child'][v].is_snv():
            childgeno = variants['child'][v].genotype
        elif variants['child'][v].is_cnv():
            childgeno = variants['child'][v].alt[1:4]
        else:
            print("Error: unrecognised variant type " + v)
            exit(1)
        mumgeno = 'NA'
        dadgeno = 'NA'
        triogenotype = childgeno + mumgeno + dadgeno
        variants['child'][v].set_triogenotype(triogenotype)

def add_trio_genotypes_mum_only(variants):
    '''add trio genotypes in a dict of variants where there is mum only'''
    for v in variants['child'].keys():
        if variants['child'][v].is_snv():
            childgeno = variants['child'][v].genotype
            mumgeno = '0'
            dadgeno = 'NA'
            if v in variants['mum'].keys():
                mumgeno = variants['mum'][v].genotype
            triogenotype = childgeno + mumgeno + dadgeno
            variants['child'][v].set_triogenotype(triogenotype)
        elif variants['child'][v].is_cnv():
            # todo improve when there is better inheritence prediction
            # for single parent CNVs
            childgeno = variants['child'][v].alt[1:4]
            mumgeno = 'NA'
            dadgeno = 'NA'
            triogenotype = childgeno + mumgeno + dadgeno
            variants['child'][v].set_triogenotype(triogenotype)
        else:
            print("Error: unrecognised variant type " + v)
            exit(1)

def add_trio_genotypes_dad_only(variants):
    '''add trio genotype in a dict of variants where there is dad only'''
    for v in variants['child'].keys():
        if variants['child'][v].is_snv():
            childgeno = variants['child'][v].genotype
            mumgeno = 'NA'
            dadgeno = '0'
            if v in variants['dad'].keys():
                dadgeno = variants['dad'][v].genotype
            triogenotype = childgeno + mumgeno + dadgeno
            variants['child'][v].set_triogenotype(triogenotype)
        elif variants['child'][v].is_cnv():
            #todo improve when there is better inheritence prediction
            # for single parent CNVs
            childgeno = variants['child'][v].alt[1:4]
            mumgeno = 'NA'
            dadgeno = 'NA'
            triogenotype = childgeno + mumgeno + dadgeno
            variants['child'][v].set_triogenotype(triogenotype)
        else:
            print("Error: unrecognised variant type " + v)
            exit(1)




import unittest
import copy

from tests.test_utils import create_test_candidate_vars
from tests.test_utils import create_test_person
from tests.test_utils import create_test_family
from tests.test_utils import create_test_variants_per_gene

class TestAutosomalInheritanceFilter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.child = create_test_person('fam', 'child_id', 'dad_id', 'mum_id',
                                        'XY', '2', '/vcf/path')
        self.mum = create_test_person('fam', 'mum_id', '0', '0', 'XX', '1',
                                      '/vcf/path')
        self.mum_aff = create_test_person('fam', 'mum_id', '0', '0', 'XX', '2',
                                          '/vcf/path')
        self.dad = create_test_person('fam', 'dad_id', '0', '0', 'XY', '1',
                                      '/vcf/path')
        self.dad_aff = create_test_person('fam', 'dad_id', '0', '0', 'XY', '2',
                                          '/vcf/path')
        self.family_both_unaff = create_test_family(self.child, self.mum,
                                                    self.dad)
        self.family_mum_aff = create_test_family(self.child, self.mum_aff,
                                                 self.dad)
        self.family_dad_aff = create_test_family(self.child, self.mum,
                                                 self.dad_aff)
        self.family_both_aff = create_test_family(self.child, self.mum_aff,
                                                  self.dad_aff)

        self.genes_biallelic = {
            '1234': {'chr': '5', 'start': '10971836', 'end': '11904446',
                     'symbol': 'MECP2', 'status': {'Probable DD gene'},
                     'mode': {'Biallelic'},
                     'mechanism': {'Loss of function'}}
        }
        self.genes_monoallelic = copy.deepcopy(self.genes_biallelic)
        self.genes_monoallelic['1234']['mode'] = {'Monoallelic'}
        self.genes_hemizygous = copy.deepcopy(self.genes_biallelic)
        self.genes_hemizygous['1234']['mode'] = {'Hemizygous'}
        self.genes_hemizygous['1234']['chr'] = {'X'}
        self.genes_X_linked_dominant = copy.deepcopy(self.genes_hemizygous)
        self.genes_X_linked_dominant['1234']['mode'] = {'X-linked dominant'}

        self.cn0vardata = {'chrom': '1', 'pos': '10971936', 'ref': 'T', 'alt': '<DEL>',
             'consequence': 'transcript_ablation', 'ensg': 'ENSG01234',
             'symbol': 'MECP1', 'feature': 'ENST01234', 'canonical': 'YES',
             'mane': 'NM01234', 'hgnc_id': 'HGNC:123', 'cnv_filter': 'Pass',
             'hgcn_id_all': 'HGNC:1|HGNC:2|HGNC:3',
             'symbol_all': 'MECP1|MECP2|MECP3', 'sex': 'XY', 'cn': '0',
             'cnv_inh':'biparental_inh'}

    def test_inh_matches_parent_aff_status(self):
        #pass if paternal and dad affected
        #fail if paternal and dad unaffected
        # pass if maternal and mum affected
        # fail if maternal and mum unaffected
        #pass if biparental and cn = 0
        #pass if biparental and either/both parents affected
        #fail if biparental, cn = 1 and parents both unaff
        #pass if male, X, maternal inh and mum unaffected
        # pass if male, X, maternal inh and mum affected(?)
        pass

    def test_non_ddg2p_filter(self):
        #should pass if cnv length > 1000000, fail if smaller and no ddg2p overlap
        pass

    def test_ddg2p_filter(self):
        # - fail duplications which completely surround monoallelic, hemizygous and
        #   x-linked dominant genes with loss of function mechanism
        # - Biallelic gene pass if copy number (CN) = 0 and mechanism in
        #   Uncertain", "Loss of function", "Dominant negative"
        # - Monoallelic, X-linked dominant or Hemizygous in male pass if CN=0,
        #   1 or 3 and any mechanism
        # - Hemizygous in female pass if CN=3 and mechanism = "Increased gene
        #   dosage"
        # - Pass intragenic DUP in monoallelic or X-linked dominant gene with
        #   loss of function mechanism and any part of the gene is outside of the CNV boundary
        pass

    def test_candidate_compound_het_filter(self):
        # add var to candidate compound hets if:
        # cn = 1 or 3 and biallelic and DDG2P gene
        # or if cn = 1, male, hemizygous and DDG2P gene
        pass


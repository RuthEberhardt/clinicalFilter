import unittest

from tests.test_utils import create_test_candidate_vars
from tests.test_utils import create_test_person
from tests.test_utils import create_test_family
from tests.test_utils import create_test_variants_per_gene

from variants.trio_genotype import add_trio_genotypes
from filtering.inheritance_filtering import InheritanceFiltering


class TestAutosomalInheritanceFilter(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.hetvardata = {'chrom': '5', 'pos': '10971838', 'ref': 'A',
                           'alt': 'GG',
                           'consequence': 'start_lost', 'ensg': 'ensg',
                           'symbol': 'MECP2', 'feature': 'feature',
                           'canonical': 'YES', 'mane': 'MANE',
                           'hgnc_id': '1234',
                           'max_af': '0', 'max_af_pops': '.', 'ddd_af': '0',
                           'revel': '.', 'polyphen': '.', 'hgvsc': '.',
                           'hgvsp': '.', 'sex': 'XY', 'denovo_snv': False,
                           'denovo_indel': False, 'gt': '0/1', 'gq': '50',
                           'pid': '.', 'protein_position': '123', 'ad': '4,4'}
        self.homaltvardata = self.hetvardata.copy()
        self.homaltvardata['gt'] = '1/1'
        self.homrefvardata = self.hetvardata.copy()
        self.homrefvardata['gt'] = '0/0'

        self.variants_100 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_101 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_110 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_111 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_102 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}
        self.variants_120 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_112 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}
        self.variants_121 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_122 = {'child': {'5_10971838_A_GG': self.hetvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}
        self.variants_200 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_201 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_210 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_211 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_202 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homrefvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}
        self.variants_220 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.homrefvardata}}
        self.variants_212 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.hetvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}
        self.variants_221 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.hetvardata}}
        self.variants_222 = {'child': {'5_10971838_A_GG': self.homaltvardata},
                    'mum': {'5_10971838_A_GG': self.homaltvardata},
                    'dad': {'5_10971838_A_GG': self.homaltvardata}}

        self.genes_biallelic = {
            '1234': {'chr': '5', 'start': '10971836', 'end': '11904446',
                     'symbol': 'MECP2', 'status': {'Probable DD gene'},
                     'mode': {'Biallelic'},
                     'mechanism': {'Loss of function'}}
        }

        self.genes_monoallelic = {
            '1234': {'chr': '5', 'start': '10971836', 'end': '11904446',
                     'symbol': 'MECP2', 'status': {'Probable DD gene'},
                     'mode': {'Monoallelic'},
                     'mechanism': {'Loss of function'}}
        }

        self.genes_mosaic = {
            '1234': {'chr': '5', 'start': '10971836', 'end': '11904446',
                     'symbol': 'MECP2', 'status': {'Probable DD gene'},
                     'mode': {'Mosaic'},
                     'mechanism': {'Loss of function'}}
        }

        self.genes_imprinted = {
            '1234': {'chr': '5', 'start': '10971836', 'end': '11904446',
                     'symbol': 'MECP2', 'status': {'Probable DD gene'},
                     'mode': {'Imprinted'},
                     'mechanism': {'Loss of function'}}
        }

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

    def test_biallelic_heterozygous_parents_filter(self):

        # parents both aff and 0/0 pass (will fail later stage as 2xDNM not allowed in compound het)
        variants_per_gene_100 = create_test_variants_per_gene(self.variants_100,
                                                          self.family_both_aff)
        inheritancefilter_100 = InheritanceFiltering(variants_per_gene_100,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_100.inheritance_filter_genes()
        test_candidate_variants_compound_het_100 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_100[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_100.candidate_variants,
                         test_candidate_variants_compound_het_100)

        # parents both aff and 0/1 pass
        variants_per_gene_111 = create_test_variants_per_gene(self.variants_111,
                                                          self.family_both_aff)
        inheritancefilter_111 = InheritanceFiltering(variants_per_gene_111,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_111.inheritance_filter_genes()
        test_candidate_variants_compound_het_111 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_111[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_111.candidate_variants,
                         test_candidate_variants_compound_het_111)
        # parents both aff, mum 0/1, dad 0/0 pass
        variants_per_gene_110 = create_test_variants_per_gene(self.variants_110,
                                                          self.family_both_aff)
        inheritancefilter_110 = InheritanceFiltering(variants_per_gene_110,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_110.inheritance_filter_genes()
        test_candidate_variants_compound_het_110 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_110[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_110.candidate_variants,
                         test_candidate_variants_compound_het_110)
        # parents both aff, mum 0/1, dad 1/1 pass
        variants_per_gene_112 = create_test_variants_per_gene(self.variants_112,
                                                          self.family_both_aff)
        inheritancefilter_112 = InheritanceFiltering(variants_per_gene_112,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_112.inheritance_filter_genes()
        test_candidate_variants_compound_het_112 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_112[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_112.candidate_variants,
                         test_candidate_variants_compound_het_112)
        # parents both aff, mum 0/0, dad 1/1 pass
        variants_per_gene_102 = create_test_variants_per_gene(self.variants_102,
                                                          self.family_both_aff)
        inheritancefilter_102 = InheritanceFiltering(variants_per_gene_102,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_102.inheritance_filter_genes()
        test_candidate_variants_compound_het_102 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_102[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_102.candidate_variants,
                         test_candidate_variants_compound_het_102)
        # parents both aff, mum 0/0, dad 0/1 pass
        variants_per_gene_101 = create_test_variants_per_gene(self.variants_101,
                                                          self.family_both_aff)
        inheritancefilter_101 = InheritanceFiltering(variants_per_gene_101,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_101.inheritance_filter_genes()
        test_candidate_variants_compound_het_101 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_101[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_101.candidate_variants,
                         test_candidate_variants_compound_het_101)
        # parents both aff, mum 1/1, dad 0/1 pass
        variants_per_gene_121 = create_test_variants_per_gene(self.variants_121,
                                                          self.family_both_aff)
        inheritancefilter_121 = InheritanceFiltering(variants_per_gene_121,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_121.inheritance_filter_genes()
        test_candidate_variants_compound_het_121 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_121[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_121.candidate_variants,
                         test_candidate_variants_compound_het_121)
        # parents both aff, mum 1/1, dad 0/0 pass
        variants_per_gene_120 = create_test_variants_per_gene(self.variants_120,
                                                          self.family_both_aff)
        inheritancefilter_120 = InheritanceFiltering(variants_per_gene_120,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_120.inheritance_filter_genes()
        test_candidate_variants_compound_het_120 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_120[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_120.candidate_variants,
                         test_candidate_variants_compound_het_120)
        # parents both aff and 1/1 fail
        variants_per_gene_122 = create_test_variants_per_gene(self.variants_122,
                                                          self.family_both_aff)
        inheritancefilter_122 = InheritanceFiltering(variants_per_gene_122,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_122.inheritance_filter_genes()
        test_candidate_variants_compound_het_122 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_122.candidate_variants,
                         test_candidate_variants_compound_het_122)

        # mum aff and both 0/0 pass
        variants_per_gene_100 = create_test_variants_per_gene(self.variants_100,
                                                          self.family_mum_aff)
        inheritancefilter_100 = InheritanceFiltering(variants_per_gene_100,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_100.inheritance_filter_genes()
        test_candidate_variants_compound_het_100 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_100[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_100.candidate_variants,
                         test_candidate_variants_compound_het_100)
        # mum aff and both 0/1 pass
        variants_per_gene_111 = create_test_variants_per_gene(self.variants_111,
                                                          self.family_mum_aff)
        inheritancefilter_111 = InheritanceFiltering(variants_per_gene_111,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_111.inheritance_filter_genes()
        test_candidate_variants_compound_het_111 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_111[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_111.candidate_variants,
                         test_candidate_variants_compound_het_111)
        # mum aff, mum 0/1, dad 0/0 pass
        variants_per_gene_110 = create_test_variants_per_gene(self.variants_110,
                                                          self.family_mum_aff)
        inheritancefilter_110 = InheritanceFiltering(variants_per_gene_110,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_110.inheritance_filter_genes()
        test_candidate_variants_compound_het_110 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_110[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_110.candidate_variants,
                         test_candidate_variants_compound_het_110)
        # mum aff, mum 0/1, dad 1/1 fail
        variants_per_gene_112 = create_test_variants_per_gene(self.variants_112,
                                                          self.family_mum_aff)
        inheritancefilter_112 = InheritanceFiltering(variants_per_gene_112,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_112.inheritance_filter_genes()
        test_candidate_variants_compound_het_112 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_112.candidate_variants,
                         test_candidate_variants_compound_het_112)
        # mum aff, mum 0/0, dad 1/1 fail
        variants_per_gene_102 = create_test_variants_per_gene(self.variants_102,
                                                          self.family_mum_aff)
        inheritancefilter_102 = InheritanceFiltering(variants_per_gene_102,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_102.inheritance_filter_genes()
        test_candidate_variants_compound_het_102 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_102.candidate_variants,
                         test_candidate_variants_compound_het_102)
        # mum aff, mum 0/0, dad 0/1 pass
        variants_per_gene_101 = create_test_variants_per_gene(self.variants_101,
                                                          self.family_mum_aff)
        inheritancefilter_101 = InheritanceFiltering(variants_per_gene_101,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_101.inheritance_filter_genes()
        test_candidate_variants_compound_het_101 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_101[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_101.candidate_variants,
                         test_candidate_variants_compound_het_101)
        # mum aff, mum 1/1, dad 0/1 pass
        variants_per_gene_121 = create_test_variants_per_gene(self.variants_121,
                                                          self.family_mum_aff)
        inheritancefilter_121 = InheritanceFiltering(variants_per_gene_121,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_121.inheritance_filter_genes()
        test_candidate_variants_compound_het_121 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_121[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_121.candidate_variants,
                         test_candidate_variants_compound_het_121)
        # mum aff, mum 1/1, dad 0/0 pass
        variants_per_gene_120 = create_test_variants_per_gene(self.variants_120,
                                                          self.family_mum_aff)
        inheritancefilter_120 = InheritanceFiltering(variants_per_gene_120,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_120.inheritance_filter_genes()
        test_candidate_variants_compound_het_120 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_120[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_120.candidate_variants,
                         test_candidate_variants_compound_het_120)
        # mum aff and both 1/1 fail
        variants_per_gene_122 = create_test_variants_per_gene(self.variants_122,
                                                          self.family_mum_aff)
        inheritancefilter_122 = InheritanceFiltering(variants_per_gene_122,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_122.inheritance_filter_genes()
        test_candidate_variants_compound_het_122 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_122.candidate_variants,
                         test_candidate_variants_compound_het_122)

        # dad aff and both 0/0 pass
        variants_per_gene_100 = create_test_variants_per_gene(self.variants_100,
                                                          self.family_dad_aff)
        inheritancefilter_100 = InheritanceFiltering(variants_per_gene_100,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_100.inheritance_filter_genes()
        test_candidate_variants_compound_het_100 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_100[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_100.candidate_variants,
                         test_candidate_variants_compound_het_100)
        # dad aff and both 0/1 pass
        variants_per_gene_111 = create_test_variants_per_gene(self.variants_111,
                                                          self.family_dad_aff)
        inheritancefilter_111 = InheritanceFiltering(variants_per_gene_111,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_111.inheritance_filter_genes()
        test_candidate_variants_compound_het_111 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_111[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_111.candidate_variants,
                         test_candidate_variants_compound_het_111)
        # dad aff, mum 0/1, dad 0/0 pass
        variants_per_gene_110 = create_test_variants_per_gene(self.variants_110,
                                                          self.family_dad_aff)
        inheritancefilter_110 = InheritanceFiltering(variants_per_gene_110,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_110.inheritance_filter_genes()
        test_candidate_variants_compound_het_110 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_110[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_110.candidate_variants,
                         test_candidate_variants_compound_het_110)
        # dad aff, mum 0/1, dad 1/1 pass
        variants_per_gene_112 = create_test_variants_per_gene(self.variants_112,
                                                          self.family_dad_aff)
        inheritancefilter_112 = InheritanceFiltering(variants_per_gene_112,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_112.inheritance_filter_genes()
        test_candidate_variants_compound_het_112 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_112[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_112.candidate_variants,
                         test_candidate_variants_compound_het_112)
        # dad aff, mum 0/0, dad 1/1 pass
        variants_per_gene_102 = create_test_variants_per_gene(self.variants_102,
                                                          self.family_dad_aff)
        inheritancefilter_102 = InheritanceFiltering(variants_per_gene_102,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_102.inheritance_filter_genes()
        test_candidate_variants_compound_het_102 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_102[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_102.candidate_variants,
                         test_candidate_variants_compound_het_102)
        # dad aff, mum 0/0, dad 0/1 pass
        variants_per_gene_101 = create_test_variants_per_gene(self.variants_101,
                                                          self.family_dad_aff)
        inheritancefilter_101 = InheritanceFiltering(variants_per_gene_101,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_101.inheritance_filter_genes()
        test_candidate_variants_compound_het_101 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_101[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_101.candidate_variants,
                         test_candidate_variants_compound_het_101)
        # dad aff, mum 1/1, dad 0/1 fail
        variants_per_gene_121 = create_test_variants_per_gene(self.variants_121,
                                                          self.family_dad_aff)
        inheritancefilter_121 = InheritanceFiltering(variants_per_gene_121,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_121.inheritance_filter_genes()
        test_candidate_variants_compound_het_121 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_121.candidate_variants,
                         test_candidate_variants_compound_het_121)
        # dad aff, mum 1/1, dad 0/0 fail
        variants_per_gene_120 = create_test_variants_per_gene(self.variants_120,
                                                          self.family_dad_aff)
        inheritancefilter_120 = InheritanceFiltering(variants_per_gene_120,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_120.inheritance_filter_genes()
        test_candidate_variants_compound_het_120 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_120.candidate_variants,
                         test_candidate_variants_compound_het_120)
        # dad aff and both 1/1 fail
        variants_per_gene_122 = create_test_variants_per_gene(self.variants_122,
                                                          self.family_dad_aff)
        inheritancefilter_122 = InheritanceFiltering(variants_per_gene_122,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_122.inheritance_filter_genes()
        test_candidate_variants_compound_het_122 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_122.candidate_variants,
                         test_candidate_variants_compound_het_122)

        # both unaff and 0/0 pass
        variants_per_gene_100 = create_test_variants_per_gene(self.variants_100,
                                                          self.family_both_unaff)
        inheritancefilter_100 = InheritanceFiltering(variants_per_gene_100,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_100.inheritance_filter_genes()
        test_candidate_variants_compound_het_100 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_100[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_100.candidate_variants,
                         test_candidate_variants_compound_het_100)
        # both unaff and 0/1 pass
        variants_per_gene_111 = create_test_variants_per_gene(self.variants_111,
                                                          self.family_both_unaff)
        inheritancefilter_111 = InheritanceFiltering(variants_per_gene_111,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_111.inheritance_filter_genes()
        test_candidate_variants_compound_het_111 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_111[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_111.candidate_variants,
                         test_candidate_variants_compound_het_111)
        # both unaff, mum 0/1, dad 0/0 pass
        variants_per_gene_110 = create_test_variants_per_gene(self.variants_110,
                                                          self.family_both_unaff)
        inheritancefilter_110 = InheritanceFiltering(variants_per_gene_110,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_110.inheritance_filter_genes()
        test_candidate_variants_compound_het_110 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_110[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_110.candidate_variants,
                         test_candidate_variants_compound_het_110)
        # both unaff, mum 0/1, dad 1/1 fail
        variants_per_gene_112 = create_test_variants_per_gene(self.variants_112,
                                                          self.family_both_unaff)
        inheritancefilter_112 = InheritanceFiltering(variants_per_gene_112,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_112.inheritance_filter_genes()
        test_candidate_variants_compound_het_112 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_112.candidate_variants,
                         test_candidate_variants_compound_het_112)
        # both unaff, mum 0/0, dad 1/1 fail
        variants_per_gene_102 = create_test_variants_per_gene(self.variants_102,
                                                          self.family_both_unaff)
        inheritancefilter_102 = InheritanceFiltering(variants_per_gene_102,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_102.inheritance_filter_genes()
        test_candidate_variants_compound_het_102 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_102.candidate_variants,
                         test_candidate_variants_compound_het_102)
        # both unaff, mum 0/0, dad 0/1 pass
        variants_per_gene_101 = create_test_variants_per_gene(self.variants_101,
                                                          self.family_both_unaff)
        inheritancefilter_101 = InheritanceFiltering(variants_per_gene_101,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_101.inheritance_filter_genes()
        test_candidate_variants_compound_het_101 = {'single_variants': {},
                                                'compound_hets': {'1234': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_101[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}}}
        self.assertEqual(inheritancefilter_101.candidate_variants,
                         test_candidate_variants_compound_het_101)
        # both unaff, mum 1/1, dad 0/1 fail
        variants_per_gene_121 = create_test_variants_per_gene(self.variants_121,
                                                          self.family_both_unaff)
        inheritancefilter_121 = InheritanceFiltering(variants_per_gene_121,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_121.inheritance_filter_genes()
        test_candidate_variants_compound_het_121 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_121.candidate_variants,
                         test_candidate_variants_compound_het_121)
        # both unaff, mum 1/1, dad 0/0 fail
        variants_per_gene_120 = create_test_variants_per_gene(self.variants_120,
                                                          self.family_both_unaff)
        inheritancefilter_120 = InheritanceFiltering(variants_per_gene_120,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_120.inheritance_filter_genes()
        test_candidate_variants_compound_het_120 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_120.candidate_variants,
                         test_candidate_variants_compound_het_120)
        # both unaff and 1/1 fail
        variants_per_gene_122 = create_test_variants_per_gene(self.variants_122,
                                                          self.family_both_unaff)
        inheritancefilter_122 = InheritanceFiltering(variants_per_gene_122,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_122.inheritance_filter_genes()
        test_candidate_variants_compound_het_122 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_122.candidate_variants,
                         test_candidate_variants_compound_het_122)

    def test_biallelic_homozygous_parents_filter(self):

        # parents both aff and 0/0 fail
        variants_per_gene_200 = create_test_variants_per_gene(self.variants_200,
                                                          self.family_both_aff)
        inheritancefilter_200 = InheritanceFiltering(variants_per_gene_200,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_200.inheritance_filter_genes()
        test_candidate_variants_200 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_200.candidate_variants,
                         test_candidate_variants_200)
        # parents both aff and 0/1 pass
        variants_per_gene_211 = create_test_variants_per_gene(self.variants_211,
                                                          self.family_both_aff)
        inheritancefilter_211 = InheritanceFiltering(variants_per_gene_211,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_211.inheritance_filter_genes()
        test_candidate_variants_211 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_211[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_211.candidate_variants,
                         test_candidate_variants_211)
        # parents both aff, mum 0/1, dad 0/0 fail
        variants_per_gene_210 = create_test_variants_per_gene(self.variants_210,
                                                          self.family_both_aff)
        inheritancefilter_210 = InheritanceFiltering(variants_per_gene_210,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_210.inheritance_filter_genes()
        test_candidate_variants_210 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_210.candidate_variants,
                         test_candidate_variants_210)
        # parents both aff, mum 0/1, dad 1/1 pass
        variants_per_gene_212 = create_test_variants_per_gene(self.variants_212,
                                                          self.family_both_aff)
        inheritancefilter_212 = InheritanceFiltering(variants_per_gene_212,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_212.inheritance_filter_genes()
        test_candidate_variants_212 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_212[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_212.candidate_variants,
                         test_candidate_variants_212)
        # parents both aff, mum 0/0, dad 1/1 fail
        variants_per_gene_202 = create_test_variants_per_gene(self.variants_202,
                                                          self.family_both_aff)
        inheritancefilter_202 = InheritanceFiltering(variants_per_gene_202,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_202.inheritance_filter_genes()
        test_candidate_variants_202 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_202.candidate_variants,
                         test_candidate_variants_202)
        # parents both aff, mum 0/0, dad 0/1 fail
        variants_per_gene_201 = create_test_variants_per_gene(self.variants_201,
                                                          self.family_both_aff)
        inheritancefilter_201 = InheritanceFiltering(variants_per_gene_201,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_201.inheritance_filter_genes()
        test_candidate_variants_201 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_201.candidate_variants,
                         test_candidate_variants_201)
        # parents both aff, mum 1/1, dad 0/1 pass
        variants_per_gene_221 = create_test_variants_per_gene(self.variants_221,
                                                          self.family_both_aff)
        inheritancefilter_221 = InheritanceFiltering(variants_per_gene_221,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_221.inheritance_filter_genes()
        test_candidate_variants_221 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_221[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_221.candidate_variants,
                         test_candidate_variants_221)
        # parents both aff, mum 1/1, dad 0/0 fail
        variants_per_gene_220 = create_test_variants_per_gene(self.variants_220,
                                                          self.family_both_aff)
        inheritancefilter_220 = InheritanceFiltering(variants_per_gene_220,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_220.inheritance_filter_genes()
        test_candidate_variants_220 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_220.candidate_variants,
                         test_candidate_variants_220)
        # parents both aff and 1/1 pass
        variants_per_gene_222 = create_test_variants_per_gene(self.variants_222,
                                                          self.family_both_aff)
        inheritancefilter_222 = InheritanceFiltering(variants_per_gene_222,
                                                 self.family_both_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_222.inheritance_filter_genes()
        test_candidate_variants_222 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_222[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_222.candidate_variants,
                         test_candidate_variants_222)

        # mum aff and both 0/0 fail
        variants_per_gene_200 = create_test_variants_per_gene(self.variants_200,
                                                          self.family_mum_aff)
        inheritancefilter_200 = InheritanceFiltering(variants_per_gene_200,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_200.inheritance_filter_genes()
        test_candidate_variants_200 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_200.candidate_variants,
                         test_candidate_variants_200)
        # mum aff and both 0/1 pass
        variants_per_gene_211 = create_test_variants_per_gene(self.variants_211,
                                                          self.family_mum_aff)
        inheritancefilter_211 = InheritanceFiltering(variants_per_gene_211,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_211.inheritance_filter_genes()
        test_candidate_variants_211 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_211[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_211.candidate_variants,
                         test_candidate_variants_211)
        # mum aff, mum 0/1, dad 0/0 fail
        variants_per_gene_210 = create_test_variants_per_gene(self.variants_210,
                                                          self.family_mum_aff)
        inheritancefilter_210 = InheritanceFiltering(variants_per_gene_210,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_210.inheritance_filter_genes()
        test_candidate_variants_210 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_210.candidate_variants,
                         test_candidate_variants_210)
        # mum aff, mum 0/1, dad 1/1 fail
        variants_per_gene_212 = create_test_variants_per_gene(self.variants_212,
                                                          self.family_mum_aff)
        inheritancefilter_212 = InheritanceFiltering(variants_per_gene_212,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_212.inheritance_filter_genes()
        test_candidate_variants_212 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_212.candidate_variants,
                         test_candidate_variants_212)
        # mum aff, mum 0/0, dad 1/1 fail
        variants_per_gene_202 = create_test_variants_per_gene(self.variants_202,
                                                          self.family_mum_aff)
        inheritancefilter_202 = InheritanceFiltering(variants_per_gene_202,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_202.inheritance_filter_genes()
        test_candidate_variants_202 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_202.candidate_variants,
                         test_candidate_variants_202)
        # mum aff, mum 0/0, dad 0/1 fail
        variants_per_gene_201 = create_test_variants_per_gene(self.variants_201,
                                                          self.family_mum_aff)
        inheritancefilter_201 = InheritanceFiltering(variants_per_gene_201,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_201.inheritance_filter_genes()
        test_candidate_variants_201 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_201.candidate_variants,
                         test_candidate_variants_201)
        # mum aff, mum 1/1, dad 0/1 pass
        variants_per_gene_221 = create_test_variants_per_gene(self.variants_221,
                                                          self.family_mum_aff)
        inheritancefilter_221 = InheritanceFiltering(variants_per_gene_221,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_221.inheritance_filter_genes()
        test_candidate_variants_221 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_221[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_221.candidate_variants,
                         test_candidate_variants_221)
        # mum aff, mum 1/1, dad 0/0 fail
        variants_per_gene_220 = create_test_variants_per_gene(self.variants_220,
                                                          self.family_mum_aff)
        inheritancefilter_220 = InheritanceFiltering(variants_per_gene_220,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_220.inheritance_filter_genes()
        test_candidate_variants_220 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_220.candidate_variants,
                         test_candidate_variants_220)
        # mum aff and both 1/1 fail
        variants_per_gene_222 = create_test_variants_per_gene(self.variants_222,
                                                          self.family_mum_aff)
        inheritancefilter_222 = InheritanceFiltering(variants_per_gene_222,
                                                 self.family_mum_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_222.inheritance_filter_genes()
        test_candidate_variants_222 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_222.candidate_variants,
                         test_candidate_variants_222)

        # dad aff and both 0/0 fail
        variants_per_gene_200 = create_test_variants_per_gene(self.variants_200,
                                                          self.family_dad_aff)
        inheritancefilter_200 = InheritanceFiltering(variants_per_gene_200,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_200.inheritance_filter_genes()
        test_candidate_variants_200 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_200.candidate_variants,
                         test_candidate_variants_200)
        # dad aff and both 0/1 pass
        variants_per_gene_211 = create_test_variants_per_gene(self.variants_211,
                                                          self.family_dad_aff)
        inheritancefilter_211 = InheritanceFiltering(variants_per_gene_211,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_211.inheritance_filter_genes()
        test_candidate_variants_211 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_211[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_211.candidate_variants,
                         test_candidate_variants_211)
        # dad aff, mum 0/1, dad 0/0 fail
        variants_per_gene_210 = create_test_variants_per_gene(self.variants_210,
                                                          self.family_dad_aff)
        inheritancefilter_210 = InheritanceFiltering(variants_per_gene_210,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_210.inheritance_filter_genes()
        test_candidate_variants_210 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_210.candidate_variants,
                         test_candidate_variants_210)
        # dad aff, mum 0/1, dad 1/1 pass
        variants_per_gene_212 = create_test_variants_per_gene(self.variants_212,
                                                          self.family_dad_aff)
        inheritancefilter_212 = InheritanceFiltering(variants_per_gene_212,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_212.inheritance_filter_genes()
        test_candidate_variants_212 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_212[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_212.candidate_variants,
                         test_candidate_variants_212)
        # dad aff, mum 0/0, dad 1/1 fail
        variants_per_gene_202 = create_test_variants_per_gene(self.variants_202,
                                                          self.family_dad_aff)
        inheritancefilter_202 = InheritanceFiltering(variants_per_gene_202,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_202.inheritance_filter_genes()
        test_candidate_variants_202 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_202.candidate_variants,
                         test_candidate_variants_202)
        # dad aff, mum 0/0, dad 0/1 fail
        variants_per_gene_201 = create_test_variants_per_gene(self.variants_201,
                                                          self.family_dad_aff)
        inheritancefilter_201 = InheritanceFiltering(variants_per_gene_201,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_201.inheritance_filter_genes()
        test_candidate_variants_201 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_201.candidate_variants,
                         test_candidate_variants_201)
        # dad aff, mum 1/1, dad 0/1 fail
        variants_per_gene_221 = create_test_variants_per_gene(self.variants_221,
                                                          self.family_dad_aff)
        inheritancefilter_221 = InheritanceFiltering(variants_per_gene_221,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_221.inheritance_filter_genes()
        test_candidate_variants_221 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_221.candidate_variants,
                         test_candidate_variants_221)
        # dad aff, mum 1/1, dad 0/0 fail
        variants_per_gene_220 = create_test_variants_per_gene(self.variants_220,
                                                          self.family_dad_aff)
        inheritancefilter_220 = InheritanceFiltering(variants_per_gene_220,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_220.inheritance_filter_genes()
        test_candidate_variants_220 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_220.candidate_variants,
                         test_candidate_variants_220)
        # dad aff and both 1/1 fail
        variants_per_gene_222 = create_test_variants_per_gene(self.variants_222,
                                                          self.family_dad_aff)
        inheritancefilter_222 = InheritanceFiltering(variants_per_gene_222,
                                                 self.family_dad_aff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_222.inheritance_filter_genes()
        test_candidate_variants_222 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_222.candidate_variants,
                         test_candidate_variants_222)

        # both unaff and 0/0 fail
        variants_per_gene_200 = create_test_variants_per_gene(self.variants_200,
                                                          self.family_both_unaff)
        inheritancefilter_200 = InheritanceFiltering(variants_per_gene_200,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_200.inheritance_filter_genes()
        test_candidate_variants_200 = {'single_variants': {},
                                                'compound_hets': {}}
        self.assertEqual(inheritancefilter_200.candidate_variants,
                         test_candidate_variants_200)
        # both unaff and 0/1 pass
        variants_per_gene_211 = create_test_variants_per_gene(self.variants_211,
                                                          self.family_both_unaff)
        inheritancefilter_211 = InheritanceFiltering(variants_per_gene_211,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_211.inheritance_filter_genes()
        test_candidate_variants_211 = {'single_variants': {
                                                    '5_10971838_A_GG': {
                                                        'mode': {'biallelic'},
                                                        'variant':
                                                            variants_per_gene_211[
                                                                '1234'][
                                                                '5_10971838_A_GG'][
                                                                'child'],
                                                        'hgncid': '1234'}}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_211.candidate_variants,
                         test_candidate_variants_211)
        # both unaff, mum 0/1, dad 0/0 fail
        variants_per_gene_210 = create_test_variants_per_gene(self.variants_210,
                                                          self.family_both_unaff)
        inheritancefilter_210 = InheritanceFiltering(variants_per_gene_210,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_210.inheritance_filter_genes()
        test_candidate_variants_210 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_210.candidate_variants,
                         test_candidate_variants_210)
        # both unaff, mum 0/1, dad 1/1 fail
        variants_per_gene_212 = create_test_variants_per_gene(self.variants_212,
                                                          self.family_both_unaff)
        inheritancefilter_212 = InheritanceFiltering(variants_per_gene_212,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_212.inheritance_filter_genes()
        test_candidate_variants_212 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_212.candidate_variants,
                         test_candidate_variants_212)
        # both unaff, mum 0/0, dad 1/1 fail
        variants_per_gene_202 = create_test_variants_per_gene(self.variants_202,
                                                          self.family_both_unaff)
        inheritancefilter_202 = InheritanceFiltering(variants_per_gene_202,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_202.inheritance_filter_genes()
        test_candidate_variants_202 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_202.candidate_variants,
                         test_candidate_variants_202)
        # both unaff, mum 0/0, dad 0/1 fail
        variants_per_gene_201 = create_test_variants_per_gene(self.variants_201,
                                                          self.family_both_unaff)
        inheritancefilter_201 = InheritanceFiltering(variants_per_gene_201,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_201.inheritance_filter_genes()
        test_candidate_variants_201 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_201.candidate_variants,
                         test_candidate_variants_201)
        # both unaff, mum 1/1, dad 0/1 fail
        variants_per_gene_221 = create_test_variants_per_gene(self.variants_221,
                                                          self.family_both_unaff)
        inheritancefilter_221 = InheritanceFiltering(variants_per_gene_221,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_221.inheritance_filter_genes()
        test_candidate_variants_221 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_221.candidate_variants,
                         test_candidate_variants_221)
        # both unaff, mum 1/1, dad 0/0 fail
        variants_per_gene_220 = create_test_variants_per_gene(self.variants_220,
                                                          self.family_both_unaff)
        inheritancefilter_220 = InheritanceFiltering(variants_per_gene_220,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_220.inheritance_filter_genes()
        test_candidate_variants_220 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_220.candidate_variants,
                         test_candidate_variants_220)
        # both unaff and 1/1 fail
        variants_per_gene_222 = create_test_variants_per_gene(self.variants_222,
                                                          self.family_both_unaff)
        inheritancefilter_222 = InheritanceFiltering(variants_per_gene_222,
                                                 self.family_both_unaff,
                                                 self.genes_biallelic, None,
                                                 None)
        inheritancefilter_222.inheritance_filter_genes()
        test_candidate_variants_222 = {'single_variants': {}, 'compound_hets': {}}
        self.assertEqual(inheritancefilter_222.candidate_variants,
                         test_candidate_variants_222)

    def test_monoallelic_heterozygous_parents_filter(self):
        pass

    def test_monoallelic_homozygous_parents_filter(self):
        pass

    def test_imprinted_heterozygous_parents_filter(self):
        pass

    def test_imprinted_homozygous_parents_filter(self):
        pass

    def test_mosaic_heterozygous_parents_filter(self):
        pass

    def test_mosaic_homozygous_parents_filter(self):
        pass

    def test_biallelic_heterozygous_no_parents_filter(self):
        pass

    def test_biallelic_homozygous_no_parents_filter(self):
        pass

    def test_monoallelic_heterozygous_no_parents_filter(self):
        pass

    def test_monoallelic_homozygous_no_parents_filter(self):
        pass

    def test_imprinted_heterozygous_no_parents_filter(self):
        pass

    def test_imprinted_homozygous_no_parents_filter(self):
        pass

    def test_mosaic_heterozygous_no_parents_filter(self):
        pass

    def test_mosaic_homozygous_no_parents_filter(self):
        pass

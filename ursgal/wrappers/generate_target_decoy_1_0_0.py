#!/usr/bin/env python3.4
import ursgal
import importlib
import os
import sys
import pprint

class generate_target_decoy_1_0_0( ursgal.UNode ):
    """Generate Target Decoy 1_0_0 UNode"""
    META_INFO = {
        'engine_type' : {
            'search_engine' : False,
            'converter'     : True
        },
        'output_extension' : '.fasta',
        'output_suffix'    : 'target_decoy',
        'input_types'      : [''],
        'in_development'   : False,
        'include_in_git'   : True,
        'utranslation_style'    : 'generate_target_decoy_style_1',
        'engine': {
            'platform_independent' : {
                'arc_independent' : {
                    'exe'     : 'generate_target_decoy_1_0_0.py',
                },
            },
        },

        # 'engine_exe'                : {
        #     'arc_independent' : 'generate_target_decoy_1_0_0.py',
        # },
        # 'engine_url' : {
        #     'internal' : True,
        # },
    }

    def __init__(self, *args, **kwargs):
        super(generate_target_decoy_1_0_0, self).__init__(*args, **kwargs)

    def _execute( self ):
        '''
        Creates a target decoy database based on shuffling of peptides or
        complete reversing the protein sequence.

        The engine currently available generates a very stringent target decoy
        database by peptide shuffling but also offers the possibility to
        simple reverse the protein sequence. The mode can be defined in the
        params with 'decoy_generation_mode'.

        The shuffling peptide method is described below.
        As one of the first steps redundant sequences are filtered and the
        protein gets a tag which highlight its double occurence in the database.
        This ensures that no unequal distribution of target and decoy peptides
        is present.
        Further, every peptide is shuffled, while the amindo acids where the
        enzyme cleaves aremaintained at their original position.
        Every peptide is only shuffled once and the shuffling result is stored.
        As a result it is ensured that if a peptide occurs multiple times it is
        shuffled the same way. It is further ensured that unmutable peptides
        (e.g. 'RR' for trypsin) are not shuffled and are reported by the engine
        as unmutable peptides in a text file, so that they can be excluded in
        the further analysis.
        This way of generating a target decoy database lead to the fulfillment
        of the following quality criteria (Proteome Bioinformatics,
        Eds: S.J. Hubbard, A.R. Jones, Humana Press ).

        Quality criteria:

            * every target peptide sequence has exactly one decoy peptide sequence
            * equal amino acid distribution
            * equal protein and peptide length
            * equal number of proteins and peptides
            * similar mass distribution
            * no predicted peptides in common


        Avaliable modes:

            * shuffle_peptide  - stringent target decoy generation with shuffling
                of peptides with maintaining the cleavage site amino acid.

            * reverse_protein - reverses the protein sequence


        Available enzymes and their cleavage site can be found in the knowledge
        base of generate_target_decoy_1_0_0.

        '''
        
        print('[ -ENGINE- ] Executing conversion ..')
        self.time_point(tag = 'execution')
        generate_target_decoy_main = self.import_engine_as_python_function()

        input_files = []
        if 'input_file_dicts' in self.params.keys():
            for input_file_dict in self.params['input_file_dicts']:
                input_files.append(
                    os.path.join(
                        input_file_dict['dir'],
                        input_file_dict['file']
                    )
                )
        else:
            input_files.append(
                os.path.join(
                    self.io['input']['finfo']['dir'],
                    self.io['input']['finfo']['file']
                )
            )

        self.params['translations']['output_file_incl_path'] = os.path.join(
            self.params['output_dir_path'],
            self.params['output_file']
        )

        generate_target_decoy_main(
            input_files = input_files,
            output_file = self.params['translations']['output_file_incl_path'],
            enzyme      = self.params['translations']['enzyme'],
            mode        = self.params['translations']['decoy_generation_mode'],
            decoy_tag   = self.params['translations']['decoy_tag']
        )

        self.print_execution_time(tag='execution')
        return self.params['output_file_incl_path']

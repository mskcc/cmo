from setuptools import setup

setup(name='cmo',
        version='0.1',
        description='Center for Molecular Oncology Python Package for Great Convenience and Enhanced Double Plus User Experiences',
        url='github.com/mskcc/mskcmo.git',
        author='Chris Harris',
        author_email='harrisc2@mskcc.org',
        licence='GPLv3',
        packages=['cmo'],
        install_requires=['argparse'],
        scripts=['bin/cmo_bwa_sampe',
                 'bin/cmo_bwa_aln',
                 'bin/cmo_bwa_mem',
                 'bin/cmo_picard',
                 'bin/cmo_gatk',
                 'bin/cmo_mutect',
                 'bin/cmo_bedtools'
                 ],
        zip_safe=False)


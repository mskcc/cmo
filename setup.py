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
        scripts=['bin/bwa_sampe',
                 'bin/bwa_align_paired_end',
                 'bin/bwa_aln',
                 'bin/bwa_mem'],
        zip_safe=False)


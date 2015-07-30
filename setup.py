from setuptools import setup

setup(name='mskcmo',
        version='0.1',
        description='Center for Molecular Oncology Python Package for Great Convenience and Enhanced Double Plus User Experiences',
        url='github.com/mskcc/mskcmo.git',
        author='Chris Harris',
        author_email='harrisc2@mskcc.org',
        licence='GPLv3',
        packages=['mskcmo'],
        install_requires=['argparse'],
        scripts=['bin/bwa_sampe',
                 'bin/bwa_align_paired_end',
                 'bin/bwa_aln'],
        zip_safe=False)


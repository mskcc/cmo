from setuptools import setup, find_packages
import os, subprocess, re, sys

VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.

__version__ = '%s'
"""

def update_version_py():
    if not os.path.isdir(".git"):
        print "This does not appear to be a Git repository."
        return
    try:
        p = subprocess.Popen(["git", "describe",
        "--tags", "--dirty", "--always"],
        stdout=subprocess.PIPE)
    except EnvironmentError:
        print "unable to run git, leaving cmo/_version.py alone"
        return
    stdout = p.communicate()[0]
    if p.returncode != 0:
        print "unable to run git, leaving cmo/_version.py alone"
        return
    ver = "1.0+"+stdout.strip()
    if ver.find("-dirty") > -1:
        print >>sys.stderr,  "REFUSING TO INSTALL DIRTY TREE! COMMIT TO TRUNK OR BRANCH!"
        #sys.exit(1)
    f = open("cmo/_version.py", "w")
    f.write(VERSION_PY % ver)
    f.close()
    print "set cmo/_version.py to '%s'" % ver

def get_version():
    try:
        f = open("cmo/_version.py")
    except EnvironmentError:
        return None
    for line in f.readlines():
        mo = re.match("__version__ = '([^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None

#class Version(Command):
#    description = "update _version.py from Git repo"
#    user_options = []
#    boolean_options = []
#    def initialize_options(self):
#        pass
#    def finalize_options(self):
#        pass
#    def run(self):
#        update_version_py()
#    print "Version is now", get_version()

#class sdist(_sdist):
#    def run(self):
#        update_version_py()
#        # unless we update this, the sdist command will keep using the old
#        # version
#        self.distribution.metadata.version = get_version()
#        return _sdist.run(self)


##make _version.py
#update_version_py();
#use its value in setuptools
setup(name='cmo',
        version=get_version(),
        description='Center for Molecular Oncology Python Package for Great Convenience and Enhanced Double Plus User Experiences',
        url='github.com/mskcc/cmo.git',
        author='Chris Harris',
        author_email='harrisc2@mskcc.org',
        licence='GPLv3',
        packages=find_packages(),
        dependency_links=['https://github.com/cemsbr/python-daemon/tarball/latest_release#egg=python-daemon-2.1.2'],
        install_requires=['argparse','requests', 'fireworks', 'python-daemon==2.1.2', 'filemagic'],
        scripts=['bin/cmo_bwa_sampe',
                 'bin/cmo_getbasecounts',
                 'bin/cmo_facets',
                 'bin/cmoflow_facets',
                 'bin/cmoflow_postprocess',
                 'bin/cmo_bwa_aln',
                 'bin/cmo_watcher',
                 'bin/cmo_bwa_mem',
                 'bin/cmo_picard',
                 'bin/cmo_gatk',
                 'bin/cmo_mutect',
                 'bin/cmo_bedtools',
                 'bin/cmo_maf2maf',
                 'bin/cmo_vcf2maf',
                 'bin/cmo_vcf2vcf',
                 'bin/cmo_maf2vcf',
                 'bin/cmo_filter_haplotype',
                 'bin/cmo_filter_mutect',
                 'bin/cmo_merge_mafs',
                 'bin/cmo_trinuc_and_impact',
                 'bin/cmo_add_variant_info',
                 'bin/cmo_mutsig',
                 'bin/cmo_make_facets_file',
                 'bin/cmo_abra',
                 'bin/cmo_qcpdf',
                 'bin/cmoflow_reference_alignment',
                 'bin/cmo_split_reads',
                 'bin/cmo_samstat',
                 'bin/cmo_taskmod',
                 'bin/cmo_rerun',
                 'bin/cmo_gdc',
                 'bin/cmoflow_rnaseq',
                 'bin/cmo_snp-pileup',
                 'bin/cmo_ppflag-fixer',
                 'bin/cmo_trimgalore',
                 'bin/cmo_vardict',
                 'bin/cmo_list2bed',
                 'bin/cmo_pindel',
                 'bin/cmo_bcftools',
                 'bin/cmo_index',
                 'bin/cmo_fillout',
                 'bin/cmo_file_of_files'
                 #'bin/cmo_hotspot3d'
                 ],
        zip_safe=False)


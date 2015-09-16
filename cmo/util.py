from collections import defaultdict
import json, subprocess, sys, re
#STRAWMAN FIXME
#THIS WOULD BE A PROGRAMMATICALLY INGESTED JSON ON MODULE LOAD IN REAL LIFE
#DONT HATE THIS PART
#programs = defaultdict(dict)
#programs['bwa']={"default":"/opt/common/CentOS_6/bwa/bwa-0.7.12/bwa",
#                 "0.7.12":"/opt/common/CentOS_6/bwa/bwa-0.7.12/bwa",
#                 "0.7.10":"/opt/common/CentOS_6/bwa/bwa-0.7.10/bwa"
#                 }
#programs['samtools']={"default":"/opt/common/CentOS_6/samtools/samtools-0.1.19/samtools",
#                      "0.1.19":"/opt/common/CentOS_6/samtools/samtools-0.1.19/samtools"}
#genomes = defaultdict(dict)
#genomes['hg19']={"fasta":"/ifs/depot/assemblies/H.sapiens/hg19/hg19.fasta"}
json_config = json.load(open("/opt/common/CentOS_6-dev/cmo/cmo_resources.json"))
programs = json_config['programs']
genomes = json_config['genomes']
chr1_fingerprints = json_config['chr1_fingerprints']

def infer_fasta_from_bam(bam_file):
    get_chr1_cmd= [programs['samtools']['default'], "view -H", bam_file, "| fgrep \"@SQ\" |  head -1 | awk '{print $2,$3}'"]
    chr1_tag = subprocess.Popen(" ".join(get_chr1_cmd), shell=True, stdout=subprocess.PIPE, stderr=open("/dev/null")).communicate()[0]
    (chr_name, length) = chr1_tag.strip().split(" ")
    chr_name = chr_name[3:]
    length = length[3:]
    for candidate in chr1_fingerprints:
        if chr1_fingerprints[candidate]['name']==chr_name and chr1_fingerprints[candidate]['length']==int(length):
            print >>sys.stderr, "Inferred genome to be %s" % candidate
            return (candidate, genomes[candidate]['fasta'])
    print >>sys.stderr, "Chromoosome 1 name %s, length %s, doesn't match any standard refs?" % (chr_name, length)
    return (None, None)

def infer_sample_from_bam(bam_file):
    get_rg_cmd= [programs['samtools']['default'], "view -H", bam_file, "| fgrep \"@RG\" "]
    rg_lines = subprocess.Popen(" ".join(get_rg_cmd), shell=True, stdout=subprocess.PIPE, stderr=open("/dev/null")).communicate()[0]
    sample_dict = {}
    for rg in rg_lines.splitlines():
        print rg
        tags = rg.split("\t")
        for tag in tags:
            if tag[0:2]=="SM":
                sample_dict[tag[3:]]=1
    if len(sample_dict.keys()) > 1:
                    print >>sys.stderr, "Mixed sample tags in Read Group header for %, can't infer a single sample name from this bam naively" % bam_file
    elif len(sample_dict.keys()) == 1:
        print >>sys.stderr, "Found one sample key for this bam: %s" % sample_dict.keys()[0]
        return sample_dict.keys()[0]
    else:
        #we didnt find any RG with SM: at all :(
        print >>sys.stderr, "No @RG lines with SM: tags found in %s, can't infer sample" % bam_file
    return None

def filesafe_string(string):
    keepcharacters = ('.','_')
    return  "".join(c for c in string if c.isalnum() or c in keepcharacters).rstrip()



def call_cmd(cmd, shell=True, stderr=None, stdout=None, stdin=None):
    try:
        if(stderr):
            error_fh = open(stderr, "w")
            stderr = error_fh
            #FIXME log that this happened
        if(stdout):
            out_fh = open(stdout, "w")
            stdout = out_fh
            #FIXME log that this happened
        return_code = subprocess.check_call(cmd, shell=shell, stderr=stderr, stdout=stdout, stdin=stdin)
    except subprocess.CalledProcessError, e:
        print >>sys.stderr, "Non Zero Exit Code %s from %s" % (e.returncode, cmd)
        print >>sys.stderr, "Bailing out!"
        sys.exit(1)
    except IOError, e:
        print >>sys.stderr, e
        print >>sys.stderr, "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(1)

logging_options = [
        ("--stderr", "log stderr to file"),
        ("--stdout", "log stdout to file"),
        ]

def add_logging_options(parser):
    for (arg, help) in logging_options:
        parser.add_argument(arg, default=None, help=help)

def remove_logging_options_from_dict(dict):
        for (arg, help) in logging_options:
            key = arg.replace("--","")
            if key in dict:
                del dict[key]


VT_LOCATION = '/home/charris/code/VCF_accuracy_evaluator/vt/vt'
TABIX_LOCATION = '/opt/common/CentOS_6/samtools/samtools-1.2/htslib-1.2.1/tabix'
BGZIP_LOCATION = '/opt/common/CentOS_6/samtools/samtools-1.2/htslib-1.2.1/bgzip'
SORTBED_LOCATION = '/opt/common/CentOS_6/bedtools/bedtools-2.22.0/bin/sortBed'

def sort_vcf(vcf):

    outfile = vcf.replace('.vcf', '.sorted.vcf')
    cmd = [SORTBED_LOCATION, '-i', vcf, '-header']
    print >> sys.stdout, 'sortBed command: %s'%(' '.join(cmd))
    #logger.debug('sortBed command: %s'%(' '.join(cmd)))
    try:
        rv = subprocess.check_call(cmd, stdout=open(outfile,'w'))
        return outfile
    except subprocess.CalledProcessError, e:
        print >> sys.stderr, "Non-zero exit code from sortBed! Bailing out."
        #logger.critical("Non-zero exit code from sortBed! Bailing out.")
        sys.exit(1)

    
def bgzip(vcf):

    if re.search('.gz', vcf):
        return vcf
    outfile = '%s.gz'%(vcf)
    cmd = [BGZIP_LOCATION, '-c', vcf]
    #logger.debug('BGZIP COMMAND: %s'%(' '.join(cmd)))
    print >> sys.stderr, 'BGZIP COMMAND: %s'%(' '.join(cmd))
    subprocess.call(cmd, stdout=open(outfile, 'w'))
    return outfile


def tabix_file(vcf_file):

    ''' index a vcf file with tabix for random access'''
    with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
        if(m.id_filename(vcf_file).find('gz') == -1):
            print >> sys.stderr, 'VCF File needs to be bgzipped for tabix random access. tabix-0.26/bgzip should be compiled for use'
            #logger.critical('VCF File needs to be bgzipped for tabix random access. tabix-0.26/bgzip should be compiled for use')
            sys.exit(1)
    cmd = [TABIX_LOCATION, '-p' , 'vcf', vcf_file]
    print >> sys.stdout, 'Tabix command: %s'%(' '.join(cmd))
    #logger.debug('Tabix command: %s'%(' '.join(cmd)))
    try:
        rv = subprocess.check_call(cmd)
    except subprocess.CalledProcessError, e:
        print >> sys.stderr, 'Non-zero exit code from Tabix! Bailing out.'
        #logger.critical('Non-zero exit code from Tabix! Bailing out.')
        sys.exit(1)


def normalize_vcf(vcf_file, ref_fasta):
    sorted_vcf = sort_vcf(vcf_file)
    zipped_file = bgzip(sorted_vcf)
    tabix_file(zipped_file)
    output_vcf = zipped_file.replace('.vcf', '.normalized.vcf')
    cmd = [VT_LOCATION, 'normalize', '-r', ref_fasta, zipped_file, '-o', output_vcf, '-q']
    print >> sys.stdout, 'VT Command: %s'%(' '.join(cmd))
    #logger.debug('VT Command: %s'%(' '.join(cmd)))
    #cmd = [BCFTOOLS_LOCATION, 'norm', '-m', '-', '-O', 'b', '-o', output_vcf, zipped_file] #Python vcf parser doesn't like bcftools norm output
    #logger.info('bcftools norm Command: %s'%(' '.join(cmd)))
    try:
        rv = subprocess.check_call(cmd)
        return output_vcf
    except subprocess.CalledProcessError, e:
        print >> sys.stderr, "Non-zero exit code from normalization! Bailing out."
        #logger.critical("Non-zero exit code from normalization! Bailing out.")
        sys.exit(1)

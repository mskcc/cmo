from collections import defaultdict
import json, subprocess, sys
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
    chr1_tag = subprocess.Popen(" ".join(get_chr1_cmd), shell=True, stdout=subprocess.PIPE).communicate()[0]
    print chr1_tag
    (chr_name, length) = chr1_tag.strip().split(" ")
    chr_name = chr_name[3:]
    length = length[3:]
    for candidate in chr1_fingerprints:
        if chr1_fingerprints[candidate]['name']==chr_name and chr1_fingerprints[candidate]['length']==int(length):
            print >>sys.stderr, "Inferred genome to be %s" % candidate
            return genomes[candidate]['fasta']
    print >>sys.stderr, "Chromoosome 1 name %s, length %s, doesn't match any standard refs?" % (chr_name, length)
    return None


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



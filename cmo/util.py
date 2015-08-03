from collections import defaultdict
import json
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


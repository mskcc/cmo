import os, sys
from . import util




class Bwa:
    def __init__(self,version="default", samtools_version="default"):
        try:
            self.bwa_cmd=util.programs["bwa"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of bwa in configuration file: %s" % version
            sys.exit(1)
        try:   
            self.samtools_cmd=util.programs["samtools"][samtools_version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of samtools in configuration file: %s" % version
            sys.exit(1)
    def index(self, fasta, args_dict=None):
        if not os.path.isfile(fasta):
            print >>sys.stderr, "You must supply a fasta file to bwa index: %s is not a file" % fasta
            sys.exit(1)
        cmd = [self.bwa_cmd,"index"]
        if args_dict != None:
            for arg, value in args_dict.items():
                cmd.append( "-" + arg + " " + value)
        cmd.append(fasta)
        return " ".join(cmd)
    def aln(self, fasta, fastq, output, args_dict=None):
        cmd = [self.bwa_cmd, "aln"]
        if args_dict != None:
            for arg, value in args_dict.items():
                cmd.append( "-" + arg + " " + value)
        cmd.append(fasta)
        cmd.append(fastq)
        cmd = cmd + [">", output]
        return " ".join(cmd)
    def mem(self, fasta, fastq1, fastq2, output, args_dict=None, no_bam=False):
        cmd = [self.bwa_cmd, "mem"]
        if args_dict != None:
            for arg, value in args_dict.items():
                if value != None:
                    cmd.append( "-" + arg + " " + value)
        cmd.append(fasta)
        cmd.append(fastq1)
        if(fastq2):
            cmd.append(fastq2)
        if no_bam: 
            cmd = cmd + [">", output]
        else:
            cmd = cmd + ["|", self.samtools_cmd, "view -bShq 1 -F 4 - ", ">", output]
        return " ".join(cmd)
    def sampe(self, fasta, sai1, sai2, fq1, fq2, output_bam, args_dict=None, no_bam=False):
        cmd = [self.bwa_cmd, "sampe"]
        if args_dict != None:
            for arg, value in args_dict.items():
                if value != None:
                    cmd.append( "-" + arg + " " + value)
        cmd = cmd + [ sai1, sai2, fq1, fq2, "|", self.samtools_cmd, "view -bShq 1 -F 4  -", ">", output_bam]
        return " ".join(cmd)

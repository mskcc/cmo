import os, sys
from . import util




class Bwa:
    def __init__(self,version="default"):
        try:
            self.bwa_cmd=util.programs["bwa"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of bwa in configuration file: %s" % version
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
        return cmd.join(" ")
    def aln(self, prefix, fastq, args_dict=None):
        cmd = [self.bwa_cmd, "aln"]
        if args_dict != None:
            for arg, value in args_dict.items():
                cmd.append( "-" + arg + " " + value)
        cmd.append(prefix)
        cmd.append(fastq)
        return cmd.join(" ")
    def sampe(self, prefix, sai1, sai2, fq1, fq2, args_dict):
        cmd = [self.bwa_cmd, "sampe"]
        if args_dict != None:
            for arg, value in args_dict.items():
                cmd.append( "-" + arg + " " + value)
        cmd = cmd + [ sai1, sai2, fq1, fq2]
        return cmd.join(" ")

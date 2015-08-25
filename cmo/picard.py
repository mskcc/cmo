import os, sys
from . import util




class Picard:
    def __init__(self,version="default", java_version="default", java_args="-Xmx2g"):
        try:
            self.picard_jar=util.programs["picard"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of piard in configuration file: %s" % version
            sys.exit(1)
        try: 
            self.java_cmd=util.programs["java"][version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of java to run picard with: %s" % version
            sys.exit(1)
        self.java_args = java_args
        self.default_args = {
                "TMP_DIR" : "None",
                "VERBOSITY" : "INFO",
                "QUIET": "false",
                "VALIDATION_STRINGENCY":"STRICT",
                "COMPRESSION_LEVEL": "5",
                "MAX_RECORDS_IN_RAM": "500000",
                "CREATE_INDEX": "false",
                "CREATE_MD5_FILE": "false",
                "REFERENCE": "null",
           #     "GA4GH_CLIENT_SECRETS":"null",
                }
    def picard_cmd(self, command, default_args_override={}, command_specific_args={}):
        cmd = [self.java_cmd, self.java_args, "-jar", self.picard_jar, command]
        for arg, value in self.default_args.items():
            if arg not in default_args_override:
                cmd = cmd + [arg + "=" + value]
            else:
                cmd = cmd + [arg + "=" + default_args_override[arg]]
        for arg, value in command_specific_args.items():
            if value != None:
                cmd = cmd + [arg + "=" + value]
        return " ".join(cmd)
    def picard_cmd_help(self, command):
        cmd = [self.java_cmd, self.java_args, "-jar", self.picard_jar, command, " -h"]
        return " ".join(cmd)






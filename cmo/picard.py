import os, sys, subprocess, re
from . import util




class Picard:
    def __init__(self,version="default", java_version="default", java_args="-Xmx2g"):
        try:
            self.picard_jar=util.programs["picard"][version]
            self.version=version
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of piard in configuration file: %s" % version
            sys.exit(1)
        try: 
            self.java_cmd=util.programs["java"][java_version]
        except KeyError, e:
            print >>sys.stderr, "Cannot find specified version of java to run picard with: %s" % java_version
            sys.exit(1)
        self.java_args = java_args
        self.default_args = {
                "TMP_DIR" : "/scratch/",
                "VERBOSITY" : "INFO",
                "QUIET": "false",
                "VALIDATION_STRINGENCY":"SILENT",
                "COMPRESSION_LEVEL": "5",
                "MAX_RECORDS_IN_RAM": "5000000",
                "CREATE_INDEX": "true",
                "CREATE_MD5_FILE": "false",
           #     "GA4GH_CLIENT_SECRETS":"null",
                }
        
    def picard_cmd(self, command, default_args_override={}, command_specific_args={}):
        #TODO -make this resource hack better
        self.java_args = "-Xms256m -Xmx30g -XX:-UseGCOverheadLimit -Djava.io.tmpdir=/scratch/"
        if(self.version == "1.96"):
            cmd = [self.java_cmd, self.java_args, "-jar", os.path.join(self.picard_jar, command+".jar")]
        else:
            cmd = [self.java_cmd, self.java_args, "-jar", self.picard_jar, command]
        #overwrite default args with whatever was passed in
        for arg, value in default_args_override.items():
            if arg in self.default_args:
                self.default_args[arg] = value        
        #add combination of pass-ins and defaults to command 
        for arg, value in self.default_args.items():
            if arg in default_args_override:
                value = default_args_override[arg]
            if arg not in command_specific_args:
                if value==True:
                    cmd = cmd + [arg + "="+ str(value)]
                elif value != None and value !=False:
                    cmd = cmd + [arg + "=" + value]
        for arg, value in command_specific_args.items():
            if(isinstance(value, list)):
                for arg_value in value:
                    cmd = cmd + [arg + "=" + arg_value]
            elif value==True:
                cmd = cmd + [arg + "=" + str(value)]
            elif value != None and value!=False:
                cmd = cmd + [arg + "=" + value]
        print >>sys.stderr, " ".join(cmd)
        return " ".join(cmd)
    def picard_cmd_help(self, command):
        if(self.version == "1.96"):
            cmd = [self.java_cmd, self.java_args, "-jar", os.path.join(self.picard_jar, command+ ".jar"), "-h"]
        else:
            cmd = [self.java_cmd, self.java_args, "-jar", self.picard_jar, command, " -h"]
        return " ".join(cmd)

    def find_sub_command_options(self, sub_command):
        cmd = self.picard_cmd_help(sub_command) 
        picard_help = subprocess.Popen(cmd,stderr=subprocess.PIPE,shell=True).communicate()[1]
        #look for "is not a valid command, and return the picard help instead of a parsed dict of args
        if re.search("is not a valid command", picard_help):
            return (None, picard_help)
        #look for 1 or 2 occurrences of WORD_THINGY=THINGY and the following help and return them as a dictified
        #list of tuples
        valid_args = []
        new_short_option = None;
        new_description = '';

        for line in picard_help.split("\n"):
            m= re.search("(?:^([\S_]+)=\S+\n?)\s+([\S\s]+)$", line)
            if(m):
                #new option
                if new_short_option:
                    valid_args.append((new_short_option, new_description))
                new_short_option = m.group(1)
                new_description = m.group(2)
            elif new_description !='':
                new_description = new_description + line
        valid_args.append((new_short_option, new_description))
        #valid_args = re.findall(r"(?:^([\S_]+)=\S+\n?){1,2}\s+([\S\s]+?(?=^[\S_]+=\S+))", picard_help, re.M)
        return (dict(valid_args), None)





import fireworks
from fireworks.queue import queue_launcher
from fireworks.core import rocket_launcher
from fireworks.utilities.fw_serializers import load_object_from_file
from pymongo import MongoClient
import getpass, os, sys, time, uuid, daemon, atexit
import logging, yaml, copy
FW_LPAD_CONFIG_LOC = "/opt/common/CentOS_6-dev/cmo/fireworks_config_files"
FW_WFLOW_LAUNCH_LOC = "/ifs/res/pwg/logs/fireworks_workflows"
class Job(fireworks.Firework):
    #FIXME inherit from Firework?
    #TODO type checking
    #if not isinstance(command, string):
    def __new__(cls, command, **kwargs):
        bsub_options_dict = {}
        spec = None
        name = None
        for key in['queue', 'resources', 'walltime', 'est_wait_time', 'processors']:
            if key in kwargs:
                bsub_options_dict[key] = kwargs[key]
        spec = {}
        if len(bsub_options_dict.keys()) > 0:
            spec['_queueadapter'] = bsub_options_dict
     #   spec['_dupefinder']={"_fw_name" : "DupeFinderScript"}
        if 'name' in kwargs:
            name = kwargs['name']
        return fireworks.Firework(fireworks.ScriptTask.from_str(command), name=name, spec=spec)
    def __init__(self, command, resources=None, name=None, queue=None, walltime=None):
        self.resources = resources
        self.queue = queue
        self.walltime = walltime
        if name:
            self.name = name
       
class Workflow():
    def __init__(self, jobs_list, job_dependencies, name=None):
        self.jobs_list = jobs_list
        self.job_dependencies = job_dependencies
        self.name = name
        db = DatabaseManager()
        self.db = db
        # Make sure the user has rlaunch in their PATH
        if self.which('rlaunch') is None:
            print >>sys.stderr, "Can't find rlaunch in $PATH. Please see readme to set $PATH correctly"
            sys.exit(1)
        self.launchpad = fireworks.LaunchPad.from_file(db.find_lpad_config())
    def add_job(job):
        if job not in self.jobs_list:
            jobs_list.append(job)
    def add_dep(job1, jobs2):
        if not isinstance(jobs2,list):
            jobs2 = [jobs2]
        if job1 in self.job_dependencies:
            self.job_dependencies[job1] = self.job_dependencies[job1] + jobs2
        else:
            self.job_dependencies[job1] = jobs2
            if job1 not in self.jobs_list:
                jobs_list.append(job)
                

    def run(self, processing_mode, daemon_log=None):
        if not daemon_log:
            daemon_log = os.path.join(FW_WFLOW_LAUNCH_LOC, getpass.getuser(), "daemon.log")
        self.set_launch_dir()
        if processing_mode == 'serial':
            unique_serial_key = str(uuid.uuid4())
            serial_worker = fireworks.FWorker(name=unique_serial_key)
            for job in self.jobs_list:
                job.spec['_fworker'] = unique_serial_key
            self.workflow = fireworks.Workflow(self.jobs_list, self.job_dependencies, name=self.name)
            self.launchpad.add_wf(self.workflow)
            rocket_launcher.rapidfire(self.launchpad, fworker=serial_worker)
        elif processing_mode == 'LSF':
            for job in self.jobs_list:
                job.spec['_fworker'] = 'LSF'
            self.workflow = fireworks.Workflow(self.jobs_list, self.job_dependencies, name=self.name)
            self.launchpad.add_wf(self.workflow)
            self.watcher_daemon(daemon_log)

    # Look through user's path for a program
    def which(self, program):
        import os
        def is_exe(fpath):
            return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

        fpath, fname = os.path.split(program)
        if fpath:
            if is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if is_exe(exe_file):
                    return exe_file

        return None

    def set_launch_dir(self):
        if self.name:
            keepcharacters = ('.','_')
            sanitized_workflow_name = "".join(c for c in self.name.replace(" ", "_") if c.isalnum() or c in keepcharacters).rstrip() + "-" + str(uuid.uuid4())
        else:
            sanitized_workflow_name = time.strftime("%m-%d-%Y-%I-%M-%S") +  str(uid.uuid4())
        workflow_dir = os.path.join(FW_WFLOW_LAUNCH_LOC, getpass.getuser(), sanitized_workflow_name, "")
        os.makedirs(workflow_dir)
        for job in self.jobs_list:
            if job.name:
                keepcharacters = ('.','_')
                sanitized_job_name = "".join(c for c in job.name.replace(" ", "_") if c.isalnum() or c in keepcharacters).rstrip() + "-" + str(uuid.uuid4())
            else:
                sanitized_job_name = time.strftime("%m-%d-%Y-%I-%M-%S") +  str(uid.uuid4())
            job_launch_dir = os.path.join(workflow_dir, sanitized_job_name, "")
            os.makedirs(job_launch_dir)
            job.spec['_launch_dir'] = job_launch_dir
    def cleanup_daemon(self):
            print >>sys.stderr, "Cleaning up Daemon record..."
            daemons = self.db.client.daemons
            daemons.daemons.remove({"user":getpass.getuser()})
    def watcher_daemon(self, log_file):
        log = None
        
        if(log_file):
            try:
                log = open(log_file, "w")
            except:
                log = log_file #hope its a filehandle instead!
        print >>sys.stderr ,"Log file opened!"
        #about to fork a process, throw away all handlers.
        #fireworks will create a new queue log handler to write to test with
        #lil hacky but who cares right now
        logging.handlers = []
        #FIXME this seems not to have fixed it all the time?
        old_sys_stdout = sys.stdout
        self.db.client.close()
        self.launchpad.connection.close()
        print >>sys.stderr, "Connections closed, preparing to fork..."
        with daemon.DaemonContext( stdout=log, stderr=log):
            logging.handlers = []
            dbm = DatabaseManager()
            self.db = dbm
            #reconnect to mongo after fork
            print dbm.find_lpad_config()
            self.launchpad = fireworks.LaunchPad.from_file(dbm.find_lpad_config())
            self.qadapter = dbm.find_qadapter()
            #add our pid as a running process so new daemons don't get started
            dbm.client.admin.authenticate("fireworks", "speakfriendandenter")
            db = dbm.client.daemons
            #FIXME POSSIBLE CRITICAL RAISE FOR EXTREMELY RAPID WORKFLOW STARTS
            #ADD MUTEX?
            running_daemons = db.daemons.find({"user":getpass.getuser()}).count()
            if running_daemons > 0:
            #todo, check pid is alive
                print >>old_sys_stdout, "Not Forking Daemon- daemon process found"
            #don't start daemon
                sys.exit(0)
            atexit.register(self.cleanup_daemon)
            db.daemons.insert_one({"user":getpass.getuser(), "pid":os.getpid()})

            while(True):

                common_adapter  = load_object_from_file(self.qadapter)
                launcher_log_dir = os.path.join(FW_WFLOW_LAUNCH_LOC, getpass.getuser(), "")
                queue_launcher.rapidfire(self.launchpad, fireworks.FWorker(name="LSF"), common_adapter, reserve=True, nlaunches=0, launch_dir=launcher_log_dir, sleep_time=10, njobs_queue=500)
                failed_fws = []
                time.sleep(50)
#                offline_runs =  self.launchpad.offline_runs.find({"completed": False, "deprecated": False}, {"launch_id": 1}).count()
#                self.launchpad.m_logger.info("%s offline runs found" % offline_runs)
                ready_lsf_jobs = self.launchpad.fireworks.find({"state":"READY", "spec._fworker" : "LSF"}).count()
                reserved_lsf_jobs = self.launchpad.fireworks.find({"state":"RESERVED", "spec._fworker" : "LSF"}).count()
                running_lsf_jobs = self.launchpad.fireworks.find({"state":"RUNNING", "spec._fworker":"LSF"}).count()

                self.launchpad.m_logger.info("%s ready, %s running, %s reserved lsf jobs found" % (ready_lsf_jobs, running_lsf_jobs, reserved_lsf_jobs))
                if(ready_lsf_jobs == 0 and reserved_lsf_jobs == 0 and running_lsf_jobs == 0):
                    break
                for l in self.launchpad.offline_runs.find({"completed": False, "deprecated": False}, {"launch_id": 1}):
                    fw = self.launchpad.recover_offline(l['launch_id'], True)
                    if fw:
                        failed_fws.append(fw)
                self.launchpad.m_logger.info("FINISHED recovering offline runs.")
                if failed_fws:
                    self.launchpad.m_logger.info("FAILED to recover offline fw_ids: {}".format(failed_fws))
            db.daemons.remove({"user":getpass.getuser()})
    def dump_yaml(self, yaml_filename):
        ofh = open(yaml_filename, "w")
        job_list = {'fws': list()}
        old_jobs = dict()
        for i, job in enumerate(self.jobs_list):
            new_job = dict()
            new_job['spec'] = copy.deepcopy(job.spec)
            new_job['spec']['_tasks'] = dict({'_fw_name': 'ScriptTask'})
            new_job['spec']['_tasks']['script'] = job.spec['_tasks'][0]['script'][0]
            new_job['fw_id'] = i
            new_job['name'] = job.name
            job_list['fws'].append(new_job)
            old_jobs[job] = i
        ofh.write(yaml.safe_dump(job_list, default_flow_style=False))
        links = { 'links': dict()}
        for (key, value) in self.job_dependencies.items():
            if isinstance(value, list):
                links['links'][old_jobs[key]] = list()
                for item in value:
                    print key, item
                    links['links'][old_jobs[key]].append(old_jobs[item])
            else:
                links['links'][old_jobs[key]] = list()
                links['links'][old_jobs[key]].append(old_jobs[value])
        ofh.write(yaml.safe_dump(links, default_flow_style=False))
        ofh.write(yaml.safe_dump({"metadata":dict()}))
        ofh.close()

class DatabaseManager():
    def __init__(self, host="pitchfork.cbio.private", port="27017", user=getpass.getuser()):
        self.host = host
        self.port = port
        self.client = MongoClient(host+":"+port)
        self.user = user
    def lpad_cfg_filename(self):
        return self.user+".yaml"
    def qadapt_cfg_filename(self):
        return "qadapter_LSF." + self.user + ".yaml"
    def find_lpad_config(self):
        lpad_file = os.path.join(FW_LPAD_CONFIG_LOC, self.lpad_cfg_filename())
        if not os.path.exists(lpad_file):
            self.create_lpad_config()
        print >>sys.stderr, "Using %s launchpad config" % lpad_file
        return lpad_file
    def find_qadapter(self):
        qadapt_file = os.path.join(FW_LPAD_CONFIG_LOC, self.qadapt_cfg_filename())
        if not os.path.exists(qadapt_file):
            self.create_qadapt_file()
        return qadapt_file
    def create_qadapt_file(self):
        qadapt_file = os.path.join(FW_LPAD_CONFIG_LOC, self.qadapt_cfg_filename())
        fh = open(qadapt_file, "w")
        yaml_dict = {"_fw_name" :  "CommonAdapter",
                "_fw_q_type" : "LoadSharingFacility",
                "_fw_template_file" : "/opt/common/CentOS_6-dev/cmo/LoadSharingFacility_template.txt",
                "rocket_launch" : "rlaunch -l " + self.find_lpad_config() +  " singleshot",
                "queue" : "sol",
                "account" : "null",
                "job_name" : "null",
                "logdir" : "/ifs/res/pwg/logs/lsf_logs",
                "pre_rocket" : "null",
                "post_rocket" : "null"
                }
        for key,value in yaml_dict.items():
            print >>sys.stderr, "Qadapt: %s: %s" % (key, value)
            fh.write(key + ": " + value + "\n")
        fh.close()

    def create_lpad_config(self):
        # Make sure the user didn't bsub/qsub the cmoflow command that led us here
        if 'LSB_JOBID' in os.environ or 'PBS_JOBID' in os.environ or 'JOB_ID' in os.environ:
            print >>sys.stderr, "Please run cmoflow commands in an interactive shell. Don't bsub/qsub them!"
            sys.exit(1)
        print >>sys.stderr, "Writing new config file for your user"
        print >>sys.stderr, "Initializing a new DB will destroy any data in Mongo if you have anything there"
        date = raw_input("Enter today's date in YYYY-MM-DD to confirm:")
        lpad_file = os.path.join(FW_LPAD_CONFIG_LOC, self.lpad_cfg_filename())
        fh = open(lpad_file,"w")
        yaml_dict =  { "username" : self.user,
                "name" : self.user,
                "strm_lvl": "INFO",
                "host" : self.host,
                "logdir" : "null",
                "password" : "speakfriendandenter",
                "port" : self.port }
        for key, value in yaml_dict.items():
            print >>sys.stderr, "Config: %s:%s" % (key, value)
            fh.write(key + ": " + value + "\n")
        fh.close()
        self.client.admin.authenticate("fireworks", "speakfriendandenter")
        self.client[self.user].add_user(self.user,"speakfriendandenter", roles=[{'role':'readWrite', 'db':'testdb'}])
        lpad = fireworks.LaunchPad.from_file(lpad_file)
        lpad.reset(date)
        return lpad_file
    def get_daemon_pid(self, user=getpass.getuser()):
        daemon_record = self.client.daemons.daemons.find_one({"user":user})
        if daemon_record:
            return daemon_record['pid']
        else:
            return None
    def remove_daemon_pid(self, user=getpass.getuser()):
        return self.client.daemons.daemons.remove({"user":user})

import fireworks
from fireworks.queue import queue_launcher
from fireworks.core import rocket_launcher
from fireworks.utilities.fw_serializers import load_object_from_file
from pymongo import MongoClient
import getpass, os, sys, time, uuid, daemon
import logging
FW_LPAD_CONFIG_LOC = "/opt/common/CentOS_6-dev/cmo/fireworks_config_files"
FW_WFLOW_LAUNCH_LOC = "/opt/common/CentOS_6-dev/fireworks_workflows"
class Job(fireworks.Firework):
    #FIXME inherit from Firework?
    #TODO type checking
    #if not isinstance(command, string):
    def __new__(cls, command, **kwargs):
        bsub_options_dict={}
        spec = None
        name = None
        for key in['queue', 'resources', 'walltime']:
            if key in kwargs:
                bsub_options_dict[key]=kwargs[key]
        if len(bsub_options_dict.keys()) > 0:
            spec = {}
            spec['_queueadapter']=bsub_options_dict
        if 'name' in kwargs:
            name=kwargs['name']
        return fireworks.Firework(fireworks.ScriptTask.from_str(command), name=name, spec=spec)
    def __init__(self, command, rusage=None, name=None, queue=None, walltime=None):
        self.rusage = rusage
        self.queue= queue
        self.walltime=walltime
        if name:
            self.name=name
       
class Workflow():
    def __init__(self, jobs_list, job_dependencies, name=None):
        self.jobs_list = jobs_list
        self.job_dependencies = job_dependencies
        self.name=name
        db = DatabaseManager()
        self.launchpad = fireworks.LaunchPad.from_file(db.find_lpad_config())
    def run(self, processing_mode, daemon_log=None):
        if processing_mode=='serial':
            unique_serial_key = str(uuid.uuid4())
            serial_worker = fireworks.FWorker(name=unique_serial_key)
            for job in self.jobs_list:
                job.spec['_fworker']=unique_serial_key
            self.workflow = fireworks.Workflow(self.jobs_list, self.job_dependencies, name=self.name)
            self.launchpad.add_wf(self.workflow)
            rocket_launcher.rapidfire(self.launchpad, fworker=serial_worker)
        elif processing_mode=='LSF':
            self.set_launch_dir()
            for job in self.jobs_list:
                job.spec['_fworker']='LSF'
            self.workflow = fireworks.Workflow(self.jobs_list, self.job_dependencies, name=self.name)
            self.launchpad.add_wf(self.workflow)
            self.watcher_daemon(daemon_log)
    def set_launch_dir(self):
        if self.name:
            keepcharacters = ('.','_')
            sanitized_workflow_name = "".join(c for c in self.name.replace(" ", "_") if c.isalnum() or c in keepcharacters).rstrip() + "-"+ str(uuid.uuid4())
        else:
            sanitized_workflow_name = time.strftime("%m-%d-%Y-%I-%M-%S") +  str(uid.uuid4())
        workflow_dir = os.path.join(FW_WFLOW_LAUNCH_LOC, getpass.getuser(), sanitized_workflow_name, "")
        os.makedirs(workflow_dir)
        for job in self.jobs_list:
            if job.name:
                keepcharacters = ('.','_')
                sanitized_job_name = "".join(c for c in job.name.replace(" ", "_") if c.isalnum() or c in keepcharacters).rstrip() + "-"+ str(uuid.uuid4())
            else:
                sanitized_job_name = time.strftime("%m-%d-%Y-%I-%M-%S") +  str(uid.uuid4())
            job_launch_dir = os.path.join(workflow_dir, sanitized_job_name, "")
            os.makedirs(job_launch_dir)
            job.spec['_launch_dir']=job_launch_dir
    def watcher_daemon(self, log_file):
        log=None
        if(log_file):
            log = open(log_file, "w")
        #about to fork a process, throw away all handlers.
        #fireworks will create a new queue log handler to write to test with
        #lil hacky but who cares right now
        logging.handlers=[]
        #FIXME this seems not to have fixed it all the time?
        old_sys_stdout = sys.stdout
        with daemon.DaemonContext( stdout=log, stderr=log):
            dbm = DatabaseManager()
            #reconnect to mongo after fork
            self.launchpad=fireworks.LaunchPad.from_file(dbm.find_lpad_config())
            #add our pid as a running process so new daemons don't get started
            dbm.client.admin.authenticate("fireworks", "speakfriendandenter")
            db = dbm.client.daemons
            #FIXME POSSIBLE CRITICAL RAISE FOR EXTREMELY RAPID WORKFLOW STARTS
            #ADD MUTEX?
            running_daemons = db.daemons.find({"user":getpass.getuser()}).count()
            if running_daemons >0:
            #todo, check pid is alive
                print >>old_sys_stdout, "Not Forking Daemon- daemon process found"
            #don't start daemon
                sys.exit(0)

            db.daemons.insert_one({"user":getpass.getuser(), "pid":os.getpid()})
            while(True):
                common_adapter  = load_object_from_file("/opt/common/CentOS_6-dev/cmo/qadapter_LSF.yaml")
                launcher_log_dir = os.path.join(FW_WFLOW_LAUNCH_LOC, getpass.getuser(), "")
                queue_launcher.rapidfire(self.launchpad, fireworks.FWorker(name="LSF"), common_adapter, reserve=True, nlaunches=0, launch_dir=launcher_log_dir, sleep_time=10)
                failed_fws = []
                time.sleep(10)
                offline_runs =  self.launchpad.offline_runs.find({"completed": False, "deprecated": False}, {"launch_id": 1}).count()
                self.launchpad.m_logger.info("%s offline runs found" % offline_runs)
                if(offline_runs == 0):
                    break
                for l in self.launchpad.offline_runs.find({"completed": False, "deprecated": False}, {"launch_id": 1}):
                    fw = self.launchpad.recover_offline(l['launch_id'], True)
                    if fw:
                        failed_fws.append(fw)
                self.launchpad.m_logger.info("FINISHED recovering offline runs.")
                if failed_fws:
                    self.launchpad.m_logger.info("FAILED to recover offline fw_ids: {}".format(failed_fws))
            db.daemons.remove({"user":getpass.getuser()})



class DatabaseManager():
    def __init__(self, host="plvcbiocmo2.mskcc.org", port="27017", user=getpass.getuser()):
        self.host=host
        self.port=port
        self.client=MongoClient(host+":"+port)
        self.user = user
    def lpad_cfg_filename(self):
        return self.user+".yaml"
    def find_lpad_config(self):
        lpad_file = os.path.join(FW_LPAD_CONFIG_LOC, self.lpad_cfg_filename())
        if not os.path.exists(lpad_file):
            self.create_lpad_config()
        return lpad_file
    def create_lpad_config(self):
        if os.path.exists(find_lpad_config):
            print >>sys.stderr, "Config already exists: %s" % self.find_lpad_config
        else:
            fh.open(self.find_lpad_config(),"w")
            yaml_dict =  { "username" : self.user,
                    "name" : self.user,
                    "strm_lvl": "INFO",
                    "host" : self.host,
                    "logdir" : "null",
                    "password" : "speakfriendandenter",
                    "port" : self.port }
            for key, value in yaml_dict:
                fh.write(key + ": " + value + "\n")
            fh.close()
            client.admin.authenticate("fireworks", "speakfriendandenter")
            client.charris.add_user("charris","speakfriendandenter", roles=[{'role':'readWrite', 'db':'testdb'}])
            lpad = fireworks.LaunchPad.from_file(self.find_lpad_config())
            lpad.reset()
        return self.find_lpad_config()
        





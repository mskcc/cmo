import fireworks
from fireworks.queue import queue_launcher
from fireworks.core import rocket_launcher
from fireworks.utilities.fw_serializers import load_object_from_file

class Job(fireworks.Firework):
    #FIXME inherit from Firework?
    #TODO type checking
    #if not isinstance(command, string):
    def __new__(cls, command, **kwargs):
        return fireworks.Firework(fireworks.ScriptTask.from_str(command))
    def __init__(self, command, rusage=None, name=None, queue=None, walltime=None):
        self.rusage = rusage
        self.queue= queue
        self.walltime=walltime
        if name:
            self.name=name
        bsub_options_dict = {}
        if queue:
            bsub_options_dict['queue']=queue
        if walltime:
            bsub_options_dict['walltime']=walltime
        if rusage:
            bsub_options_dict['resources']=rusage
        if len(bsub_options_dict.keys())>0:
            self.spec['_queueadapter']=bsub_options_dict

class Workflow():
    def __init__(self, jobs_list, job_dependencies):
        self.jobs_list = jobs_list
        self.job_dependencies = job_dependencies
        self.launchpad=fireworks.LaunchPad.auto_load() # need an FW config in ENV OR similar for this to work
        self.workflow = fireworks.Workflow(jobs_list, job_dependencies)
        self.launchpad.add_wf(self.workflow)
    def run(self, processing_mode):
        if processing_mode=='serial':
            #load user launchpad
            #create user collection if necessary
            #init if necessary
            rocket_launcher.rapidfire(self.launchpad, fireworks.FWorker())
        elif processing_mode=='LSF':

            common_adapter  = load_object_from_file("/opt/common/CentOS_6-dev/cmo/qadapter_LSF.yaml")
            queue_launcher.rapidfire(self.launchpad, fireworks.FWorker(), common_adapter, reserve=True, nlaunches=len(self.jobs_list))






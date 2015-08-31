=========
Fireworks
=========
Writing your first workflow
###########################
1. ssh to s01 (ask for help if you don't know what this means)
2. download and install the CMO package at https://github.com/mskcc/cmo (install for your user with setup.py install --user, as the directions say
3. https://github.com/mskcc/cmo/blob/master/wrapper_template/wrapper_example look over this example code

Example Script
##############

This is the source code of the above link::

    import cmo
    from cmo import workflow
    #create jobs- any command line you can imagine should be OK
    task1 = workflow.Job('echo "Ingrid is the CEO"', name="Task 1", queue="test")
    task2 = workflow.Job('echo "Jill is a manager."', name="Task 2", queue="test")
    task3 = workflow.Job('echo "Jack is a manager."', name="Task 3", queue="test")
    task4 = workflow.Job('echo "Kip is an intern."', name="Task 4", queue="test")

    # assemble Workflow from FireWorks and their connections by id
    jobs_list = [task1,task2,task3,task4]
    #task 1 is root
    #task 2 and task 3 depend on task 1 to be done
    #task 4 depends on task 2 and task 3 to be done
    jobs_dict = {task1: [task2,task3], task2: [task4], task3:[task4]}
    #create the workflow
    new_workflow = workflow.Workflow(jobs_list, jobs_dict, name="Test Workflow")
    #run on lsf and log the run daemon's activity to the file "test"
    new_workflow.run('LSF', daemon_log="test")


Notes
#####
The daemon is a process that runs as you and stays behind on s01 after you launch the script to monitor your job.

If you launch more workflows during this time, the daemon will start monitoring those too- you shouldn't be able to start more than one daemon, no matter how hard you try.

Once the daemon is satisfied all jobs have completed, it will exit on its own









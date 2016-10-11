=========================
Facets via Fireworks/LSF
=========================
Instructions
###########################

.. code-block:: none

    usage: cmoflow_facets [-h] --normal-bam NORMAL_BAM --tumor-bam TUMOR_BAM
    [--tag TAG] [--vcf VCF] [--output-dir OUTPUT_DIR]
    [--normal-name NORMAL_NAME] [--tumor-name TUMOR_NAME]
    [--workflow-mode {serial,LSF}] [--force]
    
    Run Facets on luna!
    
    optional arguments:
    -h, --help            show this help message and exit
    --normal-bam NORMAL_BAM
    The normal bam file
    --tumor-bam TUMOR_BAM
    The Tumor bam file
    --tag TAG             The optional tag with which to identify this pairing,
    default TUMOR_SAMPLE__NORMAL_SAMPLE
    --vcf VCF             override default FACETS snp positions
    --output-dir OUTPUT_DIR
    output dir, will default to $CWD/TAG_NAME/
    --normal-name NORMAL_NAME
    Override this if you don't want to use the SM: tag on
    the @RG tags within the bam you supply-- required if
    your bam doesn't have well formatted @RG SM: tags
    --tumor-name TUMOR_NAME
    Override this if you don't want to use the SM: tag on
    the @RG tags in the tumor bam you supply-- required if
    your bam doesnt have well formatted @RG SM: tags
    --workflow-mode {serial,LSF}
    select 'serial' to run all jobs on the launching box.
    select 'LSF' to parallelize jobs as much as possible
    on luna
    --force               forcibly overwrite any directories you find there
    
    Include any FACETS args directly on this command line and they will be passed
    
    

1. ssh to s01 (ask for help if you don't know what this means)
2. you should have cmoflow_facets available at the command line -- if you don't, add /opt/common/CentOS_6-dev/python/python-2.7.10/bin/
3. Minimally you need to supply \-\-tumor-bam and \-\-normal-bam
4. CMO package will attempt to read all @RG headers and find the SM: tags, and if they all match, it will use that id
5. If the SM: ids betweeen the two bams you supply are IDENTICAL, if they are ABSENT, or if there is MORE THAN ONE PER BAM, you will need to supply --tumor-name and normal-name as well, to manually fill in these values
6. it will autocreate a sub of the format TUMOR_SAMPLE_NAME__NORMAL_SAMPLE_NAME in the dir you launch from if you don't specify OUTPUT DIR
7. it will use the same string as the TAG to identify any merged files, etc.
8. you can specify --workflow_mode=serial to avoid running on LSF 
9. the workflow will take about 1 hr on lsf, 1.5hr serially for 5gb input bams
10. check on your workflow at haystack.mskcc.org:5000/your_cbio_username/
11. facets runs that start in the same output directory will shortcut on both the readcounts and the counts merged gzipped files
12. facets runs will autocreate a subdir of the form "facets\_\[first_param_char\]\[value\]_..." 
13. if it detects a facets run it already has performed it will refuse to do work

.. image:: images/ZiGyS.gif


Notes
###########################

A daemon is a process that runs as you and stays behind on s01 after you launch the script to monitor your job.

If you launch more workflows during this time, the daemon will start monitoring those too- you shouldn't be able to start more than one daemon, no matter how hard you try.

Once the daemon is satisfied all jobs have completed, it will exit on its own.


Code sample for coding other worfklows
#########################################

.. code-block:: python

    #!/opt/common/CentOS_6-dev/python/python-2.7.10/bin/python
    from cmo import workflow
    import argparse, os, sys
    import cmo 
    #WHOA, existentially troubling, man
    PYTHON = cmo.util.programs['python']['default']

    def main(tumorbam, normalbam, tag, facets_args, output_dir,snps=None, tumor_sample=None, normal_sample=None, workflow_mode=None):
        #look at @RG SM: tag for samples
        if not tumor_sample: 
            tumor_sample = cmo.util.infer_sample_from_bam(tumorbam)
        if not normal_sample:
            normal_sample = cmo.util.infer_sample_from_bam(normalbam)
        if normal_sample == tumor_sample:
            print >>sys.stderr, "Sample names in normal and tumor are the same- forcibly override one or both to use this pipeline"
            sys.exit(1)
        if not tag and tumor_sample and normal_sample:  
            tag = tumor_sample + "__" + normal_sample
        elif not tumor_sample:
            print >>sys.stderr, "Can't infer tumor sample name from BAM file-- please supply it to workflow"
            sys.exit(1)
        elif not normal_sample:
            print >>sys.stderr, "Can't infer normal sample name from BAM file-- please supply it to workflow"
            sys.exit(1)
        default_basecount_options = [ "--sort_output", "--compress_output", "--filter_improper_pair 0"]
        if not output_dir:
            #TODO make directory safe for invalid dir chars in sample names
            output_dir = os.path.join(os.getcwd(), tag, '')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        #if the idiot user supplied relative path we must fix
        output_dir = os.path.abspath(output_dir)
        
        #count jobs
        count_jobs = []
        tumor_normal_counts = []
        
        for (bam, base) in [(tumorbam, tumor_sample), (normalbam, normal_sample)]:
            out_file = os.path.abspath(os.path.join(output_dir, base + ".dat"))
            if os.path.exists(out_file + ".gz"):
                #pretend we did this shitty slow step
                tumor_normal_counts.append(out_file)
                continue
            #first we add tumor, then normal - the order mergeTN expects them
            tumor_normal_counts.append(out_file)

            basecount_cmd = ["cmo_getbasecounts", "--bam", bam, "--out", out_file] + default_basecount_options
            if(snps):
                basecount_cmd = basecount_cmd + ["--vcf" ,os.path.abspath(snps)]
            print " ".join(basecount_cmd)
            job = workflow.Job(" ".join(basecount_cmd), est_wait_time="59", resources="rusage[mem=40]", name="getBasecounts " + base)

            count_jobs.append(job)
       
        #merge job
        merged_counts = os.path.join(output_dir, "countsMerged____" + tag + ".dat.gz")
        merge_job= None
        if not os.path.exists(merged_counts):
            merge_cmd = ["cmo_facets mergeTN"] + tumor_normal_counts + [merged_counts]
            print " ".join(merge_cmd)
            merge_job = workflow.Job(" ".join(merge_cmd), est_wait_time="59", resources="rusage[mem=60]", name="mergeTN " + tag)
      
        #facets job
        #args will be [--foo, value] or [-f, value] in this list
        it = iter(facets_args)
        facets_dir = "facets_"
        if len(facets_args) ==0:
            facets_dir += "default"
        else:
            for val in it:
                arg = val.lstrip("-")[0]
                value = next(it)
                facets_dir += "%s-%s" % (arg, value)
        facets_dir = os.path.join(output_dir, cmo.util.filesafe_string(facets_dir))
        if os.path.exists(facets_dir):
            print >>sys.stderr, "This facets setting directory already exists- bailing out - RM it to force rerun"
            sys.exit(1)
        else:
            print >>sys.stderr, "created facets subdir for these settings: %s" % facets_dir
            os.makedirs(facets_dir)
        facets_cmd = ["cmo_facets run"] + [merged_counts, tag, facets_dir] + facets_args
        facets_job = workflow.Job(" ".join(facets_cmd), est_wait_Time="59", name="Run Facets")
        dependencies = {}
      
      #FIXME: can we have a merge exist without the counts file?
        #if so this set of ifs needs to be redone
        jobs = []
        if len(count_jobs) > 0:
            dependencies[count_jobs[0]]=[merge_job]
            dependencies[count_jobs[1]]=[merge_job]
            jobs = jobs + count_jobs
        if(merge_job):
            dependencies[merge_job]=[facets_job]
            jobs.append(merge_job)
        #make workflow
        jobs.append(facets_job)
        facets_workflow = workflow.Workflow(jobs, dependencies, name="Facets job " + tag)
        facets_workflow.run(workflow_mode)



    if __name__=='__main__':
        parser = argparse.ArgumentParser(description="Run Facets on luna!", epilog="Include any FACETS args directly on this command line and they will be passed through")
        parser.add_argument("--normal-bam", required=True, help="The normal bam file")
        parser.add_argument("--tumor-bam", required=True, help="The Tumor bam file")
        parser.add_argument("--tag", help="The optional tag with which to identify this pairing, default TUMOR_SAMPLE__NORMAL_SAMPLE")
        parser.add_argument("--vcf", help="override default FACETS snp positions")
        parser.add_argument("--output-dir", help="output dir, will default to $CWD/TAG_NAME/")
        parser.add_argument("--normal-name", help="Override this if you don't want to use the SM: tag on the @RG tags within the bam you supply-- required if your bam doesn't have well formatted @RG SM: tags")
        parser.add_argument("--tumor-name", help="Override this if you don't want to use the SM: tag on the @RG tags in the tumor bam you supply-- required if your bam doesnt have well formatted @RG SM: tags")
        parser.add_argument("--workflow-mode", choices=["serial","LSF"], default="LSF", help="select 'serial' to run all jobs on the launching box. select 'LSF' to parallelize jobs as much as possible on luna")
        (args, facets_args) = parser.parse_known_args()
        if args.output_dir:
            args.output_dir = os.path.abspath(output_dir)
        args.tumor_bam = os.path.abspath(args.tumor_bam)
        args.normal_bam = os.path.abspath(args.normal_bam)
        main(args.tumor_bam, args.normal_bam, args.tag, facets_args, args.output_dir, snps=args.vcf, tumor_sample = args.tumor_name, normal_sample=args.normal_name, workflow_mode=args.workflow_mode)


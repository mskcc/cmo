================================
Exome Pipeline via Fireworks/LSF
================================
Instructions
###########################

.. code-block:: none

    usage: cmoflow_reference_alignment [-h] [--output-dir OUTPUT_DIR]
    [--config-file CONFIG_FILE]
    [--map-file MAP_FILE]
    [--group-file GROUP_FILE]
    [--pair-file PAIR_FILE]
    [--patient-file PATIENT_FILE]
    [--project PROJECT] --targets
    {IMPACT_341_hg19,AgilentExon_51MB_hg19_v3,AgilentExon_51MB_b37_v3,Agilent_MouseAllExonV1_mm10_v1,Genomic_mm10,AgilentExon_51MB_hg19_mm10_v3,wgs_hg19,abra,IMPACT410_hg19}
    [--workflow-mode {serial,LSF}]
    [--workflow-name WORKFLOW_NAME]
    [--genome {GRCh37,hg19}] [--gatk-indel]
    
    Run Variant pipeline on luna!
    
    optional arguments:
    -h, --help            show this help message and exit
    --output-dir OUTPUT_DIR
    output dir, will default to $CWD/TAG_NAME/
    --config-file CONFIG_FILE
    configuration file
    --map-file MAP_FILE   file listing sample information for processing
    --group-file GROUP_FILE
    file listing grouping of samples for realign/recal
    steps
    --pair-file PAIR_FILE
    file listing tumor/normal pairs for mutect/maf
    conversion
    --patient-file PATIENT_FILE
    if a patient file is given, patient wide fillout will
    be added to maf file
    --project PROJECT     name of project
    --targets {IMPACT_341_hg19,AgilentExon_51MB_hg19_v3,AgilentExon_51MB_b37_v3,Agilent_MouseAllExonV1_mm10_v1,Genomic_mm10,AgilentExon_51MB_hg19_mm10_v3,wgs_hg19,abra,IMPACT410_hg19}
    --workflow-mode {serial,LSF}
    select 'serial' to run all jobs on the launching box.
    select 'LSF' to parallelize jobs as much as possible
    on luna
    --workflow-name WORKFLOW_NAME
    name for this worklfow on GUI
    --genome {GRCh37,hg19}
    --gatk-indel          use GATK isntead of abra (don't do this unless it's WGS)
    
    

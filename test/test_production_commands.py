import subprocess, shutil, os, sys

TEST_TEMP_DIR = None
TEST_DATA_DIR = "/ifs/res/pwg/tests/cmo_testdata/cmo_pipeline_commands/"


test_inputs = {}


def setup_module():
    global TEST_TEMP_DIR
    TEST_TEMP_DIR = tempfile.mkdtemp();

def teardown_module():
    if TEST_TEMP_DIR is not None:
        shutil.rmtree(TEST_TEMP_DIR)
        pass


def test_bwa_mem():
    cmd = ["cmo_bwa_mem",
            "--fastq1", fastq1,
            "--fastq2", fastq2,
            "--genome", genome_string,
            "output", output,
            "--version", version ]

def test_list2bed():
    cmd = ["cmo_list2bed",
            "--input_file", input_file,
            "--no_sort",
            "--output_file", output]

def test_mutect():
    cmd = ['cmo_mutect', 
            '--version', '1.1.4',
            '--cosmic', cosmic,
            '--dbsnp', dbsnp,
            '--downsampling_type', 'NONE',
            '--input_file:normal', normal_bam,
            '--input_file:tumor', tumor_bam,
            '--java_args', '-Xmx48g -Xms256m -XX:-UseGCOverheadLimit',
            '--reference_sequence', genome_string
            '--vcf', out_vcf]

def test_printreads():
    cmd = ['cmo_gatk',
            '-T', 'PrintReads',
            '--version', '3.3-0',
            '--BQSR', output_matrix,
            '--input_file', input_bam,
            '--java_args',  '-Xmx48g -Xms256m -XX:-UseGCOverheadLimit',
            '--num_cpu_threads_per_data_thread', '6',
            '--out', output_filename,
            '--reference_sequence', genome_string]

def test_addorreplacereadgroups():
    cmd = ['cmo_picard',
            '--cmd', 'AddOrReplaceReadGroups',
            '--CN', 'MSKCC',
            '--CREATE_INDEX',
            '--I', tumor_bam,
            '--ID', 'P-0000377',
            '--LB', '5',
            '--O', output_bam,
            '--PL', 'Illumina',
            '--PU', 'bc26',
            '--SM', 'P-0000377-T02-IM3',
            '--SO', 'coordinate',
            '--TMP_DIR', tmpdir]


def test_trimgalore():
    cmd = ['cmo_trimgalore',
            '--adapter',
            'AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATGAGCATCTCGTATGCCGTCTTCTGCTTG',
            '--adapter2',
            'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT',
            '--gzip',
            '--length', '25',
            '--paired',
            '--quality', '1',
            '--suppress_warn',
            '--version', 'default',
            fastq1,
            fastq2,
            ]

def



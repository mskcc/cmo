import subprocess, shutil, os, sys, tempfile, re
from nose.tools import assert_true

TEST_TEMP_DIR = None
TEST_DATA_DIR = "/ifs/work/charris/testdata_for_cmo"


test_inputs = {}
####INPUTS
tumor_bam = os.path.join(TEST_DATA_DIR, "P1_ADDRG_MD.abra.fmi.printreads.bam")
normal_bam = os.path.join(TEST_DATA_DIR, "P2_ADDRG_MD.abra.fmi.printreads.bam")
fastq1=os.path.join(TEST_DATA_DIR, "P1_R1.fastq.gz")
fastq2=os.path.join(TEST_DATA_DIR, "P1_R2.fastq.gz")
matrix=os.path.join(TEST_DATA_DIR, "recal.matrix")
genome_string = "GRCh37"
abratmpdir = "/scratch/abra_cmo_test/"
if not os.path.exists("/scratch"):
    #for jenkins box
    abratmpdir = "/srv/data/scratch"
tmpdir = "/scratch/"
cosmic = "/ifs/work/socci/Pipelines/CBE/variants_pipeline/data/b37/CosmicCodingMuts_v67_b37_20131024__NDS.vcf"
dbsnp = "/ifs/work/charris/temp_depot/dbsnp_138.b37.excluding_sites_after_129.vcf"
hapmap = "/ifs/work/charris/temp_depot/hapmap_3.3.b37.vcf"
snps_1000g = "/ifs/work/charris/temp_depot/1000G_phase1.snps.high_confidence.b37.vcf"
indels_1000g = "/ifs/work/charris/temp_depot/Mills_and_1000G_gold_standard.indels.b37.vcf"
input_list = os.path.join(TEST_DATA_DIR, "intervals.list")
input_bed = os.path.join(TEST_DATA_DIR, "intervals.bed")
##########OUTPUTS
output = None
output2 = None
def setup_module():
    global TEST_TEMP_DIR
    TEST_TEMP_DIR = tempfile.mkdtemp();
    global output
    output= os.path.join(TEST_TEMP_DIR, "output")
    global output2
    output2 = os.path.join(TEST_TEMP_DIR, "output2")
    

def teardown_module():
    if TEST_TEMP_DIR is not None:
#        shutil.rmtree(TEST_TEMP_DIR)
#        shutil.rmtree(abratmpdir)
        pass

def test_abra():
    cmd = ['cmo_abra',
            '--in', ",".join([tumor_bam, normal_bam]),
            "--out", ",".join([output, output2]),
            '--reference_sequence', genome_string,
            '--targets', input_bed,
            '--working', abratmpdir]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True)
    #check prog_output to see if it picked up the arguments we gave...
    assert_true(re.search("input0: /ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
    assert_true(re.search("input0: /ifs/work/charris/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
    assert_true(re.search("regions: /ifs/work/charris/testdata_for_cmo/intervals.bed", prog_output))
    assert_true(re.search("reference: /ifs/depot/assemblies/H.sapiens/b37/b37.fasta", prog_output))
    assert_true(re.search("working dir: /scratch/abra_cmo_test/", prog_output))




def test_bwa_mem():
    cmd = ["cmo_bwa_mem",
            "--fastq1", fastq1,
            "--fastq2", fastq2,
            "--genome", genome_string,
            "--output", output,
            "--version", '0.7.5a'  ]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("0.7.5a", prog_output))

def test_list2bed():
    cmd = ["cmo_list2bed",
            "--input_file", input_list,
            "--no_sort",
            "--output_file", output]
    subprocess.check_call(" ".join(cmd), shell=True)

def test_mutect():
    cmd = ['cmo_mutect', 
            '--version', '1.1.4',
            '-L', '22',
            '--cosmic', cosmic,
            '--dbsnp', dbsnp,
            '--downsampling_type', 'NONE',
            '--input_file:normal', normal_bam,
            '--input_file:tumor', tumor_bam,
            '--java_args', '"-Xmx48g -Xms256m -XX:-UseGCOverheadLimit"',
            '--reference_sequence', genome_string,
            '--enable_extended_output',
            '--vcf', output]
    print " ".join(cmd)
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("INFO .* HelpFormatter - Program Args: -T MuTect --vcf .* --cosmic /ifs/work/socci/Pipelines/CBE/variants_pipeline/data/b37/CosmicCodingMuts_v67_b37_20131024__NDS.vcf --input_file:tumor /ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --downsampling_type NONE --input_file:normal /ifs/work/charris/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam --intervals 22 --dbsnp /ifs/work/charris/temp_depot/dbsnp_138.b37.excluding_sites_after_129.vcf --enable_extended_output --reference_sequence /ifs/depot/assemblies/H.sapiens/b37/b37.fasta", prog_output))

def test_printreads():
    cmd = ['cmo_gatk',
             'PrintReads',
            '--version', '3.3-0',
            '--BQSR', matrix,
            '--input_file', tumor_bam,
            '--java_args',  "'-Xmx48g -Xms256m -XX:-UseGCOverheadLimit'",
            '--num_cpu_threads_per_data_thread', '6',
            '--out', output,
            '--reference_sequence', genome_string]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("INFO  .* HelpFormatter - Program Args: -T PrintReads --input_file /ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --num_cpu_threads_per_data_thread 6 --BQSR /ifs/work/charris/testdata_for_cmo/recal.matrix --reference_sequence /ifs/depot/assemblies/H.sapiens/b37/b37.fasta --out", prog_output))

def test_baserecal():
    cmd= ['cmo_gatk',
            'BaseRecalibrator',
            '--version', '3.3-0',
            '--input_file', tumor_bam,
            '--covariate', 'ContextCovariate',
            '--covariate', 'CycleCovariate',
            '--covariate', 'ReadGroupCovariate',
            '--covariate', 'QualityScoreCovariate',
            '--knownSites', dbsnp,
            '--knownSites',hapmap,
            '--knownSites', snps_1000g,
            '--knownSites', indels_1000g,
            '--java_args', "'-Xmx48g -Xms256m -XX:-UseGCOverheadLimit'",
            '--out', output,
            '--reference_sequence', genome_string]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("INFO .* HelpFormatter - Program Args: -T BaseRecalibrator --input_file /ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --reference_sequence /ifs/depot/assemblies/H.sapiens/b37/b37.fasta --knownSites /ifs/work/charris/temp_depot/dbsnp_138.b37.excluding_sites_after_129.vcf --knownSites /ifs/work/charris/temp_depot/hapmap_3.3.b37.vcf --knownSites /ifs/work/charris/temp_depot/1000G_phase1.snps.high_confidence.b37.vcf --knownSites /ifs/work/charris/temp_depot/Mills_and_1000G_gold_standard.indels.b37.vcf --covariate ContextCovariate --covariate CycleCovariate --covariate ReadGroupCovariate --covariate QualityScoreCovariate --out", prog_output))

def test_addorreplacereadgroups():
    cmd = ['cmo_picard',
            'AddOrReplaceReadGroups',
            '--CN', 'MSKCC',
            '--CREATE_INDEX',
            '--I', tumor_bam,
            '--ID', 'P-0000377',
            '--LB', '5',
            '--O', output,
            '--PL', 'Illumina',
            '--PU', 'bc26',
            '--SM', 'P-0000377-T02-IM3',
            '--SO', 'coordinate',
            '--TMP_DIR', tmpdir]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    print prog_output
    assert_true(re.search("picard.sam.AddOrReplaceReadGroups INPUT=/ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam OUTPUT=.* SORT_ORDER=coordinate RGID=P-0000377 RGLB=5 RGPL=Illumina RGPU=bc26 RGSM=P-0000377-T02-IM3 RGCN=MSKCC TMP_DIR=\[/scratch\] CREATE_INDEX=true    VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_MD5_FILE=false", prog_output))

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
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true("/opt/common/CentOS_6/trim_galore/Trim_Galore_v0.2.5/trim_galore --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATGAGCATCTCGTATGCCGTCTTCTGCTTG --suppress_warn --paired --length 25 --gzip --quality 1 --adapter2 AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT /ifs/work/charris/testdata_for_cmo/P1_R1.fastq.gz /ifs/work/charris/testdata_for_cmo/P1_R2.fastq.gz", prog_output)


def test_vardict():
    cmd = ['cmo_vardict',
            '--version', '1.4.6',
            '-C',
            '-E', '3',
            '-G', genome_string,
            '-N', "Tumor",
            '-N2', "Normal",
            '-Q', '20',
            '-S', '2',
            '-X', '5',
            '-b', tumor_bam,
            '-b2', normal_bam,
            '-c', '1',
            '-f', '0.01',
            '-q', '20',
            '--vcf', output,
            '-x', '2000',
            '-z', '1',
            input_bed ]
    subprocess.check_call(" ".join(cmd), shell=True)


def test_somaticindeldetector():
    cmd = ['cmo_gatk',
            '--version', '2.3-9',
            'SomaticIndelDetector',
            '--filter_expressions', "'\"T_COV<10||N_COV<4||T_INDEL_F<0.0001||T_INDEL_CF<0.7\"'",
            '--intervals', input_bed,
            '--java_args', '"-Xmx48g -Xms256m -XX:-UseGCOverheadLimit"', 
            '--maxNumberOfReads', '100000',
            '--min_mapping_quality_score', '20',
            '--input_file:normal', normal_bam,
            '--input_file:tumor', tumor_bam,
            '--out', output,
            '--reference_sequence', genome_string,
            '--verboseOutput', output2,
            '--read_filter', 'DuplicateRead',
            '--read_filter', 'FailsVendorQualityCheck',
            '--read_filter', 'NotPrimaryAlignment',
            '--read_filter', 'BadMate',
            '--read_filter', 'MappingQualityUnavailable',
            '--read_filter', 'UnmappedRead',
            '--read_filter', 'MappingQuality',
            '--read_filter', 'BadCigar']
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("INFO  .* HelpFormatter - Program Args: -T SomaticIndelDetector --input_file:normal /ifs/work/charris/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam --input_file:tumor /ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --min_mapping_quality_score 20 --intervals /ifs/work/charris/testdata_for_cmo/intervals.bed --filter_expressions T_COV<10||N_COV<4||T_INDEL_F<0.0001||T_INDEL_CF<0.7 --maxNumberOfReads 100000 --verboseOutput .* --read_filter DuplicateRead --read_filter FailsVendorQualityCheck --read_filter NotPrimaryAlignment --read_filter BadMate --read_filter MappingQualityUnavailable --read_filter UnmappedRead --read_filter MappingQuality --read_filter BadCigar --reference_sequence /ifs/depot/assemblies/H.sapiens/b37/b37.fasta --out .*", prog_output))

def test_markduplicates():
    cmd = ['cmo_picard',
            'MarkDuplicates',
            '--CREATE_INDEX',
            '--I', tumor_bam,
            '--M', output2,
            '--O', output,
            '--TMP_DIR', tmpdir
            ]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    assert_true(re.search("picard.sam.markduplicates.MarkDuplicates INPUT=\[/ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam\] OUTPUT=.* METRICS_FILE=.* TMP_DIR=\[/scratch\] CREATE_INDEX=true    MAX_SEQUENCES_FOR_DISK_READ_ENDS_MAP=50000 MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=8000 SORTING_COLLECTION_SIZE_RATIO=0.25 PROGRAM_RECORD_ID=MarkDuplicates PROGRAM_GROUP_NAME=MarkDuplicates REMOVE_DUPLICATES=false ASSUME_SORTED=false DUPLICATE_SCORING_STRATEGY=SUM_OF_BASE_QUALITIES READ_NAME_REGEX=\[a-zA-Z0-9\]\+:\[0-9\]:\(\[0-9\]\+\):\(\[0-9\]\+\):\(\[0-9\]\+\).* OPTICAL_DUPLICATE_PIXEL_DISTANCE=100 VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_MD5_FILE=false", prog_output))

def test_fixmateinformation():
    cmd = ['cmo_picard',
            'FixMateInformation',
            '--I', tumor_bam,
            '--O', output]
    prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
    print prog_output
    assert_true(re.search("picard.sam.FixMateInformation INPUT=\[/ifs/work/charris/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam\] OUTPUT=.* ASSUME_SORTED=false ADD_MATE_CIGAR=true VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false", prog_output))
    





            





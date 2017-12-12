import subprocess, shutil, os, sys, tempfile, re
from nose.tools import assert_true
import unittest


TEST_TEMP_DIR = None
TEST_DATA_DIR = "/ifs/work/pi/testdata/testdata_for_cmo"


test_inputs = {}
####INPUTS
tumor_bam = os.path.join(TEST_DATA_DIR, "P1_ADDRG_MD.abra.fmi.printreads.bam")
normal_bam = os.path.join(TEST_DATA_DIR, "P2_ADDRG_MD.abra.fmi.printreads.bam")
fastq1=os.path.join(TEST_DATA_DIR, "P1_R1.fastq.gz")
fastq2=os.path.join(TEST_DATA_DIR, "P1_R2.fastq.gz")
matrix=os.path.join(TEST_DATA_DIR, "recal.matrix")
genome_string = "GRCh37"
GRCh37_path = "/ifs/work/pi/testdata/assemblies/b37/b37.fasta"
current_dir = os.getcwd()
abratmpdir = "/scratch/"
tmpdir = "/scratch"
working_dir = "/ifs/work/pi/cmo-test/scratch"
cosmic = "/ifs/work/pi/testdata/CosmicCodingMuts_v67_b37_20131024__NDS.vcf"
dbsnp = "/ifs/work/pi/testdata/dbsnp_138.b37.excluding_sites_after_129.vcf"
hapmap = "/ifs/work/pi/testdata/hapmap_3.3.b37.vcf"
snps_1000g = "/ifs/work/pi/testdata/1000G_phase1.snps.high_confidence.b37.vcf"
indels_1000g = "/ifs/work/pi/testdata/Mills_and_1000G_gold_standard.indels.b37.vcf"
target_interval = "/ifs/work/pi/testdata/AgilentExon_51MB_b37_v3_targets.ilist"
bait_interval = "/ifs/work/pi/testdata/AgilentExon_51MB_b37_v3_baits.ilist"
per_target_coverage = "/ifs/work/pi/testdata/Per_Target_Coverage.txt"
input_list = os.path.join(TEST_DATA_DIR, "intervals.list")
input_bed = os.path.join(TEST_DATA_DIR, "intervals.bed")
##########OUTPUTS
output = None
output2 = None

class CMOTest(unittest.TestCase):
    def setUp(self):
        global TEST_TEMP_DIR
        if os.path.exists(working_dir):
            TEST_TEMP_DIR = tempfile.mkdtemp(dir=working_dir)
            global output
            output= os.path.join(TEST_TEMP_DIR, "output")
            global output2
            output2 = os.path.join(TEST_TEMP_DIR, "output2")
            os.chdir(TEST_TEMP_DIR)
	else:
	    raise "I cannot open the working directoy %s" % working_dir

        

    def tearDown(self):
        if TEST_TEMP_DIR is not None:
    #        shutil.rmtree(TEST_TEMP_DIR)
    #        shutil.rmtree(abratmpdir)
            pass
    '''def test_abra_207(self):
        cmd = ['cmo_abra',
                '--version', '2.07',
                '--in', ",".join([tumor_bam, normal_bam]),
                "--out", ",".join([output, output2]),
                '--reference_sequence', genome_string,
                '--targets', input_bed,
                '--working', abratmpdir]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True)
	print prog_output
        #check prog_output to see if it picked up the arguments we gave...
        assert_true(re.search("input0: /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
        assert_true(re.search("input0: /ifs/work/pi/testdata/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
        assert_true(re.search("regions: /ifs/work/pi/testdata/testdata_for_cmo/intervals.bed", prog_output))
        assert_true(re.search("reference: /ifs/work/pi/testdata/assemblies/b37/b37.fasta", prog_output))
        assert_true(re.search("working dir: "+current_dir+"/abra_cmo_test/", prog_output))'''

    def test_abra_default(self):
        cmd = ['cmo_abra',
                '--version', '2.12',
		'--in', ",".join([tumor_bam, normal_bam]),
                "--out", ",".join([output, output2]),
                '--reference_sequence', genome_string,
                '--targets', input_bed,
                '--working', abratmpdir]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        #check prog_output to see if it picked up the arguments we gave...
	assert_true(re.search("input0: /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
        assert_true(re.search("input0: /ifs/work/pi/testdata/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam", prog_output))
        assert_true(re.search("regions: /ifs/work/pi/testdata/testdata_for_cmo/intervals.bed", prog_output))
        assert_true(re.search("reference: /ifs/work/pi/testdata/assemblies/b37/b37.fasta", prog_output))
        #assert_true(re.search("working dir: "+current_dir+"/abra_cmo_test/", prog_output))

    def test_bwa_mem(self):
        cmd = ["cmo_bwa_mem",
                "--fastq1", fastq1,
                "--fastq2", fastq2,
                "--genome", genome_string,
                "--output", output,
                "--version", '0.7.5a'  ]
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        print prog_output
        assert_true(re.search("0.7.5a", prog_output))

    def test_list2bed(self):
        cmd = ["cmo_list2bed",
                "--input_file", input_list,
                "--no_sort",
                "--output_file", output]
        subprocess.check_call(" ".join(cmd), shell=True)

    def test_mutect(self):
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
        assert_true(re.search("INFO .* HelpFormatter - Program Args: -T MuTect --vcf .* --cosmic /ifs/work/pi/testdata/CosmicCodingMuts_v67_b37_20131024__NDS.vcf --input_file:tumor /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --downsampling_type NONE --input_file:normal /ifs/work/pi/testdata/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam --intervals 22 --dbsnp /ifs/work/pi/testdata/dbsnp_138.b37.excluding_sites_after_129.vcf --enable_extended_output --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta", prog_output))

    def test_printreads(self):
        cmd = ['cmo_gatk',
                '-T', 'PrintReads',
                '--version', '3.3-0',
                '--BQSR', matrix,
                '--input_file', tumor_bam,
                '--java_args',  "'-Xmx48g -Xms256m -XX:-UseGCOverheadLimit'",
                '--num_cpu_threads_per_data_thread', '6',
                '--out', output,
                '--reference_sequence', genome_string]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("INFO  .* HelpFormatter - Program Args: -T PrintReads --input_file /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --num_cpu_threads_per_data_thread 6 --BQSR /ifs/work/pi/testdata/testdata_for_cmo/recal.matrix --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta --out", prog_output))

    def test_baserecal(self):
        cmd= ['cmo_gatk',
                '-T', 'BaseRecalibrator',
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
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("INFO .* HelpFormatter - Program Args: -T BaseRecalibrator --input_file /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta --knownSites /ifs/work/pi/testdata/dbsnp_138.b37.excluding_sites_after_129.vcf --knownSites /ifs/work/pi/testdata/hapmap_3.3.b37.vcf --knownSites /ifs/work/pi/testdata/1000G_phase1.snps.high_confidence.b37.vcf --knownSites /ifs/work/pi/testdata/Mills_and_1000G_gold_standard.indels.b37.vcf --covariate ContextCovariate --covariate CycleCovariate --covariate ReadGroupCovariate --covariate QualityScoreCovariate --out", prog_output))

    def test_addorreplacereadgroups(self):
        cmd = ['cmo_picard',
                '--version 1.129',
                '--cmd', 'AddOrReplaceReadGroups',
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
        #print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)

        print prog_output
        assert_true(re.search("picard.sam.AddOrReplaceReadGroups INPUT=/ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam OUTPUT=.* SORT_ORDER=coordinate RGID=P-0000377 RGLB=5 RGPL=Illumina RGPU=bc26 RGSM=P-0000377-T02-IM3 RGCN=MSKCC .* CREATE_INDEX=true    VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_MD5_FILE=false", prog_output))

    def test_CalculateHsMetrics(self):
        #picard version 1.129 with genome short string
        cmd = ['cmo_picard',
                '--version', '1.129',
                '--cmd', 'CalculateHsMetrics',
                '--BI', bait_interval,
                '--I', normal_bam,
                '--O', output,
                '--PER_TARGET_COVERAGE', per_target_coverage,
                '--R', genome_string,
                '--TI', target_interval,
                '--TMP_DIR', tmpdir,
                '--VALIDATION_STRINGENCY', 'LENIENT',
                '--java-version','default']
        prog_output = subprocess.check_output(" ".join(cmd), shell=True,stderr=subprocess.STDOUT)    
        print prog_output
        CalculateHsMetrics_validation_output = "picard.analysis.directed.CalculateHsMetrics BAIT_INTERVALS=.* TARGET_INTERVALS=.* INPUT=.* OUTPUT=.* PER_TARGET_COVERAGE=.* TMP_DIR=.* VALIDATION_STRINGENCY=LENIENT REFERENCE_SEQUENCE=/ifs/work/pi/testdata/assemblies/b37/b37.fasta    METRIC_ACCUMULATION_LEVEL=\[ALL_READS\] VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false"
        assert_true(re.search(CalculateHsMetrics_validation_output,prog_output))
        #picard version 1.129 with genome path
        #cmd = ['cmo_picard',
        #        '--version', '1.129',
        #        '--cmd', 'CalculateHsMetrics',
        #        '--BI', bait_interval,
        #        '--I', normal_bam,
        #        '--O', output,
        #        '--PER_TARGET_COVERAGE', 'Per_Target_Coverage.txt',
        #        '--REFERENCE_SEQUENCE', GRCh37_path,
        #        '--TI', target_interval,
        #        '--TMP_DIR', tmpdir,
        #        '--VALIDATION_STRINGENCY', 'LENIENT',
        #        '--java-version','default']
        #prog_output2 = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        #assert_true(re.search(CalculateHsMetrics_validation_output,prog_output2))

    def test_CollectMultipleMetrics(self):
        cmd = ['cmo_picard',
                '--version','1.129',
                '--cmd','CollectMultipleMetrics',
                '--AS','true',
                '--I',normal_bam,
                '--O',output,
                '--PROGRAM','null',
                '--PROGRAM','CollectInsertSizeMetrics',
                '--TMP_DIR',tmpdir,
                '--VALIDATION_STRINGENCY',' LENIENT',
                '--java-version','default']
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("picard.analysis.CollectMultipleMetrics INPUT="+normal_bam+" ASSUME_SORTED=true OUTPUT=.* PROGRAM=\[CollectInsertSizeMetrics\] .* VALIDATION_STRINGENCY=LENIENT    STOP_AFTER=0 VERBOSITY=INFO QUIET=false COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false",prog_output))

    def test_DepthOfCoverage(self):
        cmd = ['cmo_gatk',
                '-T','DepthOfCoverage',
                '--input_file',normal_bam,
                '--intervals','1:1-1000000',
                '--java_args',"'-Xmx48g -Xms256m -XX:-UseGCOverheadLimit'",
                '--java-version','default',
                '--minBaseQuality','3',
                '--minMappingQuality','10',
                '--omitIntervalStatistics','--omitLocusTable',
                '--omitPerSampleStats',
                '--out',output,
                '--printBaseCounts',
                '--read_filter','BadCigar',
                '--reference_sequence','GRCh37',
                '--version','3.3-0']
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("INFO .* HelpFormatter - Program Args: -T DepthOfCoverage --input_file "+normal_bam+" --printBaseCounts --omitPerSampleStats --minBaseQuality 3 --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta --intervals 1:1-1000000 --out "+output+" --read_filter BadCigar --omitLocusTable --minMappingQuality 10 --omitIntervalStatistics",prog_output))

    def test_trimgalore(self):
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
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true("/opt/common/CentOS_6/trim_galore/Trim_Galore_v0.2.5/trim_galore --adapter AGATCGGAAGAGCACACGTCTGAACTCCAGTCACATGAGCATCTCGTATGCCGTCTTCTGCTTG --suppress_warn --paired --length 25 --gzip --quality 1 --adapter2 AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT /ifs/work/pi/testdata/testdata_for_cmo/P1_R1.fastq.gz /ifs/work/pi/testdata/testdata_for_cmo/P1_R2.fastq.gz", prog_output)


    def test_vardict(self):
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
        print " ".join(cmd)
        subprocess.check_call(" ".join(cmd), shell=True)


    def test_somaticindeldetector(self):
        cmd = ['cmo_gatk',
                '--version', '2.3-9',
                '-T', 'SomaticIndelDetector',
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
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("INFO  .* HelpFormatter - Program Args: -T SomaticIndelDetector --input_file:normal /ifs/work/pi/testdata/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam --input_file:tumor /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --min_mapping_quality_score 20 --intervals /ifs/work/pi/testdata/testdata_for_cmo/intervals.bed --filter_expressions T_COV<10||N_COV<4||T_INDEL_F<0.0001||T_INDEL_CF<0.7 --maxNumberOfReads 100000 --verboseOutput .* --read_filter DuplicateRead --read_filter FailsVendorQualityCheck --read_filter NotPrimaryAlignment --read_filter BadMate --read_filter MappingQualityUnavailable --read_filter UnmappedRead --read_filter MappingQuality --read_filter BadCigar --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta --out .*", prog_output))

    def test_findcoveredintervals(self):
        cmd = ['cmo_gatk',
                '--version', '3.3-0',
                '-T','FindCoveredIntervals',
                '--input_file',tumor_bam,
                '--java_args','"-Xmx48g -Xms256m -XX:-UseGCOverheadLimit"',
                '--out',output,
                '--reference_sequence', genome_string,
                '--input_file',normal_bam]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd),shell=True, stderr=subprocess.STDOUT)
        assert_true(re.search("INFO  .* HelpFormatter - Program Args: -T FindCoveredIntervals --input_file /ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam --input_file /ifs/work/pi/testdata/testdata_for_cmo/P2_ADDRG_MD.abra.fmi.printreads.bam --out .* --reference_sequence /ifs/work/pi/testdata/assemblies/b37/b37.fasta",prog_output))

    def test_pindel(self):
        cmd = ['cmo_pindel',
               '--version','0.2.5a7',
               '--bams','"'+normal_bam+' '+tumor_bam+'"',
               '--fasta',genome_string,
               '--output-prefix','Tumor',
               '--sample_names','"Normal Tumor"']

        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd),shell=True, stderr=subprocess.STDOUT)
        #print prog_output
        assert_true(re.search(tumor_bam,prog_output))
        assert_true(re.search(normal_bam,prog_output))
        assert_true(re.search("call_cmd INFO EXECUTING: sing.sh pindel 0.2.5a7 pindel --fasta /ifs/work/pi/testdata/assemblies/b37/b37.fasta --config-file temp.config --output-prefix Tumor",prog_output))
        with open('temp.config') as configFile:
            configFileStr = configFile.read()
        assert_true(re.search("Normal",configFileStr))
        assert_true(re.search("Tumor",configFileStr))
    def test_index(self):
        cmd = ['cmo_index',
               '--normal',normal_bam,
               '--tumor',tumor_bam]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd),shell=True,stderr=subprocess.STDOUT)
        assert_true(re.search(normal_bam,prog_output))
        assert_true(re.search(tumor_bam,prog_output))

    def test_markduplicates(self):
        cmd = ['cmo_picard',
                '--version 1.129',
                '--cmd', 'MarkDuplicates',
                '--CREATE_INDEX',
                '--I', tumor_bam,
                '--M', output2,
                '--O', output,
                '--TMP_DIR', tmpdir
                ]
        print " ".join(cmd)
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        print prog_output
        assert_true(re.search("INPUT=\[/ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam\] OUTPUT=.* METRICS_FILE=.* TMP_DIR=.* CREATE_INDEX=true.*", prog_output))

    def test_fixmateinformation(self):
        cmd = ['cmo_picard',
                '--version 1.129',
                '--cmd', 'FixMateInformation',
                '--I', tumor_bam,
                '--O', output]
        print cmd
        prog_output = subprocess.check_output(" ".join(cmd), shell=True, stderr=subprocess.STDOUT)
        print prog_output
        assert_true(re.search("INPUT=\[/ifs/work/pi/testdata/testdata_for_cmo/P1_ADDRG_MD.abra.fmi.printreads.bam\] OUTPUT=.* VERBOSITY=INFO QUIET=false VALIDATION_STRINGENCY=STRICT COMPRESSION_LEVEL=5 MAX_RECORDS_IN_RAM=500000 CREATE_INDEX=false CREATE_MD5_FILE=false", prog_output))
    




            





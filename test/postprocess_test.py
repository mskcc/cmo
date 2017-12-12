import tempfile, subprocess, shutil, os
from nose.tools import nottest

TEST_TEMP_DIR = None
TEST_DATA_DIR = "/ifs/work/pi/testdata/postprocess/"
test_expected_outputs = {
        "filter_haplotype": "filt_haplotype.short",
        "filter_mutect": "filt_mutect.short",
        "merge_mafs": "merge_maf3.short",
        "maf2maf" : "merge_maf3.vep",
        "trinuc_impact": "trinuc_impact.short",
        "trinuc_seq":"trinuc_seq.short",
        "add_variant_info":"sorted_expected_maf"
        }

test_inputs = {"pairing_file": "Proj_04525_J_sample_pairing.txt",
        "haplotype_vcf": "Proj_04525_J_HaplotypeCaller.short.vcf",
        "mutect_vcf": "Proj_04525_J_s_JH_rec3_041_N_s_JH_rec3_041_P2_mutect_calls.short.vcf"}
dev_null = open("/dev/null", "w")

for key, value in test_inputs.items():
    test_inputs[key]= os.path.join(TEST_DATA_DIR, "inputs", value)

for key, value in test_expected_outputs.items():
    test_expected_outputs[key] = os.path.join(TEST_DATA_DIR, value)

def setup_module():
    global TEST_TEMP_DIR
    TEST_TEMP_DIR = tempfile.mkdtemp();


def teardown_module():
    if TEST_TEMP_DIR is not None:
        pass
#        shutil.rmtree(TEST_TEMP_DIR)

def test_filter_haplotype():
    expected_output = test_expected_outputs['filter_haplotype']
    test_output = os.path.join(TEST_TEMP_DIR, "filt_haplotype")
    cmd = ['cmo_filter_haplotype', 
            '--pairing-file', test_inputs['pairing_file'], 
            '--haplotype-vcf', test_inputs['haplotype_vcf'], 
            '--output-file', test_output,
            '--temp-dir', TEST_TEMP_DIR]
    try:
        print " ".join(cmd)
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False
    diff_cmd = ['diff', expected_output, test_output]
    try:
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "Differences between expected haplotype filter output and test output"
   

@nottest
def test_filter_mutect():
    expected_output = test_expected_outputs['filter_mutect']
    test_output = os.path.join(TEST_TEMP_DIR, "filt_mutect")
    cmd = ['cmo_filter_mutect', 
            '--pairing-file', test_inputs['pairing_file'],
            '--mutect-vcf', test_inputs['mutect_vcf'], 
            '--output-file', test_output,
            '--temp-dir', TEST_TEMP_DIR]
    try:
        print " ".join(cmd)
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "Unable to run cmo_filter_mutect"
    diff_cmd = ['diff', expected_output, test_output]
    try:
        rv = subprocess.call(diff_cmd, stderr=dev_null)
        assert rv==0
    except: 
        assert False, "diff between expected output and test-generated output"



def test_merge_mafs():
    expected_output = test_expected_outputs['merge_mafs']
    test_output = os.path.join(TEST_TEMP_DIR, "merge_maf")
    cmd = ['cmo_merge_mafs', 
            test_expected_outputs['filter_mutect'], 
            test_expected_outputs['filter_haplotype'],
            '--output-file', test_output]
    try:
        print " ".join(cmd)
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "Couldn't run cmo_merge_mafs correctly"
    diff_cmd = ['diff', test_output, expected_output]
    try:
        rv = subprocess.call(diff_cmd, stderr=dev_null, stdout=dev_null)
        assert rv==0
    except:
        assert False, "merge_mafs expected output doesn't match newly test generated output"


@nottest
def test_maf2maf():
    expected_output = test_expected_outputs['maf2maf']
    test_output = os.path.join(TEST_TEMP_DIR, 'maf.vep')
    retain_cols = "Center,Verification_Status,Validation_Status,Mutation_Status,Sequencing_Phase,Sequence_Source,Validation_Method,Score,BAM_file,Sequencer,Tumor_Sample_UUID,Matched_Norm_Sample_UUID,Caller"
    cmd = ['cmo_maf2maf',
            '--version', 'develop',
            '--vep-forks', '12',
            '--vep-path', '/opt/common/CentOS_6-dev/vep/v81/',
            '--vep-data', '/opt/common/CentOS_6-dev/vep/v81/',
            '--retain-cols', retain_cols,
            '--custom-enst', '/opt/common/CentOS_6-dev/vcf2maf/develop/data/isoform_overrides_at_mskcc',
            '--input-maf', test_expected_outputs['merge_mafs'],
            '--output-maf', test_output]
    rv = subprocess.call(cmd, stderr=dev_null, stdout=dev_null)
    assert rv==0
    diff_cmd = ['diff', expected_output, test_output]
    rv = subprocess.call(cmd, stderr=dev_null)
    assert rv==0


@nottest
def test_trinuc():
    expected_impact = test_expected_outputs['trinuc_impact']
    expected_seq = test_expected_outputs['trinuc_seq']
    test_seq = os.path.join(TEST_TEMP_DIR, "trinuc_seq")
    test_impact = os.path.join(TEST_TEMP_DIR, "trinuc_impact")
    cmd = ['cmo_trinuc_and_impact', 
            '--source-file', test_expected_outputs['merge_mafs'],
            '--genome', 'hg19',
            '--output-seq', test_seq,
            '--output-impact', test_impact ]
    try:
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "unable to run cmo_trinuc_and_impact wihtout errors"
    try:
        diff_cmd = ['diff', expected_impact, test_impact]
        rv = subprocess.call(diff_cmd, stderr=dev_null)
        assert rv==0
    except: 
        assert False, "diff shows differences between expected impact and test-generated impact output"
    try:
        diff_cmd = ['diff', expected_seq, test_seq]
        rv = subprocess.call(diff_cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "diff shows differences between expected seq and test-generated sequence output"

def test_add_variant_info():
    expected_output = test_expected_outputs['add_variant_info']
    test_output = os.path.join(TEST_TEMP_DIR, 'final_maf')
    cmd = ['cmo_add_variant_info',
            '--sequence-data-file', test_expected_outputs['trinuc_seq'],
            '--impact-positions', test_expected_outputs['trinuc_impact'],
            '--original-maf', test_expected_outputs['maf2maf'],
            '--output-file', test_output]
    try:
        rv = subprocess.call(cmd, stderr=dev_null)
        assert rv==0
    except:
        assert False, "unable to run add_variant_info: %s" % " ".join(cmd)
    test_sorted_output = os.path.join(TEST_TEMP_DIR, "sorted_final_maf")
    sort_cmd = ["sort" , "-k5,6n", test_output, ">", test_sorted_output]
    print " ".join(sort_cmd)
    rv = subprocess.call(" ".join(sort_cmd), shell=True, stderr=dev_null)
    diff_cmd = ['diff', expected_output, test_sorted_output]
    try:
        rv = subprocess.call(diff_cmd, stderr=dev_null, stdout=dev_null)
        assert rv==0
    except:
        assert False, "diff shows difference between expected output of cmo_add_variant_info and test-generated output"




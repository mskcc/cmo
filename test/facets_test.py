import tempfile, subprocess, shutil, os

TEST_TEMP_DIR = None
TEST_DATA_DIR = "/ifs/res/pwg/tests/cmo_testdata/facets/"
def setup_module():
    global TEST_TEMP_DIR
    TEST_TEMP_DIR = tempfile.mkdtemp();

def teardown_module():
    if TEST_TEMP_DIR is not None:
        shutil.rmtree(TEST_TEMP_DIR)

def test_getbasecounts():
    input_bam_file = os.path.join(TEST_DATA_DIR, "Chr22_hg19_TCGA-A8-A094-01A-11W-A019-09.tumor.bam")
    input_vcf_file = os.path.join(TEST_DATA_DIR, "/ifs/res/pwg/tests/cmo_testdata/facets/dbsnp_137.chr22.snp.positions.hg19.vcf.gz")
    output_file = os.path.join(TEST_TEMP_DIR, "test_getbascounts_output")
    cmd = ["cmo_getbasecounts", "--bam", input_bam_file,
            "--out", output_file, "--sort_output", "--compress_output",  "--filter_improper_pair", "0",
            "--vcf", input_vcf_file ]
    rv = subprocess.check_call(cmd)
    assert rv==0, "cmo_getbascounts threw shell error (program failed)"
    expected_output= os.path.join(TEST_DATA_DIR, "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1/", "H_LS-A8-A094-01A-11W-A019-09-1.dat.gz")
    
    diff_cmd = ['diff', expected_output, output_file+".gz"]
    rv = subprocess.check_call(diff_cmd)
    assert rv==0, "getbasecounts output does not match expected output"

def test_mergeTN():
    input_tumor = os.path.join(TEST_DATA_DIR, 
            "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1/",
            "H_LS-A8-A094-01A-11W-A019-09-1.dat.gz")
    input_normal = os.path.join(TEST_DATA_DIR, 
            "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1/",
            "H_LS-A8-A094-10A-01W-A021-09-1.dat.gz")
    test_output = os.path.join(TEST_TEMP_DIR, "test_countsmerged.gz")
    cmd = ["cmo_facets", "mergeTN", input_tumor, input_normal, test_output]
    rv = subprocess.check_call(cmd)
    assert rv==0, "cmo_facets mergeTN threw shell error(program failed)"
    expected_output= os.path.join(TEST_DATA_DIR,
        "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1/", 
        "countsMerged____H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1.dat.gz")
    shutil.copy(expected_output, TEST_TEMP_DIR)
    temp_expected_output = os.path.join(TEST_TEMP_DIR, os.path.basename(expected_output))
    gunzip_cmd = ["gunzip", temp_expected_output]
    subprocess.call(gunzip_cmd)
    gunzip_cmd = [ "gunzip", test_output]
    subprocess.call(gunzip_cmd)
    temp_expected_output= temp_expected_output.replace(".gz", "")
    test_output = test_output.replace(".gz", "")
    diff_cmd = ["diff", test_output, temp_expected_output]
    rv = subprocess.check_call(diff_cmd)
    assert rv==0, "cmo_facets mergeTN output does not match expected output"

def test_facets():
    output_dir = os.path.join(TEST_TEMP_DIR)
    facets_cmd = ["cmo_facets", "run", "/ifs/res/pwg/tests/cmo_testdata/facets/countsMerged____TCGA-A8-A094-01A-11W-A019-09____TCGA-A8-A094-10A-01W-A021-09.dat.gz", " H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1", TEST_TEMP_DIR, "-c 200", "-pc 300"]
    rv = subprocess.check_call(facets_cmd)
    assert rv==0, "facets failed to run :("
    expected_seg_output = os.path.join(TEST_DATA_DIR, "TCGA-A8-A094-01A-11W-A019-09__TCGA-A8-A094-10A-01W-A021-09/facets_c300/", "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1_hisens.seg")
    test_seg_output = os.path.join(TEST_TEMP_DIR, "H_LS-A8-A094-01A-11W-A019-09-1__H_LS-A8-A094-10A-01W-A021-09-1_hisens.seg")
    diff_cmd = ["diff", expected_seg_output, test_seg_output]
    rv = subprocess.check_call(diff_cmd)
    assert rv==0, "facets test seg output differs from expected output!"


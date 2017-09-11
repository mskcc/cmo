#!/usr/bin/env cwl-runner
# This tool description was generated automatically by argparse2cwl ver. 0.3.1
# To generate again: $ cmo_vcf2maf --generate_cwl_tool
# Help: $ cmo_vcf2maf --help_arg2cwl

cwlVersion: "cwl:v1.0"

class: CommandLineTool
baseCommand: ['cmo_vcf2maf']

doc: |
  None

inputs:
  
  version:
    type:
    - "null"
    - type: enum
      symbols: [u'default']
    default: default
    doc: Version of tool to run
    inputBinding:
      prefix: --version 

  vep_release:
    type:
    - "null"
    - type: enum
      symbols: [u'default']
    default: default
    doc: Version of VEP and its cache to use
    inputBinding:
      prefix: --vep-release 

  species:
    type:
    - "null"
    - type: enum
      symbols: ['homo_sapiens', 'mus_musculus']
    default: homo_sapiens
    doc: Species of variants in input
    inputBinding:
      prefix: --species 

  ncbi_build:
    type:
    - "null"
    - type: enum
      symbols: ['GRCh37', 'GRCh38', 'GRCm38']
    default: GRCh37
    doc: Genome build of variants in input
    inputBinding:
      prefix: --ncbi-build 

  ref_fasta:
    type: ["null", str]
    default: /ifs/depot/assemblies/H.sapiens/b37/b37.fasta
    doc: Reference FASTA file 
    inputBinding:
      prefix: --ref-fasta 

  maf_center:
    type: ["null", str]
    default: mskcc.org
    doc: Variant calling center to report in MAF 
    inputBinding:
      prefix: --maf-center 

  output_maf:
    type: ["null", str]
    doc: Path to output MAF file 
    inputBinding:
      prefix: --output-maf 

  max_filter_ac:
    type: ["null", str]
    default: 10
    doc: Use tag common_variant if the filter-vcf reports a subpopulation AC higher than this 
    inputBinding:
      prefix: --max-filter-ac 

  min_hom_vaf:
    type: ["null", str]
    default: 0.7
    doc: If GT undefined in VCF, minimum allele fraction to call a variant homozygous 
    inputBinding:
      prefix: --min-hom-vaf 

  remap_chain:
    type: ["null", str]
    doc: Chain file to remap variants to a different assembly before running VEP
    inputBinding:
      prefix: --remap-chain 

  normal_id:
    type: ["null", str]
    default: NORMAL
    doc: Matched_Norm_Sample_Barcode to report in the MAF 
    inputBinding:
      prefix: --normal-id 

  buffer_size:
    type: ["null", str]
    default: 5000
    doc: Number of variants VEP loads at a time; Reduce this for low memory systems 
    inputBinding:
      prefix: --buffer-size 

  custom_enst:
    type: ["null", str]
    default: sudo docker run -i vcf2maf:1.6.14 data/isoform_overrides_at_mskcc
    doc: List of custom ENST IDs that override canonical selection
    inputBinding:
      prefix: --custom-enst 

  vcf_normal_id:
    type: ["null", str]
    default: NORMAL
    doc: Matched normal ID used in VCF's genotype columns 
    inputBinding:
      prefix: --vcf-normal-id 

  vep_path:
    type: ["null", str]
    default: sudo docker run -i vep:86
    doc: Folder containing variant_effect_predictor.pl 
    inputBinding:
      prefix: --vep-path 

  vep_data:
    type: ["null", str]
    default: /opt/common/CentOS_6-dev/vep/v86/
    doc: VEP's base cache/plugin directory 
    inputBinding:
      prefix: --vep-data 

  any_allele:
    type: ["null", str]
    doc: When reporting co-located variants, allow mismatched variant alleles too
    inputBinding:
      prefix: --any-allele 

  tmp_dir:
    type: ["null", str]
    default: /scratch/<username>/...
    doc: Folder to retain intermediate VCFs after runtime 
    inputBinding:
      prefix: --tmp-dir 

  input_vcf:
    type: ["null", str]
    doc: Path to input file in VCF format
    inputBinding:
      prefix: --input-vcf 

  vep_forks:
    type: ["null", str]
    default: 4
    doc: Number of forked processes to use when running VEP 
    inputBinding:
      prefix: --vep-forks 

  vcf_tumor_id:
    type: ["null", str]
    default: TUMOR
    doc: Tumor sample ID used in VCF's genotype columns 
    inputBinding:
      prefix: --vcf-tumor-id 

  tumor_id:
    type: ["null", str]
    default: TUMOR
    doc: Tumor_Sample_Barcode to report in the MAF 
    inputBinding:
      prefix: --tumor-id 

  filter_vcf:
    type: ["null", str]
    default: /opt/common/CentOS_6-dev/vep/v86/ExAC_nonTCGA.r0.3.1.sites.vep.vcf.gz
    doc: The non-TCGA VCF from exac.broadinstitute.org 
    inputBinding:
      prefix: --filter-vcf 

  retain_info:
    type: ["null", str]
    doc: Comma-delimited names of INFO fields to retain as extra columns in MAF 
    inputBinding:
      prefix: --retain-info 


outputs:
    []

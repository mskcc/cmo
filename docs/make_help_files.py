#!/opt/common/CentOS_6-dev/python/python-2.7.10/bin/python

import os,sys,re

scripts = os.listdir("../bin/")

source_dir = "source/"

wraplist = open("source/wrapperlist.rst", "w")
wraplist.write("================\n")
wraplist.write("List of wrappers\n")
wraplist.write("================\n")
wraplist.write("\n")
wraplist.write(".. toctree::\n")
wraplist.write("    :titlesonly:\n")
wraplist.write("\n")

bedtools_commands = ["tagBam","getOverlap","genomeCoverageBed","linksBed","bamToFastq","pairToPair","multiIntersectBed","nucBed","multiBamCov","bedToBam","groupBy","annotateBed","closestBed","expandCols","pairToBed","maskFastaFromBed","clusterBed","complementBed","mergeBed","flankBed","coverageBed","fastaFromBed","bedpeToBam","bamToBed","subtractBed","bed12ToBed6","randomBed","slopBed","mapBed","intersectBed","bedToIgv","sortBed","windowBed","windowMaker","shuffleBed","unionBedGraphs"]

picard_commands = ["CreateSequenceDictionary", "ExtractSequences", "NormalizeFasta", "CheckIlluminaDirectory", "CollectIlluminaBasecallingMetrics", "CollectIlluminaLaneMetrics", "ExtractIlluminaBarcodes", "IlluminaBasecallsToFastq", "IlluminaBasecallsToSam", "MarkIlluminaAdapters", "BedToIntervalList", "IntervalListTools", "LiftOverIntervalList", "ScatterIntervalsByNs", "CalculateHsMetrics", "CollectAlignmentSummaryMetrics", "CollectBaseDistributionByCycle", "CollectGcBiasMetrics",     "CollectHiSeqXPfFailMetrics", "CollectInsertSizeMetrics", "CollectJumpingLibraryMetrics", "CollectMultipleMetrics", "CollectOxoGMetrics", "CollectQualityYieldMetrics", "CollectRawWgsMetrics", "CollectRnaSeqMetrics", "CollectRrbsMetrics", "CollectTargetedPcrMetrics", "CollectWgsMetrics", "EstimateLibraryComplexity", "MeanQualityByCycle", "QualityScoreDistribution", "BaitDesigner", "FifoBuffer", "AddCommentsToBam", "AddOrReplaceReadGroups", "BamIndexStats", "BamToBfq", "BuildBamIndex", "CalculateReadGroupChecksum", "CheckTerminatorBlock", "CleanSam", "CompareSAMs", "DownsampleSam"    , "FastqToSam", "FilterSamReads", "FixMateInformation", "GatherBamFiles", "MarkDuplicates", "MarkDuplicatesWithMateCigar", "MergeBamAlignment", "MergeSamFiles", "ReorderSam", "ReplaceSamHeader", "RevertOriginalBaseQualitiesAndAddMateCigar", "RevertSam", "SamFormatConverter", "SamToFastq", "SortSam", "SplitSamByLibrary", "ValidateSamFile", "ViewSam",     "FilterVcf", "GatherVcfs", "GenotypeConcordance", "MakeSitesOnlyVcf", "MergeVcfs", "RenameSampleInVcf", "SortVcf", "SplitVcfs", "UpdateVcfSequenceDictionary", "VcfFormatConverter", "VcfToIntervalList"]

gatk_commands = ["VariantAnnotator", "BeagleOutputToVCF", "ProduceBeagleInput", "VariantsToBeagleUnphased", "AnalyzeCovariates", "BaseRecalibrator", "CallableLoci", "CompareCallableLoci", "DepthOfCoverage", "GCContentByInterval", "DiagnoseTargets", "BaseCoverageDistribution", "CoveredByNSamplesSites", "ErrorRatePerCycle", "FindCoveredIntervals", "ReadGroupProperties", "ReadLengthDistribution", "GATKPaperGenotyper", "FastaAlternateReferenceMaker", "FastaReferenceMaker", "FastaStats", "VariantFiltration", "UnifiedGenotyper", "HaplotypeCaller", "HaplotypeResolver", "IndelRealigner", "LeftAlignIndels", "RealignerTargetCreator", "QualifyMissingIntervals", "PhaseByTransmission", "ReadBackedPhasing", "CheckPileup", "CountBases", "CountIntervals", "CountLoci", "CountMales", "CountReadEvents", "CountReads", "CountRODs", "CountRODsByRef", "CountTerminusEvent", "ErrorThrowing", "FlagStat", "Pileup", "PrintRODs", "QCRef", "ReadClippingStats", "ClipReads", "PrintReads", "ReadAdaptorTrimmer", "SplitSamFile", "ASEReadCounter", "SplitNCigarReads", "SimulateReadsForVariants", "GenotypeAndValidate", "Genotyper", "ValidationSiteSelector", "VariantEval", "ApplyRecalibration", "VariantRecalibrator", "CalculateGenotypePosteriors", "CombineGVCFs", "CombineVariants", "FilterLiftedVariants", "GenotypeConcordance", "GenotypeGVCFs", "LeftAlignAndTrimVariants", "LiftoverVariants", "RandomlySplitVariants", "RegenotypeVariants", "SelectHeaders", "SelectVariants", "ValidateVariants", "VariantsToAllelicPrimitives", "VariantsToBinaryPed", "VariantsToTable", "VariantsToVCF", "VariantValidationAssessor"]
for script in scripts:
    underbar_name = script.replace("-","_")
    filename = os.path.join(source_dir, underbar_name + ".rst")
    fh = open(filename, "w")
    header = len(script) * "="
    fh.write(header + "\n")
    fh.write(script + "\n")
    fh.write(header + "\n")
    if script == "cmo_bedtools":
        for command in bedtools_commands:
            fh.write(command + "\n")
            underline = len(command) * "#"
            fh.write(underline + "\n")
            fh.write(".. program-output:: %s --cmd %s -h\n\n" % (script, command))
    elif script == "cmo_picard":
        for command in picard_commands:
            fh.write(command + "\n")
            underline = len(command) * "#"
            fh.write(underline + "\n")
            fh.write(".. program-output:: %s --cmd %s -h\n\n" % (script, command))
    elif script == "cmo_gatk":
        for command in gatk_commands:
            fh.write(command + "\n")
            underline = len(command) * "#"
            fh.write(underline + "\n")
            fh.write(".. program-output:: %s --cmd %s -h\n\n" % (script, command))
    else:
        fh.write(".. program-output:: %s -h" % script)
    fh.close()
    wraplist.write("    " + underbar_name+"\n")

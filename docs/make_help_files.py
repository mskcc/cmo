#!/opt/common/CentOS_6-dev/python/python-2.7.10/bin/python

import os,sys,re

scripts= os.listdir("../bin/")

source_dir = "source/"

wraplist=open("source/wrapperlist.rst", "w")
wraplist.write("================\n")
wraplist.write("List of wrappers\n")
wraplist.write("================\n")
wraplist.write("\n")
wraplist.write(".. toctree::\n")
wraplist.write("    :titlesonly:\n")
wraplist.write("\n")

bedtools_commands=["tagBam","getOverlap","genomeCoverageBed","linksBed","bamToFastq","pairToPair","multiIntersectBed","nucBed","multiBamCov","bedToBam","groupBy","annotateBed","closestBed","expandCols","pairToBed","maskFastaFromBed","clusterBed","complementBed","mergeBed","flankBed","coverageBed","fastaFromBed","bedpeToBam","bamToBed","subtractBed","bed12ToBed6","randomBed","slopBed","mapBed","intersectBed","bedToIgv","sortBed","windowBed","windowMaker","shuffleBed","unionBedGraphs"]

for script in scripts:
    underbar_name = script.replace("-","_")
    filename=os.path.join(source_dir, underbar_name + ".rst")
    fh = open(filename, "w")
    header = len(script) * "="
    fh.write(header + "\n")
    fh.write(script + "\n")
    fh.write(header + "\n")
    if script=="cmo_bedtools":
        for command in bedtools_commands:
            fh.write(command + "\n")
            underline = len(command) * "#"
            fh.write(underline + "\n")
            fh.write(".. program-output:: %s --cmd %s -h\n\n" % (script, command))
    else:
        fh.write(".. program-output:: %s -h" % script)
    fh.close()
    wraplist.write("    " +underbar_name+"\n")

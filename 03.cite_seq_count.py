#!/usr/bin/env python3

# $1 = tags.csv
# $2 = umitransformed.fq.gz
# $3 = samples.csv

import sys
import gzip

# index = sample + cell = dict
# dict elements {} ab = [list of UMIs]
# cell
#  
result_table = {}

# open tags.csv
tags = {}
with open(sys.argv[1]) as f_tags:
    for line in f_tags:
        barcode, ab = line.strip().split(",")
        tags[barcode] = ab

samples = {}
with open(sys.argv[3]) as f_samples:
    for line in f_samples:
        sample_name, barcode = line.strip().split(",")
        samples[barcode] = sample_name

i = 0
# open umitransformed.fq.gz
with gzip.open(sys.argv[2]) as fq:
    cell = ""
    umi = ""
    sample = ""
    sample_barcode = ""
    ab_barcode = ""
    for line in fq:
        i += 1
        if i % 4 == 1:
            line = line.decode().strip()
            header, read = line.split(":CELL_", 2)
            cell, umi, sample_barcode = read.split(":")
            umi = umi.replace("UMI_", "")
            sample_barcode = sample_barcode.replace("SAMPLE_", "")
            if sample_barcode in samples:
                sample = samples[sample_barcode]
            else:
                sample = ""
        elif i % 4 == 2:
            ab_barcode = line.decode().strip()[21:36]
        elif i % 4 == 0:
            if ab_barcode in tags:
                merger = cell + umi
                print("sample: " + sample)
                print("merger: " + merger)
                if (sample != "") and ("N" not in merger):
                    sindex = sample + "_" + cell
                    print("sindes: " + sindex)
                    ab = tags[ab_barcode]
                    if sindex in result_table:
                        record = result_table[sindex]
                        if ab not in record:
                            result_table[sindex][ab] = []
                        result_table[sindex][ab].append(umi)
                    else:
                        d = dict()
                        d[ab] = []
                        d[ab].append(umi)
                        result_table[sindex] = d
            cell = ""
            umi = ""
            sample = ""
            ab_barcode = ""
            sample_barcode = ""

antibodies = []
for k in tags:
    antibodies.append(tags[k])

print("sampleid_cellid," + ",".join(antibodies))

for sindex in result_table:
    counts = []
    for k in antibodies:
        if k in result_table[sindex]:
            counts.append(str(len(set(result_table[sindex][k]))))
        else:
            counts.append("0")
    print(sindex + "," + ",".join(counts))

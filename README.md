
https://github.com/Hoohm/CITE-seq-Count/issues/108

- bcbio_R1 = R1 = 61bp - bases 22 - 36 = 15 bp antibody motif
- bcbio_R2 = I1 = 8 bp part 1 of cell barcode
- bcbio_R3 = I2 = 8 bp sample (library) barcode
- bcbio_R4 = R2 = 14 bp = 8 bp - using as a part 2 of cell barcode + 6 bp of transcript UMI - used to filter PCR duplicates

# Methods
- 01_bcl2fq.sh: We converted binary files from the Illumina run to fastq files corresponding to 4 reads of indrops3 library with bcl2fastq/2.18.0.12 without read trimming. https://support.illumina.com/sequencing/sequencing_software/bcl2fastq-conversion-software.html
- 02_cite_seq.sh: We created a single fastq file containing cellular and sample barcode information in the header of the read with `umis fastqtransform`
https://github.com/vals/umis.
- 03.cite_seq_count.py - we wrote a custrom python script to count antibody barcodes and assign the counts to a proper cell/sample pair. The input parameters of the script were antibody barcodes (tags), a fastq file from step2, and a list of sample barcodes. We ran the script using the wrapper. https://github.com/hbc/rowe2020_indrop_citeseq_hbc03948/blob/master/04.cite_seq_count.sh 

The source code for all of the steps is avaliable at https://github.com/hbc/rowe2020_indrop_citeseq_hbc03948.


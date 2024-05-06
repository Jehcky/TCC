### About the Project

#### Python version: 3.11.3

#### Docker Image

The docker image used to build this project can be found at docker hub, just search for 'continuumio/anaconda3'.

#### List of tools needed to run this project (version used)
1. bedtools (v2.30.0)
2. bcftools (1.11) using htslib (1.11-4)
3. minimap2 (2.17-r941)
4. samtools (1.11)
5. pilon 
6. bwa (0.7.17-r1188)
7. trimmomatic (0.39)
8. mafft (7.505)
9. selenium w/ chromedriver (obs.: web scraping is not required at this point to run the project, I was just experimenting, this tool is optional)
10. SPAdes (3.15.5)
11. hashable
12. pysam
13. pyvcf

#### Running the pipeline

In order to run this pipeline, you must provide input genome files. The files must be located in the dataset/FASTQ/ folder. The files must be in .fastq.gz format. Reference sequence files must be located in implementation/RefSeq/ folder. After doing so, all you have to do is run the .py files located in each of the numbered folders in the following order: 

1. implementation/00_pipeline_Trimmomatic/00_Trimmomatic.py
2. implementation/01_single_alignment_mafft/01_Single_Alignment.py
3. implementation/03_Find_SNPs/SNP_finder.py

The other numbered folders not mentioned here were experiments and are not required to run the project.

All the output files generated will be located in the result folder.

After following these steps you'll see console output showing all SNPs found. Then you'll have to manually compare them with mutation tables for each blood group analyzed. Of course, this step will need to be automatized in the future.

If you have any questions about this project, you can contact me sending an e-mail to jehck.tnj@gmail.com. Happy hunting! 

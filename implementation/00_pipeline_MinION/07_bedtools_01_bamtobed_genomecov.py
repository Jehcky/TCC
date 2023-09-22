import subprocess
import os
import Gene

# echo -e "$REF_NAME\t$LENGTH" > my.genome
# bedtools bamtobed -i $pilon_fasta_file > reads.bed
# bedtools genomecov -bga -i reads.bed -g my.genome | awk '$4 < 20' > zero.bed

REF_FILE_FOLDER = "/home/TCC/result/03_pilon_01/"
OUTPUT_FOLDER = "/home/TCC/result/07_bedtools_01_bamtobed_genomecov/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

pilon_fasta_files = [f for f in os.listdir(REF_FILE_FOLDER) if f.endswith(".Pilon.fasta")]

for ref_file in pilon_fasta_files:

    # 
    ref_file_name = ref_file.rstrip(".Pilon.fasta")
    bam_file = f"/home/TCC/result/02_samtools_02_sort/{ref_file_name}.Pilon.sorted.bam"
    
    if Gene.Gene.RHD.value in ref_file_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in ref_file_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"

    command = f"cat {REF_FILE_FOLDER}{ref_file} | grep '>' | tr -d '>' | cut -d ' ' -f 1"
    ref_name = subprocess.getoutput(command)

    command = f"tail -n +2 {REF_FILE_FOLDER}{ref_file} | tr -d \'\n\' | wc -m | xargs"
    length = subprocess.getoutput(command)
    # 
    
    command = f"echo -e \"{ref_name}\\t{length}\" > {OUTPUT_FOLDER}{ref_file_name}.genome"
    subprocess.call(command, shell=True)

    command = f"bedtools bamtobed -i {bam_file} > {OUTPUT_FOLDER}{ref_file_name}_reads.bed"
    subprocess.call(command, shell=True)

    command = f"bedtools genomecov -bga -i {OUTPUT_FOLDER}{ref_file_name}_reads.bed -g {OUTPUT_FOLDER}{ref_file_name}.genome | awk \'$4 < 20\' > {OUTPUT_FOLDER}{ref_file_name}_zero.bed"
    subprocess.call(command, shell=True)
    print(command)

    command = f"maskFastaFromBed -fi {REF_FILE_FOLDER}{ref_file} -bed {OUTPUT_FOLDER}{ref_file_name}_zero.bed -fo {OUTPUT_FOLDER}{ref_file_name}_masked.fasta"
    #subprocess.call(command, shell=True)
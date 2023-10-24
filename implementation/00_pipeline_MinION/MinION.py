import sys
sys.path.append('/home/TCC/implementation')

import subprocess
import os
import Gene as Gene

# uncompress
import os
import gzip
import shutil

# TODO: Finish MinION pipeline for ION technology sequencing files

def MinION():

    # GET FASTQ FILES
    FASTQ_FOLDER = "/home/TCC/dataset/FASTQ/uncompressed/"
    fastq_files = [f for f in os.listdir(FASTQ_FOLDER) if f.endswith(".fastq")]

    for fastq_file in fastq_files:

        fastq_name = fastq_file.rstrip(".fastq")
        output_folder = f"/home/TCC/result/{fastq_name}/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Get Reference sequence based on gene
        ref_seq = get_ref_seq(fastq_name)

        step_01_minimap2(fastq_name, output_folder, FASTQ_FOLDER, ref_seq)
        step_02_samtools_view(output_folder, fastq_name)
        step_03_samtools_sort(output_folder, fastq_name)
        step_04_samtools_index(output_folder, fastq_name)
        step_05_pilon(output_folder, fastq_name, ref_seq)
        step_06_bwa_index(output_folder, fastq_name)
        step_07_bwa_mem(output_folder, fastq_name)
        step_08_samtools_index(output_folder, fastq_name)
        step_09_consensus(output_folder, fastq_name)
        

def get_ref_seq(fastq_name):
    # Get RefSeq
    if Gene.Gene.RHD.value in fastq_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in fastq_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"

def step_01_minimap2(fastq_name, output_folder, fastq_folder, ref_seq):
    # Execute: minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam
    command = f"minimap2 -ax map-ont {ref_seq} {fastq_folder}{fastq_name}.fastq > {output_folder}{fastq_name}.PrePilon.sam"
    subprocess.call(command, shell=True)
    print(f"Minimap2 map-ont complete. .SAM file saved as {fastq_name}.PrePilon.sam.")

def step_02_samtools_view(output_folder, fastq_name):
    # Execute: samtools view -S -b ${SEQ}.PrePilon.sam > ${SEQ}.PrePilon.bam
    print("Running command: samtools view -S -b ${SEQ}.PrePilon.sam > ${SEQ}.PrePilon.bam")
    sam_file = os.path.basename(output_folder + fastq_name + ".PrePilon.sam")
    file_name = sam_file.rstrip(".PrePilon.sam")
    command = f"samtools view -S -b {output_folder}{file_name}.PrePilon.sam > {output_folder}{file_name}.PrePilon.bam"
    subprocess.call(command, shell=True)
    print(f"Samtools view complete. .BAM file saved as {file_name}.PrePilon.bam.")

def step_03_samtools_sort(output_folder, fastq_name):
    # Execute: samtools sort ${SEQ}.PrePilon.bam -o ${SEQ}.PrePilon.sorted.bam
    bam_file = os.path.basename(output_folder + fastq_name + ".PrePilon.bam")
    file_name = bam_file.rstrip(".PrePilon.bam")
    command = f"samtools sort {output_folder}{file_name}.PrePilon.bam -o {output_folder}{file_name}.PrePilon.sorted.bam"
    subprocess.call(command, shell=True)
    print(f"Samtools sort complete. .BAM file saved as {file_name}.PrePilon.sorted.bam.")

def step_04_samtools_index(output_folder, fastq_name):
    # Execute: samtools index ${SEQ}.PrePilon.sorted.bam
    bam_file = os.path.basename(output_folder + fastq_name + ".PrePilon.bam")
    file_name = bam_file.rstrip(".PrePilon.sorted.bam")
    command = f"samtools index {output_folder}{file_name}.PrePilon.sorted.bam"
    subprocess.call(command, shell=True)
    print(f"Samtools index complete.")

def step_05_pilon(output_folder, fastq_name, ref_seq):
    # Execute: pilon --genome $REF_FILE --frags ${SEQ}.PrePilon.sorted.bam --output ${SEQ}.Pilon --fix "gaps,indels" --threads 1 --mindepth 5
    bam_file = os.path.basename(output_folder + fastq_name + ".PrePilon.sorted.bam")
    file_name = bam_file.rstrip(".PrePilon.sorted.bam")
    command = f"pilon --genome {ref_seq} --frags {output_folder}{bam_file} --output {output_folder}{file_name}.Pilon --fix \"gaps,indels\" --threads 1 --mindepth 5"
    subprocess.call(command, shell=True)
    print(f"Pilon complete. .Pilon file saved as {file_name}.Pilon.fasta")

def step_06_bwa_index(output_folder, fastq_name):
    # Execute: bwa index ${SEQ}.Pilon.fasta
    fasta_file = os.path.basename(output_folder + fastq_name + ".Pilon.fasta")
    file_name = fasta_file.rstrip(".Pilon.fasta")
    command = f"bwa index {output_folder}{file_name}.Pilon.fasta"
    subprocess.call(command, shell=True)
    print(f"BWA index complete. .fasta file saved as {file_name}.Pilon.fasta.")

def step_07_bwa_mem(output_folder, fastq_name):
    # Execute: bwa mem ${SEQ}.Pilon.fasta $FASTQ | samtools sort -o ${SEQ}.Pilon.sorted.bam
    fasta_file = os.path.basename(output_folder + fastq_name + ".Pilon.fasta")
    file_name = fasta_file.rstrip(".Pilon.fasta")
    fastq_file = f"/home/TCC/dataset/FASTQ/uncompressed/{file_name}.fastq"
    if not os.path.isfile(fastq_file):
        print("FASTQ file not found.")
    command = f"bwa mem {output_folder}{file_name}.Pilon.fasta {fastq_file} | samtools sort \\-o {output_folder}{file_name}.Pilon.sorted.bam"
    subprocess.call(command, shell=True)
    print(f"BWA mem & Samtools sort complete. .fasta file saved as {file_name}.Pilon.fasta.")

def step_08_samtools_index(output_folder, fastq_name):
    # Execute: samtools index ${SEQ}.PrePilon.sorted.bam
    bam_file = os.path.basename(output_folder + fastq_name + ".PrePilon.sorted.bam")
    file_name = bam_file.rstrip(".PrePilon.sorted.bam")
    command = f"samtools index {output_folder}{file_name}.PrePilon.sorted.bam"
    subprocess.call(command, shell=True)
    print(f"Samtools index complete. .BAM file saved as {file_name}.PrePilon.sorted.bam.")

def step_09_consensus(output_folder, fastq_name):
    # Execute:
    # REF_FILE1=${SEQ}.Pilon.fasta
    # BAM_FILE=${SEQ}.Pilon.sorted.bam
    # SEQ_NAME=`basename $REF_FILE1 _ref.fasta`
    # REF_NAME=`cat $REF_FILE1 | grep '>' | tr -d '>' | cut -d ' ' -f 1`
    # LENGTH=`tail -n +2 $REF_FILE1 | tr -d '\n' | wc -m | xargs`
    ref_file = os.path.basename(output_folder + fastq_name + ".Pilon.fasta")
    bam_file = os.path.basename(output_folder + fastq_name + ".Pilon.sorted.bam")
    command = f"cat {output_folder}{ref_file} | grep '>' | tr -d '>' | cut -d ' ' -f 1"
    ref_name = subprocess.getoutput(command)
    command = f"tail -n +2 {output_folder}{ref_file} | tr -d \'\n\' | wc -m | xargs"
    length = subprocess.getoutput(command)
        
    # echo -e "$REF_NAME\t$LENGTH" > my.genome
    command = f"echo -e \"{ref_name}\\t{length}\" > {output_folder}{fastq_name}.genome"
    subprocess.call(command, shell=True)

    # bedtools bamtobed -i $BAM_FILE > reads.bed
    command = f"bedtools bamtobed -i {output_folder}{bam_file} > {output_folder}{fastq_name}_reads.bed"
    subprocess.call(command, shell=True)

    # bedtools genomecov -bga -i reads.bed -g my.genome | awk '$4 < 20' > zero.bed
    command = f"bedtools genomecov -bga -i {output_folder}{fastq_name}_reads.bed -g {output_folder}{fastq_name}.genome | awk \'$4 < 20\' > {output_folder}{fastq_name}_zero.bed"
    subprocess.call(command, shell=True)

    # maskFastaFromBed -fi $REF_FILE1 -bed zero.bed -fo masked.fasta
    command = f"maskFastaFromBed -fi {output_folder}{ref_file} -bed {output_folder}{fastq_name}_zero.bed -fo {output_folder}{fastq_name}_masked.fasta"
    subprocess.call(command, shell=True)

    # bcftools mpileup -Ou -f masked.fasta $BAM_FILE | bcftools call --ploidy 1 -mv -Oz -o test.vcf.gz
    # bcftools index test.vcf.gz
    # cat masked.fasta | bcftools consensus test.vcf.gz > new_consensus.fasta
    # echo ">$SEQ_NAME" > $OUTPUT_FILE
    # tail -n +2 new_consensus.fasta >> $OUTPUT_FILE
# EXEC

# uncompress_fastq_gz()
MinION()

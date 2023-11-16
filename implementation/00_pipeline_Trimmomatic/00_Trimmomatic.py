import sys
sys.path.append('/home/TCC/implementation')

import subprocess
import os
import Gene as Gene

import time

def Trimmomatic():
    fastq_gz_folder = "/home/TCC/dataset/FASTQ/"

    print("Running Trimmomatic pipeline...\n")

    r1_files = [f for f in os.listdir(fastq_gz_folder) if (f.endswith(".fastq.gz") and "R1" in f.upper())]
    
    for r1_file in r1_files:
        file_name = r1_file.strip(".fastq.gz")
        file_name_parts = file_name.split("_")
        ref_seq = get_ref_seq(file_name)
        r2_file = get_r2_file(fastq_gz_folder, file_name)
        r2_file.join(".fastq.gz")

        output_folder = f"/home/TCC/result/Trimmomatic/{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        step_01(fastq_gz_folder, r1_file, r2_file, output_folder)
        step_02(file_name, output_folder, r1_file, r2_file)
        step_03(ref_seq, output_folder, file_name)
        step_04(file_name, output_folder)
        step_05(ref_seq, output_folder, file_name)

def get_ref_seq(file_name):
    # Get RefSeq
    if Gene.Gene.RHD.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"

def get_r2_file(fastq_gz_folder, file_name):
    prefix = file_name.split("_")
    r2_file = [f for f in os.listdir(fastq_gz_folder) if (f.find(prefix[0]) != -1 and "R2" in f.upper())]
    return r2_file[0]

def step_01(fastq_gz_folder, r1_file, r2_file, output_folder):
    # Execute: TrimmomaticPE 
    # -threads 8 
    # $NAMEFILE"_L001_R1_001.fastq.gz" 
    # $NAMEFILE"_L001_R2_001.fastq.gz" 
    # $NAMEFILE"_L001_R1_trimmed_001.fastq.gz" 
    # $NAMEFILE"_L001_R1_unpaired_001.fastq.gz" 
    # $NAMEFILE"_L001_R2_trimmed_001.fastq.gz" 
    # $NAMEFILE"_L001_R2_unpaired_001.fastq.gz" 
    # ILLUMINACLIP:adapters.fasta:2:30:10:2:true 
    # HEADCROP:15 SLIDINGWINDOW:6:15 MINLEN:50

    r1_stripped = r1_file.strip(".fastq.gz")
    r2_stripped = r2_file.strip(".fastq.gz")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    adapters = "/home/TCC/implementation/00_pipeline_Trimmomatic/Adapters/adapters.fasta"

    command = f"trimmomatic PE -threads 8 \
        {fastq_gz_folder}{r1_file} \
        {fastq_gz_folder}{r2_file} \
        {output_folder}{r1_stripped}_trimmed.fastq.gz \
        {output_folder}{r1_stripped}_unpaired.fastq.gz \
        {output_folder}{r2_stripped}_trimmed.fastq.gz \
        {output_folder}{r2_stripped}_unpaired.fastq.gz \
        ILLUMINACLIP:{adapters}:2:30:10:2:true \
        HEADCROP:15 SLIDINGWINDOW:6:15 MINLEN:50"
    print("Step 1: " + command)
    subprocess.call(command, shell=True)

def step_02(file_name, output_folder, r1_file, r2_file):
    # Execute:
    # spades.py 
    # -1 $NAMEFILE"_L001_R1_trimmed_001.fastq.gz" 
    # -2 $NAMEFILE"_L001_R2_trimmed_001.fastq.gz" 
    # -t 8 --only-assembler -k 21,33,55,77 -o assembly
    
    r1_stripped = r1_file.strip(".fastq.gz")
    r2_stripped = r2_file.strip(".fastq.gz")
    if not os.path.exists(f"{output_folder}assembly/tmp/"):
        os.makedirs(f"{output_folder}assembly/tmp/")

    command = f"/home/TCC/SPAdes-3.15.5/spades.py \
        -1 {output_folder}{r1_stripped}_trimmed.fastq.gz \
        -2 {output_folder}{r2_stripped}_trimmed.fastq.gz \
        -t 8 --only-assembler -k 21,33,55,77 -o {output_folder}assembly"
    print("Step 2: " + command)
    subprocess.call(command, shell=True)

def step_03(ref_seq, output_folder, file_name):
    # Execute: 
    # minimap2 -x sr --frag=yes --secondary=yes 
    # -N 5 -p 0.8 -a 
    # refseq.fasta assembly/scaffolds.fasta 
    # | samtools view -bS -F 4 - 
    # | samtools sort -o $NAMEFILE"_sorted.bam" -
    command = f"minimap2 -x sr --frag=yes --secondary=yes -N 5 -p 0.8 -a \
        {ref_seq} {output_folder}assembly/scaffolds.fasta \
        | samtools view -bS -F 4 - \
        | samtools sort -o {output_folder}{file_name}_sorted.bam"
    print("Step 3: " + command)
    subprocess.call(command, shell=True)

def step_04(file_name, output_folder):
    # Execute: 
    # samtools index $NAMEFILE"_sorted.bam"
    command = f"samtools index {output_folder}{file_name}_sorted.bam"
    print("Step 4: " + command)
    subprocess.call(command, shell=True)

def step_05(ref_seq, output_folder, file_name):
    # Execute: 
    # SEQ_NAME=`basename refseq.fasta`
    # REF_NAME=`cat refseq.fasta | grep '>' | tr -d '>' | cut -d ' ' -f 1`
    # LENGTH=`tail -n +2 refseq.fasta | tr -d '\n' | wc -m | xargs`
    # echo -e "$REF_NAME\t$LENGTH" > my.genome
    # bedtools bamtobed -i $NAMEFILE"_sorted.bam" > reads.bed
    # bedtools genomecov -bga -i reads.bed -g my.genome | awk '$4 < 1' > zero.bed
    # maskFastaFromBed -fi refseq.fasta -bed zero.bed -fo masked.fasta
    # bcftools mpileup -Ou -f masked.fasta $NAMEFILE"_sorted.bam" | bcftools call --ploidy 1 -mv -Oz -o test.vcf.gz
    # bcftools index test.vcf.gz
    # cat masked.fasta | bcftools consensus test.vcf.gz > new_consensus.fasta
    # echo ">$SEQ_NAME" > $NAMEFILE"_draft.fasta"
    # tail -n +2 new_consensus.fasta >> $NAMEFILE"_draft.fasta"
    # sed 's/>'"$SEQ_NAME"'/>'"$SEQ_NAME"'/g' $NAMEFILE"_draft.fasta" > $NAMEFILE"_consensus.fasta"

    #seq_name = {os.path.basename(ref_seq)}
    command = f"cat {ref_seq} | grep '>' | tr -d '>' | cut -d ' ' -f 1"
    ref_name = subprocess.getoutput(command)
    command = f"tail -n +2 {ref_seq} | tr -d '\\n' | wc -m | xargs"
    length = subprocess.getoutput(command)
    command = f"echo {ref_name}\\\t{length} > {output_folder}{file_name}.genome"
    subprocess.check_call(command, shell=True)
    subprocess.check_call(f"bedtools bamtobed -i {output_folder}{file_name}_sorted.bam > {output_folder}{file_name}_reads.bed", shell=True)
    subprocess.check_call(f"bedtools genomecov -bga -i {output_folder}{file_name}_reads.bed -g {output_folder}{file_name}.genome | awk '$4 < 1' > {output_folder}{file_name}_zero.bed", shell=True)
    subprocess.check_call(f"maskFastaFromBed -fi {ref_seq} -bed {output_folder}{file_name}_zero.bed -fo {output_folder}{file_name}_masked.fasta", shell=True)
    subprocess.check_call(f"bcftools mpileup -Ou -f {output_folder}{file_name}_masked.fasta {output_folder}{file_name}_sorted.bam | bcftools call --ploidy 1 -mv -Oz -o {output_folder}{file_name}_test.vcf.gz", shell=True)
    subprocess.check_call(f"bcftools index {output_folder}{file_name}_test.vcf.gz", shell=True)
    subprocess.check_call(f"cat {output_folder}{file_name}_masked.fasta | bcftools consensus {output_folder}{file_name}_test.vcf.gz > {output_folder}{file_name}_new_consensus.fasta", shell=True)
    subprocess.check_call(f"echo {ref_name} > {output_folder}{file_name}_draft.fasta", shell=True)
    subprocess.check_call(f"tail -n +2 {output_folder}{file_name}_new_consensus.fasta >> {output_folder}{file_name}_draft.fasta", shell=True)
    subprocess.check_call(f"sed 's/>'\"{file_name}\"'/>'\"{file_name}\"'/g' {output_folder}{file_name}_draft.fasta > {output_folder}{file_name}_consensus.fasta", shell=True)
Trimmomatic()
import subprocess
import os
import Gene

import time

FASTQ_GZ_FOLDER = "/home/TCC/dataset/FASTQ/"

def Trimmomatic():
    
    print("Running Trimmomatic pipeline...\n")
    start_time = time.time()

    r1_files = [f for f in os.listdir(FASTQ_GZ_FOLDER) if (f.endswith(".fastq.gz") and "R1" in f.upper())]
    
    for r1_file in r1_files:
        file_name = r1_file.strip(".fastq.gz")
        file_name_parts = file_name.split("_")
        ref_seq = get_ref_seq(file_name)
        r2_file = get_r2_file(file_name)
        r2_file.join(".fastq.gz")

        output_folder = f"/home/TCC/result/Trimmomatic/{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}/"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        step_01(FASTQ_GZ_FOLDER, r1_file, r2_file, output_folder)
        step_02(ref_seq, r1_file, r2_file, file_name_parts, output_folder)
        step_03(output_folder, file_name_parts)
        step_04(ref_seq, output_folder, file_name_parts)
        step_05(ref_seq, output_folder, file_name_parts)
        step_06(output_folder, file_name_parts)
        step_07(output_folder, file_name_parts)
        step_08(ref_seq, output_folder, file_name_parts)
        step_09(output_folder, file_name_parts)
        step_10(output_folder, file_name_parts)
    end_time = time.time()
    print("End of Trimmomatic.")

def get_ref_seq(file_name):
    # Get RefSeq
    if Gene.Gene.RHD.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"

def get_r2_file(file_name):
    prefix = file_name.split("_")
    r2_file = [f for f in os.listdir(FASTQ_GZ_FOLDER) if (f.find(prefix[0]) != -1 and "R2" in f.upper())]
    return r2_file[0]

def step_01(r1_file, r2_file, output_folder):
    # trimmomatic PE 
    #-threads 2 -phred33 
    # 1021-22_S60_L001_R1_001.fastq.gz 
    # 1021-22_S60_L001_R2_001.fastq.gz 
    # processed/1021-22_S60_L001_R1_001_trim.fastq.gz 
    # processed/1021-22_S60_L001_R1_001_utrim.fastq.gz 
    # processed/1021-22_S60_L001_R2_001_trim.fastq.gz 
    # processed/1021-22_S60_L001_R2_001_utrim.fastq.gz 
    # ILLUMINACLIP:adapters.fasta:2:30:10 
    # LEADING:10 
    # TRAILING:10 
    # SLIDINGWINDOW:4:15 
    # HEADCROP:15 
    # MINLEN:50
    r1_stripped = r1_file.strip(".fastq.gz")
    r2_stripped = r2_file.strip(".fastq.gz")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    adapters = "/home/TCC/implementation/00_pipeline_Trimmomatic/Adapters/adapters.fasta"
    command = f"trimmomatic PE -threads 2 -phred33 \
        {FASTQ_GZ_FOLDER}{r1_file} \
        {FASTQ_GZ_FOLDER}{r2_file} \
        {output_folder}{r1_stripped}_trim.fastq.gz \
        {output_folder}{r1_stripped}_utrim.fastq.gz \
        {output_folder}{r2_stripped}_trim.fastq.gz \
        {output_folder}{r2_stripped}_utrim.fastq.gz \
        ILLUMINACLIP:{adapters}:2:30:10 \
        LEADING:10 TRAILING:10 SLIDINGWINDOW:4:15 HEADCROP:15 MINLEN:50"
    print("Step 1: " + command)
    subprocess.call(command, shell=True)

def step_02(ref_seq, r1, r2, file_name_parts, output_folder):
    # minimap2 -a -t 2 -x sr  refeseq.fasta processed/1021-22_S60_L001_R1_001_trim.fastq.gz processed/1021-22_S60_L001_R2_001_trim.fastq.gz | samtools view -bS -F 4 - | samtools sort -o 1021-22_S60.sorted.bam –
    r1_stripped = r1.strip(".fastq.gz")
    r2_stripped = r2.strip(".fastq.gz")
    command = f"minimap2 -a -t 2 -x sr \
        {ref_seq} \
        {output_folder}{r1_stripped}_trim.fastq.gz \
        {output_folder}{r2_stripped}_trim.fastq.gz \
        | samtools view -bS -F 4 - | samtools sort -o \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.sorted.bam"
    print("Step 2: " + command)
    subprocess.call(command, shell=True)

def step_03(output_folder, file_name_parts):
    command = f"samtools index {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.sorted.bam "
    print("Step 3: " + command)
    subprocess.call(command, shell=True)

def step_04(ref_seq, output_folder, file_name_parts):
    command = f"bcftools mpileup --threads 2 --max-depth 2000 -E -Ou -f \
        {ref_seq} {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.sorted.bam | bcftools call --ploidy 1 --threads 2 -mv -Oz \
        -o {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.vcf.gz"
    print("Step 4: " + command)
    subprocess.call(command, shell=True)

def step_05(ref_seq, output_folder, file_name_parts):
    command = f"bcftools norm --threads 2 -f \
        {ref_seq} \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.vcf.gz -Oz \
        -o {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.norm.vcf.gz"
    print("Step 5: " + command)
    subprocess.call(command, shell=True)

def step_06(output_folder, file_name_parts):
    command = f"bcftools filter --threads 2 --IndelGap 5 \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.norm.vcf.gz -Oz -o \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.norm.flt-indels.vcf.gz"
    print("Step 6: " + command)
    subprocess.call(command, shell=True)

def step_07(output_folder, file_name_parts):
    command = f"bcftools index --threads 2 \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.norm.flt-indels.vcf.gz"
    print("Step 7: " + command)
    subprocess.call(command, shell=True)

def step_08(ref_seq, output_folder, file_name_parts):
    command = f"bcftools consensus -f \
        {ref_seq} \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.calls.norm.flt-indels.vcf.gz \
        > {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.temp.consensus.fasta"
    print("Step 8: " + command)
    subprocess.call(command, shell=True)
    
def step_09(output_folder, file_name_parts):
    command = f"bedtools genomecov -bga -ibam \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.sorted.bam > \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.table_cov.txt" 
    print("Step 9: " + command)
    subprocess.call(command, shell=True)
def step_10(output_folder, file_name_parts):
    command = f"bedtools genomecov -d -ibam \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.sorted.bam > \
        {output_folder}{file_name_parts[0]}_{file_name_parts[1]}_{file_name_parts[2]}.table_cov_basewise.txt"
    print("Step 10: " + command)
    subprocess.call(command, shell=True)
Trimmomatic()
import subprocess
import os

#bwa mem ${SEQ}.Pilon.fasta $FASTQ | samtools sort -o ${SEQ}.Pilon.sorted.bam

INPUT_FOLDER = "/home/TCC/result/03_pilon_01/"
PILON_SORTED_FOLDER = "/home/TCC/result/02_samtools_02_sort/"
fasta_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".Pilon.fasta")]

for fasta_file in fasta_files:
    file_name = fasta_file.rstrip(".Pilon.fasta")
    # TODO: Get FASTQ file for each Pilon.fasta
    
    FASTQ_FILE = f"/home/TCC/dataset/FASTQ/uncompressed/{file_name}.fastq"
    if not os.path.isfile(FASTQ_FILE):
        print("FASTQ file not found.")
    command = f"bwa mem {INPUT_FOLDER}{file_name}.Pilon.fasta {FASTQ_FILE} | samtools sort \\-o {PILON_SORTED_FOLDER}{file_name}.Pilon.sorted.bam"
    status = subprocess.call(command, shell=True)
    print(f"BWA mem & Samtools sort complete. .fasta file saved as {file_name}.Pilon.fasta.")


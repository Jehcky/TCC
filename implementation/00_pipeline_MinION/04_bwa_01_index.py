import subprocess
import os

#bwa index ${SEQ}.Pilon.fasta

INPUT_FOLDER = "/home/TCC/result/03_pilon_01/"

fasta_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".Pilon.fasta")]

for fasta_file in fasta_files:
    file_name = fasta_file.rstrip(".Pilon.fasta")
    command = f"bwa index {INPUT_FOLDER}{file_name}.Pilon.fasta"
    status = subprocess.call(command, shell=True)
    print(f"BWA index complete. .fasta file saved as {file_name}.Pilon.fasta.")
import subprocess
import os

# minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam

INPUT_FOLDER = "/home/TCC/dataset/FASTQ/uncompressed/"
OUTPUT_FOLDER = "/home/TCC/result/01_minimap2_01_result/"
REF_SEQ_FOLDER = "/home/TCC/implementation/RefSeq/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

fastq_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".fastq")]

for fastq_file in fastq_files:
    fastq_name = fastq_file.rstrip(".fastq")
    command = f"minimap2 -ax map-ont {REF_SEQ_FOLDER}RefSeq_RHD.fasta {INPUT_FOLDER}{fastq_name}.fastq > {OUTPUT_FOLDER}{fastq_name}.PrePilon.sam"

    status = subprocess.call(command, shell=True)
    if status:
        print(f"Minimap2 map-ont complete. .SAM file saved as {fastq_name}.PrePilon.sam.")
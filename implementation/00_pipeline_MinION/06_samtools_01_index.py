import subprocess
import os

# samtools index ${SEQ}.PrePilon.sorted.bam

INPUT_FOLDER = "/home/TCC/result/02_samtools_02_sort/"

bam_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".PrePilon.sorted.bam")]

for bam_file in bam_files:
    file_name = bam_file.rstrip(".PrePilon.sorted.bam")
    command = f"samtools index {INPUT_FOLDER}{file_name}.PrePilon.sorted.bam"
    status = subprocess.call(command, shell=True)
    print(f"Samtools index complete. .BAM file saved as {file_name}.PrePilon.sorted.bam.")
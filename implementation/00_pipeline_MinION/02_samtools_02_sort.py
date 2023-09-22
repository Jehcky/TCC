import subprocess
import os

# samtools sort ${SEQ}.PrePilon.bam -o ${SEQ}.PrePilon.sorted.bam

INPUT_FOLDER = "/home/TCC/result/02_samtools_01_view/"
OUTPUT_FOLDER = "/home/TCC/result/02_samtools_02_sort/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

bam_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".PrePilon.bam")]

for bam_file in bam_files:
    file_name = bam_file.rstrip(".PrePilon.bam")
    command = f"samtools sort {INPUT_FOLDER}{file_name}.PrePilon.bam -o {OUTPUT_FOLDER}{file_name}.PrePilon.sorted.bam"
    status = subprocess.call(command, shell=True)
    print(f"Samtools sort complete. .BAM file saved as {file_name}.PrePilon.sorted.bam.")
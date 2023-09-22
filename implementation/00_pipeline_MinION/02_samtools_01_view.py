import subprocess
import os

# samtools view -S -b ${SEQ}.PrePilon.sam > ${SEQ}.PrePilon.bam

INPUT_FOLDER = "/home/TCC/result/01_minimap2_01/"
OUTPUT_FOLDER = "/home/TCC/result/02_samtools_01_view/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

sam_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".PrePilon.sam")]

for sam_file in sam_files:
    file_name = sam_file.rstrip(".PrePilon.sam")
    command = f"samtools view -S -b {INPUT_FOLDER}{file_name}.PrePilon.sam > {OUTPUT_FOLDER}{file_name}.PrePilon.bam"
    print(f"Samtools view complete. .BAM file saved as {file_name}.PrePilon.bam.")
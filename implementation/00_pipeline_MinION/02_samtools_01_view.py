import subprocess
import os

# samtools view -S -b ${SEQ}.PrePilon.sam > ${SEQ}.PrePilon.bam

INPUT_FOLDER = "/home/TCC/result/01_minimap2_01_result/"
OUTPUT_FOLDER = "/home/TCC/result/02_samtools_01_view_result/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

sam_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".PrePilon.sam")]

for sam_file in sam_files:
    sam_name = sam_file.rstrip(".PrePilon.sam")
    command = f"samtools view -S -b {INPUT_FOLDER}{sam_name}.PrePilon.sam > {OUTPUT_FOLDER}{sam_name}.PrePilon.bam"

    status = subprocess.call(command, shell=True)
    if status:
        print(f"Samtools view complete. .BAM file saved as {sam_name}.PrePilon.bam.")
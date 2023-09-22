import subprocess
import os
import Gene

# minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam

FASTQ_FOLDER = "/home/TCC/dataset/FASTQ/uncompressed/"
OUTPUT_FOLDER = "/home/TCC/result/01_minimap2_01/"

fastq_files = [f for f in os.listdir(FASTQ_FOLDER) if f.endswith(".fastq")]

for fastq_file in fastq_files:

    fastq_name = fastq_file.rstrip(".fastq")
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    if Gene.Gene.RHD.value in fastq_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in fastq_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"
        
    command = f"minimap2 -ax map-ont {ref_seq_file} {FASTQ_FOLDER}{fastq_name}.fastq > {OUTPUT_FOLDER}{fastq_name}.PrePilon.sam"
    subprocess.call(command, shell=True)
    print(f"Minimap2 map-ont complete. .SAM file saved as {fastq_name}.PrePilon.sam.")

    
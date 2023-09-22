import subprocess
import os
import Gene

#pilon --genome $REF_FILE --frags ${SEQ}.PrePilon.sorted.bam --output ${SEQ}.Pilon --fix "gaps,indels" --threads 1 --mindepth 5

INPUT_FOLDER = "/home/TCC/result/02_samtools_02_sort/"
OUTPUT_FOLDER = "/home/TCC/result/03_pilon_01/"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

bam_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".PrePilon.sorted.bam")]

for bam_file in bam_files:
    file_name = bam_file.rstrip(".PrePilon.sorted.bam")

    if Gene.Gene.RHD.value in file_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in file_name:
        ref_seq_file = f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"
        
    command = f"pilon --genome {ref_seq_file} --frags {INPUT_FOLDER}{bam_file} --output {OUTPUT_FOLDER}{file_name}.Pilon --fix \"gaps,indels\" --threads 1 --mindepth 5"
    status = subprocess.call(command, shell=True)
    print(f"Pilon complete. .Pilon file saved as {file_name}.Pilon.fasta")
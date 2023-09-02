import subprocess
import pysam

# minimap2 command
# minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam
minimap2_command = [
"minimap2"
,
"-ax"
,
"map-ont"
,
"/data/TCC/implementation/RefSeq/RefSeq_RHD.fasta"
,
"/data/TCC/dataset/FASTQ/uncompressed/AF2RHD_S55_L001_R2_001.fastq"
,
">"
,
"AF2RHD_S55_L001_R1_001.PrePilon.sam"
]

# Execute minimap2 and get the output
output_minimap2 = subprocess.check_output(minimap2_command, universal_newlines=True)

# Exibir a saída do minimap2
print(output_minimap2)
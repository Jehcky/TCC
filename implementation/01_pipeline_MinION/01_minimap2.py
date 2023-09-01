import subprocess

# minimap2 command
# minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam
minimap2_command = [
"minimap2"
, 
"-ax"
, 
"map-ont"
, 
"sequencia_referencia.fasta"
, 
"sequencia_query.fastq",

"> ${SEQ}.PrePilon.sam"
]

# Execute minimap2 and get the output
output_minimap2 = subprocess.check_output(minimap2_command, universal_newlines=True)

# Exibir a saída do minimap2
print(output_minimap2)
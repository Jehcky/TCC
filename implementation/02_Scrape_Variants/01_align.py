import sys
sys.path.append('/home/TCC/implementation')
import os
import subprocess
import Gene

VARIANTS_FOLDER = "/home/TCC/GeneVariants/"
REF_SEQ_FOLDER = "/home/TCC/implementation/RefSeq/"
OUTPUT_FOLDER = "/home/TCC/GeneVariants/Aligned/"
    
def multiple_alignment():
    for gene in Gene.Gene:
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
        if not os.path.exists(f"{OUTPUT_FOLDER}{gene.name}/"):
            os.makedirs(f"{OUTPUT_FOLDER}{gene.name}/")
        gene_file = f"{VARIANTS_FOLDER}{gene.name}.fasta"
        ref_seq = f"{REF_SEQ_FOLDER}RefSeq_{gene.name}.fasta"
        command = f"mafft --auto {gene_file} > {OUTPUT_FOLDER}{gene.name}/{gene.name}_aligned.fasta"
        print("Aligning with MAFFT: " + command)
        subprocess.call(command, shell=True)

multiple_alignment()
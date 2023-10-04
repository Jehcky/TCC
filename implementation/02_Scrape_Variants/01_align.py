import sys
sys.path.append('/home/TCC/implementation')
import os
import subprocess
import Gene

RESULT_FOLDER = "/home/TCC/GeneVariants/Alignment/"

def get_ref_seq(file_name):
    if Gene.Gene.RHD.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHD.value}.fasta"
    elif Gene.Gene.RHCE.value in file_name:
        return f"/home/TCC/implementation/RefSeq/RefSeq_{Gene.Gene.RHCE.value}.fasta"
    
def multiple_alignment():
    consensus_list = os.listdir(RESULT_FOLDER)
    for consensus in consensus_list:
        consensus_file = f"{RESULT_FOLDER}{consensus}/{consensus}.temp.consensus.fasta"
        ref_seq = get_ref_seq(consensus)
        command = f"mafft --auto {consensus_file} > {RESULT_FOLDER}{consensus}/{consensus}_mafft.fasta"
        print("Aligning with MAFFT: " + command)
        subprocess.call(command, shell=True)

multiple_alignment()
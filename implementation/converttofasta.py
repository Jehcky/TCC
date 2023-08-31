import os
from Bio import SeqIO
import gzip

def convert_to_fasta():
    FASTQ_FOLDER = "/data/TCC/dataset/FASTQ/"
    FASTA_FOLDER = "/data/TCC/dataset/FASTA/"
    
    # Se não houver a pasta de destino, ela será criada
    #if not os.path.exists(FASTA_FOLDER):
    #    os.makedirs(FASTA_FOLDER)

    # Lista todos os arquivos na pasta de entrada que têm a extensão .fastq
    fastq_files = [f for f in os.listdir(FASTQ_FOLDER) if f.endswith(".fastq.gz")]

    count_files = 0
    # Loop para percorrer os arquivos FASTQ
    for fastq_file in fastq_files:
        
        fastq_complete_path = os.path.join(FASTQ_FOLDER, fastq_file)

        new_fasta_filename = fastq_file.replace(".fastq.gz", ".fasta")
        fasta_complete_path = os.path.join(FASTA_FOLDER, new_fasta_filename)

        with gzip.open(fastq_complete_path, "rt") as fastq_file, open(fasta_complete_path, "w") as fasta_file:
            count_records = 0
            for record in SeqIO.parse(fastq_file, "fastq"):
                SeqIO.write(record, fasta_file, "fasta")
                count_records += 1
        count_files += 1        

        print("Número de registros do arquivo (" + new_fasta_filename + "): " + str(count_records))
    print("Conversão concluída.")
    print("Número de arquivos convertidos: " + str(count_files))
    
    

def main():
    convert_to_fasta()

if __name__ == '__main__':
    main()
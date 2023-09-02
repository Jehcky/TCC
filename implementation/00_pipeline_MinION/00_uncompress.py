import os
import gzip
import shutil

# Pasta onde os arquivos .fastq.gz estão localizados
INPUT_FOLDER = "/data/TCC/dataset/FASTQ"
OUTPUT_FOLDER = "/data/TCC/dataset/FASTQ/uncompressed"

# Verificar se a pasta de saída existe; se não existir, ela é criada
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Listar todos os arquivos na pasta de entrada que possuem a extensão .fastq.gz
fastq_gz_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".fastq.gz")]

# Loop através de cada arquivo .fastq.gz encontrado
for fastq_gz_file in fastq_gz_files:
    # Constrir o caminho completo para o arquivo .fastq.gz de entrada
    fastq_gz_complete_path = os.path.join(INPUT_FOLDER, fastq_gz_file)

    # Constrir o caminho completo para o arquivo descomprimido
    complete_output_path = os.path.join(OUTPUT_FOLDER, fastq_gz_file.replace(".gz", ""))

    # Abrir o arquivo .fastq.gz de entrada, descomprimir e salvar
    with gzip.open(fastq_gz_complete_path, 'rb') as f_in:
        with open(complete_output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

print("Descompressão concluída!")
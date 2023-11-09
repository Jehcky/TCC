import pysam
import vcf

# Caminho para o arquivo BAM
bam_file = "AF2RHD_S55_sorted.bam"

# Caminho para o arquivo VCF gerado no pipeline
vcf_file = "test.vcf.gz"

# Abrir o arquivo BAM
bam = pysam.AlignmentFile(bam_file, "rb")

# Inicializar o leitor VCF
vcf_reader = vcf.Reader(filename=vcf_file)

# Loop através das entradas do VCF
for record in vcf_reader:
    # Obter informações sobre a posição do SNP
    chrom = record.CHROM
    pos = record.POS
    ref = record.REF
    alt = str(record.ALT[0])  # Assumindo um único SNP

    # Coletar informações do BAM na posição do SNP
    for pileupcolumn in bam.pileup(chrom, pos - 1, pos):
        if pileupcolumn.pos == pos - 1:
            # Analisar as leituras que cobrem o SNP
            for pileupread in pileupcolumn.pileups:
                if pileupread.query_position is not None:
                    # Obter a base na posição do SNP
                    base = pileupread.alignment.query_sequence[pileupread.query_position]

                    # Verificar se a base difere da referência (SNP)
                    if base != ref:
                        print(f"SNP encontrado em {chrom}:{pos}, Ref: {ref}, Alt: {alt}")
                        break

# Fechar os arquivos
bam.close()
vcf_reader.close()

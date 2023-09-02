import subprocess
import pysam

# minimap2 command
# minimap2 -ax map-ont $REF_FILE $FASTQ > ${SEQ}.PrePilon.sam
minimap2_command = ["minimap2",
                    "-ax",
                    "map-ont",
                    "/home/TCC/implementation/RefSeq/RefSeq_RHD.fasta",
                    "/home/TCC/dataset/FASTQ/uncompressed/AF2RHD_S55_L001_R2_001.fastq",
                    ">",
                    "AF2RHD_S55_L001_R1_001.PrePilon.sam"]

# Execute minimap2 and get the output
output_minimap2 = subprocess.check_output(minimap2_command, universal_newlines=True)

# Path to the output BAM file
bam_file = "output.bam"

# Create a BAM file for writing
output_bam = pysam.AlignmentFile(bam_file, "wb", header={"HD": {"VN": "1.6"}, "SQ": [{"LN": 1000, "SN": "chr1"}]})

# Read the text file and convert it to BAM format
#with open(text_file, 'r') as text_data:
for line in output_minimap2:
    parts = line.strip().split('\t')
    if len(parts) != 2:
        continue

    read_name, sequence = parts
    read = pysam.AlignedSegment()
    read.query_name = read_name
    read.query_sequence = sequence
    read.flag = 0
  
# Assuming no special flags
    read.reference_id = 0
  
# Assuming a single reference sequence
    read.reference_start = 0
  
# Start position on the reference
    read.mapping_quality = 255
  
# Maximum mapping quality
    output_bam.write(read)

# Close the BAM file
output_bam.close()

print("Conversão para BAM completa.")
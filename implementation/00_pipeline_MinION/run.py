from pathlib import Path

exec(Path("/home/TCC/implementation/00_pipeline_MinION/01_minimap2_01.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/02_samtools_01_view.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/02_samtools_02_sort.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/02_samtools_03_index.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/03_pilon_01.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/04_bwa_01_index.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/05_bwa_02_mem.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/06_samtools_01_index.py").read_text())
exec(Path("/home/TCC/implementation/00_pipeline_MinION/07_bedtools_01_bamtobed_genomecov.py").read_text())
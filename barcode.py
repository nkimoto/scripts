import gzip
import sys
import os

barcode = ""
detarame = "GGGGGGGG"
output_lines = []
fastq = "mini_pbmc4k_S1_L001_I1_001.fastq.gz"
newfile = os.path.splitext(fastq)[0] + "_new" + os.path.splitext(fastq)[1]
with gzip.open(fastq, "rt") as rf:
    for i, l in enumerate(rf):
        if i % 4 == 0:
            if i == 0:
                barcode = l[-9:-1].strip()
            output_lines.append(l.strip())
            print(l)
        output_lines.append(barcode)
        output_lines.append("+")
        output_lines.append(detarame)
res = "\n".join(output_lines)
with gzip.open(newfile, "wt") as wf:
    wf.write(res)


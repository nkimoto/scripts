# /usr/bin/env python

def get_genbank(gen_ids):
    Entrez.email = "kimoppy126@gmail.com"
    handle = Entrez.efetch(db='nucleotide', id=gen_ids, rettype="fasta")
    records = handle.read()
    print(records)

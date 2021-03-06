# Genome A
2016.3 -

# Requirements
- Python 3 with Anaconda  

##### Package install with pip (if you don't have Anaconda environment)  
  pip install requests  
  pip install beautifulsoup4  

### other required packages
- Biopython   for reannotate_gbk_mp.py  
  -> pip install biopython


# Description
- reannotate_gbk_mp.py : load genbank file from stdin, reannotate using G-links, output reannotated genbank file to stdout  

- get_desc_from_microbiome_wiki.py : load genus name or species name from stdin, get "Description and significance" content from micriobio wiki, output plain text (without reference parenthesis) to stdout

- make_reflist_from_ncbi_genomelist.py : input (stdin) -> NCBI Genome List (tsv), output -> Genome A reference (like) format (text, '\n' separated).   

- pmid2ref.py : input -> pmid , output -> Genome A reference (like) format (text).
ex.
```Bash
$ echo "15508840" | python pmid2ref.py
Ayling RD, Bashiruddin SE, Nicholas RA. 2004. Mycoplasma species and related organisms isolated from ruminants in Britain between 1990 and 2000. Vet Rec. 155:413-416.%
```

- pmid2ref_mp.py : (maybe) faster and **robust** version of 'pmid2ref.py'.



## Memo

### SPAdes
http://spades.bioinf.spbau.ru/release3.7.1/manual.html
##### output
http://spades.bioinf.spbau.ru/release3.7.1/manual.html#sec3.5

<output_dir>/corrected/ directory contains reads corrected by BayesHammer in *.fastq.gz files; if compression is disabled, reads are stored in uncompressed *.fastq files  
<output_dir>/contigs.fasta contains resulting contigs  
<output_dir>/scaffolds.fasta contains resulting scaffolds  
<output_dir>/assembly_graph.fastg contains SPAdes assembly graph in FASTG format  
<output_dir>/contigs.paths contains paths in the assembly graph corresponding to contigs.fasta (see details below)  
<output_dir>/scaffolds.paths contains paths in the assembly graph corresponding to scaffolds.fasta (see details below)

### QUAST
http://quast.bioinf.spbau.ru/manual.html
